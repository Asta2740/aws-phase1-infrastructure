import os
import re
import json
import logging
import psycopg2
import boto3
import subprocess
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    filename='/var/log/check_ips.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# 🔹 Log file path
AUTH_LOG_PATH = "/var/log/auth.log"

# 🔹 Authentication failure messages to search for
FAILURE_MESSAGES = [
    "No supported authentication",
    "UnAuthorized",
    "invalid user",
    "AuthorizedKeysCommand"
]

# 🔹 Regex pattern to extract IPs
IP_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+)')

# 🔹 Database connection details
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': '5432'
}

# 🔹 AWS Lambda client (adjust region as needed)
lambda_client = boto3.client('lambda', region_name='eu-central-1')

# 🔥 Function to extract problematic IPs
def get_problematic_ips():
    try:
        ip_counts = {}
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)

        logger.info(f"Reading authentication log from {AUTH_LOG_PATH}")

        # 🔹 Run grep command to get failed authentication logs
        grep_command = f'grep -E "{"|".join(FAILURE_MESSAGES)}" {AUTH_LOG_PATH}'
        result = subprocess.run(grep_command, shell=True, capture_output=True, text=True)

        if not result.stdout:
            logger.info("No matching log entries found.")
            return []

        # 🔹 Process each log line
        for line in result.stdout.splitlines():
            ip_match = IP_PATTERN.search(line)
            if ip_match:
                ip = ip_match.group(1)
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # 🔹 Filter IPs with more than 5 errors
        ip_list = [{'ip': ip, 'error_count': count} for ip, count in ip_counts.items() if count > 5]

        logger.info(f"Found {len(ip_list)} problematic IPs")
        return ip_list

    except Exception as e:
        logger.error(f"Error in get_problematic_ips: {str(e)}")
        return []

# 🔥 Function to check IPs against database
def check_and_store_ips(ip_list):
    new_ips = []

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # 🔹 Create table if not exists
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ip_errors (
                ip VARCHAR(45) PRIMARY KEY,
                timestamp TIMESTAMP,
                error_count INTEGER
            )
        ''')

        logger.info("Checking IPs against database")

        for ip_data in ip_list:
            ip = ip_data['ip']
            cur.execute("SELECT EXISTS(SELECT 1 FROM ip_errors WHERE ip = %s)", (ip,))
            exists = cur.fetchone()[0]

            if not exists:
                new_ips.append(ip_data)
                cur.execute(
                    "INSERT INTO ip_errors (ip, timestamp, error_count) VALUES (%s, %s, %s)",
                    (ip, datetime.now(), ip_data['error_count'])
                )
                logger.info(f"Added new IP to database: {ip}")

        conn.commit()
        logger.info(f"Stored {len(new_ips)} new IPs in database")

    except psycopg2.Error as e:
        logger.error(f"Database error in check_and_store_ips: {str(e)}")
    except Exception as e:
        logger.error(f"Error in check_and_store_ips: {str(e)}")
    finally:
        cur.close()
        conn.close()

    return new_ips

# 🔥 Function to trigger AWS Lambda
def trigger_lambda(new_ips):
    try:
        if new_ips:
            logger.info(f"Sending {len(new_ips)} new IPs to Lambda")
            lambda_client.invoke(
                FunctionName='ALC_Denier',  # 🔹 Replace with actual Lambda function name
                InvocationType='Event',
                Payload=json.dumps({'new_ips': new_ips})
            )
            logger.info("Successfully triggered Lambda")
    except Exception as e:
        logger.error(f"Error triggering Lambda: {str(e)}")

# 🔥 Main function
def main():
    try:
        # Step 1: Get problematic IPs
        problematic_ips = get_problematic_ips()

        if not problematic_ips:
            logger.info("No problematic IPs found")
            print("No problematic IPs found")
            return

        # Step 2: Check against database and store new IPs
        new_ips = check_and_store_ips(problematic_ips)

        # Step 3: Trigger AWS Lambda if new IPs are found
        if new_ips:
            logger.info(f"New IPs detected: {json.dumps(new_ips)}")
            print("New IPs detected:")
            print(json.dumps(new_ips, indent=2))
            trigger_lambda(new_ips)
        else:
            logger.info("No new IPs detected")
            print("No new IPs detected")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
