# Security Enhancements with Network ACLs

## Project Overview
- **Goal**: Block malicious IPs based on Apache log analysis to protect a web application.
- **Key AWS Services**: EC2, RDS, Lambda, Network ACLs, CloudWatch Logs.
- **Context**: Part of my journey to master AWS security, following tasks like automated EC2 restarts and web server deployment.

## Key Concepts
- **Network ACLs**: Stateless, subnet-level firewall rules for controlling traffic (used here to block IPs).
- **Threat Detection**: Analyzing Apache logs to identify IPs with excessive 400-410 errors.
- **Automation**: Using EC2 scripts and Lambda to dynamically update security rules.
- **Scalability**: Leveraging AWS services to handle growing traffic and threats.

## Technical Implementation
1. **Log Analysis on EC2**:
   - Script: `codes/ssh_Ip_check.py` `codes/apache_ip_check.py`
   - Analyzes Apache logs hourly, identifies IPs with >5 errors (400-410) in the last hour, and stores them in RDS.
2. **RDS Storage**:
   - Config: `configs/rds_table.sql`
   - Stores problematic IPs with timestamps and error counts.
3. **Lambda NACL Updates**:
   - Script: `codes/Lambda_ALC_Denier.py`
   - Updates Network ACLs to deny traffic from identified IPs.
4. **IAM Permissions**:
   - Configs: `configs/iam_logs_policy.json`, `configs/iam_ec2_lambda_policy.json`
   - Grants access to logs, EC2, and NACL operations.
5. **Log Query**:
   - Config: `configs/log_query.txt`
   - Filters and aggregates log data for analysis.

## Architecture
*(Placeholder for diagram: `diagrams/architecture_diagram.png`)*  
- EC2 runs `check_ips.py` hourly via crontab.
- Logs are pulled from CloudWatch Logs.
- IPs are stored in RDS and sent to Lambda.
- Lambda updates the Network ACL using its ID.

## Real-World Use Case
This setup mimics a basic intrusion prevention system (IPS), blocking IPs that might indicate brute force attempts or misconfigured bots hitting my web server.

## Lessons Learned
- Network ACLs are cost-effective but limited by rule caps (default 20, max 32766).
- Dynamic IPs mean this is more about detection than permanent blocking.
- Error handling and monitoring need more attention for production use.

## Files
- `codes/`: Python scripts for EC2 and Lambda.
- `configs/`: SQL, IAM policies, and log query.
- `diagrams/`: Space for architecture visuals (to be added).

## Notes:
- i know there is more ways to do this , using ubuntu firewall using WAF and many more ways but i am always looking for the way that will make me interact with the services as i am currently learning this is also a study journey not a public guide whatsoever 