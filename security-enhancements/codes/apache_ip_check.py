import socket
import psycopg2
import boto3
import os
import re
import json
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    filename='/var/log/Apache_check_ips.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

# Database connection details (using environment variables as in your code)
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST'),
    'port': '5432'
}

# Lambda client (kept for future use, though not used yet)
lambda_client = boto3.client('lambda', region_name='eu-central-1')

# Apache log pattern
LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<logTime>[^\]]+)] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d{3}) (?P<bytes>\d+) "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)

def get_problematic_ips():
    try:
        ip_counts = {}
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=23)
        print(start_time)
        logger.info("Reading Apache access log from /var/log/apache2/access.log")
        with open('/var/log/apache2/access.log', 'r') as f:
            for line in f:
                match = LOG_PATTERN.match(line.strip())
                if not match:
                    continue

                log_time_str = match.group('logTime')
                # Convert Apache log time to datetime (format: 25/Mar/2025:12:34:56 +0000)
                log_time = datetime.strptime(log_time_str.split()[0], '%d/%b/%Y:%H:%M:%S')

                # Check if log entry is within the last hour
                if start_time <= log_time <= end_time:
                    status = int(match.group('status'))
                    ip = match.group('ip')

                    # Count 400-410 status codes
                    if 400 <= status <= 410:
                        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Filter IPs with more than 5 errors
        ip_list = [
            {'ip': ip, 'error_count': count}
            for ip, count in ip_counts.items()
            if count > 4
        ]
        logger.info(f"Found {len(ip_list)} IPs with frequent errors")
        return ip_list

    except FileNotFoundError:
        logger.error("Apache access log file not found at /var/log/apache2/access.log")
        return []
    except Exception as e:
        logger.error(f"Error in get_problematic_ips: {str(e)}")
        return []

def check_and_store_ips(ip_list):
    new_ips = []

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Create table if it doesn't exist (matching your original schema)
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

def trigger_lambda(new_ips):
    try:
        if new_ips:
            logger.info(f"Sending {len(new_ips)} new IPs to Lambda")
            lambda_client.invoke(
                FunctionName='ALC_Denier',  # Replace with actual name
                InvocationType='Event',
                Payload=json.dumps({'new_ips': new_ips})  # Matches Lambda's expected format
            )
            logger.info("Successfully triggered Lambda")
    except Exception as e:
        logger.error(f"Error triggering Lambda: {str(e)}")

def main():
    try:
        # Get IPs from local Apache log
        problematic_ips = get_problematic_ips()

        if not problematic_ips:
            logger.info("No problematic IPs found")
            print("No problematic IPs found")
            return

        # Check against DB and get new IPs
        new_ips = check_and_store_ips(problematic_ips)

        # Print results for testing
        if new_ips:
            logger.info(f"New IPs detected: {json.dumps(new_ips)}")
            print("New IPs detected:")
            print(json.dumps(new_ips, indent=2))
            trigger_lambda(new_ips)  # Trigger Lambda with new IPs
        else:
            logger.info("No new IPs detected")
            print("No new IPs detected")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
