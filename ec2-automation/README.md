# EC2 Automation with Lambda and Step Functions

## Project Overview
This project automates the restart of EC2 instances when CPU utilization exceeds 80% for 5 minutes, using AWS Lambda, Step Functions, and CloudWatch. It showcases event-driven automation and orchestration.

## Architecture Diagram
[Insert architecture diagram here]

## Setup Instructions
1. **IAM Role**:
   - Create a role (e.g., `ec2-automation-role`) with permissions for EC2 (`ec2:StopInstances`, `ec2:StartInstances`, `ec2:DescribeInstances`) and CloudWatch Logs.

2. **Lambda Functions**:
   - **StopEC2Instances**: [stop_ec2.py](./stop_ec2.py)
   - **StartEC2Instances**: [start_ec2.py](./start_ec2.py)
   - **CheckEC2Instances**: [check_ec2.py](./check_ec2.py)
   - Runtime: Python 3.9
   - Attach the IAM role created above.

3. **Step Function**:
   - Create a state machine named `EC2RestartStateMachine`.
   - Definition: [step_function.json](./step_function.json)
   - Replace `<ARN>` placeholders with the actual Lambda ARNs.

4. **CloudWatch Alarm**:
   - Metric: CPUUtilization > 80% for 5 minutes.
   - Action: Trigger the Step Function via SNS or direct integration.

5. **Test the Automation**:
   - Simulate high CPU usage (e.g., using `stress` on the EC2 instance).
   - Verify the instance stops and restarts.

## Code Snippets

### StopEC2Instances (`stop_ec2.py`)
```python
import boto3

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = event['instance_id']
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    return {'status': 'stopping', 'instance_id': instance_id}