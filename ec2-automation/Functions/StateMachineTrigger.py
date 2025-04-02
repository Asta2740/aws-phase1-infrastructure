import json
import boto3
from datetime import datetime

step_function_arn = "arn:aws:states:[Region]:[Account number]:stateMachine:MyStateMachine-MachineRestartflow"


client = boto3.client("stepfunctions")

def lambda_handler(event, context):
    response = client.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps(event, default=str)  # 👈 Converts datetime to string
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response, default=str)  # 👈 Ensure response is JSON serializable
    }
