import boto3
import json
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize AWS EC2 client
    ec2_client = boto3.client('ec2')
    
    # Network ACL ID
    nacl_id = 'Your acl ID'
    
    try:
        new_ips_data = event.get('new_ips', [])
        specific_ips = [ip_data['ip'] for ip_data in new_ips_data]  # Extract just the IP addresses
        if not specific_ips:
            logger.info("No IPs provided in event payload")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No IPs provided to process'})
            }
    except KeyError as e:
        logger.error(f"Invalid event payload: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid event payload format'})
        }
    try:
        logger.info(f"Describing Network ACL: {nacl_id}")
        # Get current NACL entries
        response = ec2_client.describe_network_acls(NetworkAclIds=[nacl_id])
        
        # Extract inbound rules and track used rule numbers and existing IPs
        inbound_rules = []
        used_rule_numbers = set()
        existing_ips = set()
        
        logger.info("Processing NACL entries")
        for nacl in response['NetworkAcls']:
            for entry in nacl['Entries']:
                if not entry.get('Egress', True):  # Inbound rules only
                    rule = {
                        'RuleNumber': entry['RuleNumber'],
                        'Type': entry.get('Protocol', '-1'),
                        'Protocol': 'All' if entry['Protocol'] == '-1' else entry['Protocol'],
                        'PortRange': entry.get('PortRange', {'From': 'All', 'To': 'All'}),
                        'Source': entry['CidrBlock'],
                        'Action': entry['RuleAction']
                    }
                    inbound_rules.append(rule)
                    used_rule_numbers.add(entry['RuleNumber'])
                    existing_ips.add(entry['CidrBlock'])  # Track existing IPs (e.g., '192.168.1.1/32')
        
        logger.info(f"Found {len(inbound_rules)} inbound rules, used numbers: {sorted(used_rule_numbers)}, existing IPs: {existing_ips}")
        
        # Filter out IPs that already exist in the NACL
        new_ips_to_add = [ip for ip in specific_ips if f"{ip}/32" not in existing_ips]
        logger.info(f"New IPs to add: {new_ips_to_add}")
        
        # Add new deny rules for IPs not already present, counting down from 32765
        if new_ips_to_add:
            next_rule_number = 32765  # Start just below the max (32766)
            new_rules_added = []
            
            for ip in new_ips_to_add:
                # Find the next available number counting down
                while next_rule_number in used_rule_numbers and next_rule_number > 0:
                    next_rule_number -= 1
                
                if next_rule_number <= 0:
                    logger.error("No available rule numbers left")
                    return {
                        'statusCode': 500,
                        'body': json.dumps({'error': 'No available rule numbers left'})
                    }
                
                logger.info(f"Creating deny rule for IP: {ip} with rule number: {next_rule_number}")
                ec2_client.create_network_acl_entry(
                    NetworkAclId=nacl_id,
                    RuleNumber=next_rule_number,
                    Protocol='-1',  # All protocols
                    RuleAction='deny',
                    Egress=False,  # Inbound
                    CidrBlock=f'{ip}/32',
                    PortRange={
                        'From': 0,
                        'To': 65535
                    }
                )
                used_rule_numbers.add(next_rule_number)
                new_rules_added.append(next_rule_number)
                next_rule_number -= 1  # Decrement for the next rule
            
            # Refresh rules after adding new entries
            response = ec2_client.describe_network_acls(NetworkAclIds=[nacl_id])
            inbound_rules = [
                {
                    'RuleNumber': entry['RuleNumber'],
                    'Type': entry.get('Protocol', '-1'),
                    'Protocol': 'All' if entry['Protocol'] == '-1' else entry['Protocol'],
                    'PortRange': entry.get('PortRange', {'From': 'All', 'To': 'All'}),
                    'Source': entry['CidrBlock'],
                    'Action': entry['RuleAction']
                }
                for nacl in response['NetworkAcls']
                for entry in nacl['Entries']
                if not entry.get('Egress', True)
            ]
            logger.info(f"Added new rules: {new_rules_added}")
        else:
            logger.info("No new IPs to add; all specified IPs already exist in NACL")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'inbound_rules': inbound_rules,
                'ips_checked': specific_ips,
                'new_ips_added': new_ips_to_add
            })
        }
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }