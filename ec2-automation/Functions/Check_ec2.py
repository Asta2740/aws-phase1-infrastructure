import boto3

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    # Retrieve instance ID from event with a sensible key
    instance_id = event.get('instance_id', '(e.g., i-1234567890abcdef0)') 
    
    # Validate that instance_id is provided
    if not instance_id:
        return {'error': 'instance_id not provided'}
    
    try:
        # Call EC2 API to get instance details
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        
        # Check if the instance exists
        if not response['Reservations']:
            return {'error': 'instance not found'}
        
        # Extract the instance state
        state = response['Reservations'][0]['Instances'][0]['State']['Name']
        
        # Return status and instance ID
        return {'status': state, 'instance_id': instance_id}
    
    except Exception as e:
        # Handle any API errors (e.g., permissions, invalid ID)
        return {'error': str(e)}