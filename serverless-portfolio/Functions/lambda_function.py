## Code Snippets

### Lambda Function (`lambda_function.py`)
import json
import boto3
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Log the received event
    print("Received event:", json.dumps(event))
    
    # Extract name and comment
    name = event.get('name', 'Unknown')
    comment = event.get('comment', 'No comment')
    print(f"Name: {name}, Comment: {comment}")
    
    # Prepare data to save
    data = {
        'name': name,
        'comment': comment,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Define S3 bucket and file key
    bucket_name = 'mini-hello'  # Replace with your bucket name
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    file_key = f'messages/{timestamp}-{context.aws_request_id}.json'
    
    # Write to S3
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        print(f"Saved to S3: s3://{bucket_name}/{file_key}")
    except Exception as e:
        print(f"Error saving to S3: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Failed to save message'})
        }
    
    # Return success response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Message received and saved'})
    }