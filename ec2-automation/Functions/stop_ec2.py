import boto3

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    # Retrieve instance ID from event
    instance_id = event.get('instance_id', '(e.g., i-1234567890abcdef0)') 

    
    # Validate instance_id
    if not instance_id or not isinstance(instance_id, str) or not instance_id.startswith('i-'):
        return {'error': 'valid instance_id required (e.g., i-1234567890abcdef0)'}
    
    try:
        # Attempt to stop the instance
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        
        # Extract the state transition from the response
        current_state = response['StoppingInstances'][0]['CurrentState']['Name']
        previous_state = response['StoppingInstances'][0]['PreviousState']['Name']
        
        # Return success with state details
        return {
            'status': 'stopping' if current_state == 'stopping' else current_state,
            'instance_id': instance_id,
            'previous_state': previous_state
        }
    
    except ec2_client.exceptions.ClientError as e:
        # Handle specific AWS errors
        error_code = e.response['Error']['Code']
        if error_code == 'IncorrectInstanceState':
            # Instance might already be stopped or in a state that prevents stopping
            return {'error': 'instance cannot be stopped', 'details': str(e)}
        elif error_code == 'InvalidInstanceID.NotFound':
            return {'error': 'instance not found', 'details': str(e)}
        else:
            return {'error': 'failed to stop instance', 'details': str(e)}
    except Exception as e:
        # Catch any other unexpected errors
        return {'error': 'unexpected error', 'details': str(e)}