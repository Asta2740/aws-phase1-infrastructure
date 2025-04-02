import socket
import psycopg2
import boto3
import os

# Connect to CloudWatch (no credentials needed with IAM role)
cloudwatch = boto3.client('cloudwatch', region_name='eu-central-1')

try:
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sessions WHERE last_activity > NOW() - INTERVAL '30 minutes'")
    active_sessions = cur.fetchone()[0]
    print(f"Active sessions: {active_sessions}")
except Exception as e:
    print(f"Database error: {e}")
    active_sessions = 0  # Default value if query fails
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()

# Send the metric to CloudWatch
response = cloudwatch.put_metric_data(
    Namespace='PythonWebMetric',
    MetricData=[
        {
            'MetricName': 'ActiveSessions',
            'Dimensions': [
                {
                    'Name': 'Machine',
                    'Value': 'Pre_production'
                }
            ],
            'Value': int(active_sessions),
            'Unit': 'Count'
        }
    ]
)
print(response)
