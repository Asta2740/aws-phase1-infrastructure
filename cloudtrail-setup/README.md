# AWS CloudTrail Setup

## Project Overview
This project enables a management trail in AWS CloudTrail to log API activities across my AWS environment for auditing and monitoring purposes.

## Setup Instructions
1. **Create a CloudTrail Trail**:
   - Name: `management-trail`
   - Enable for all management events.
   - Store logs in an S3 bucket (e.g., `cloudtrail-logs-<account-id>`).

2. **Verify Logging**:
   - Perform AWS actions (e.g., launch an EC2 instance).
   - Check the S3 bucket for CloudTrail log files.

## Testing and Validation
- Created the `management-trail` and linked it to an S3 bucket.
- Launched an EC2 instance and confirmed the action was logged in S3.
- Reviewed logs to verify API call details (e.g., user, timestamp).

## Lessons Learned
- Gained visibility into AWS environment changes through audit logs.
- Understood the importance of CloudTrail for security and compliance.
- Prepared for future troubleshooting and auditing needs.