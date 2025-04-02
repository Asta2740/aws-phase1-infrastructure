# AWS S3 Exploration

## Project Overview
This project involves exploring AWS S3 concepts and testing the hosting of a video using pre-signed URLs. After evaluation, I opted to keep the video on EC2 for cost reasons.

## Setup Instructions
1. **Create an S3 Bucket**:
   - Name: `my-video-bucket`
   - Upload a sample video (e.g., `sample.mp4`).

2. **Generate Pre-signed URL**:
   - Use the AWS CLI or SDK to create a temporary URL:
     ```bash
     aws s3 presign s3://my-video-bucket/sample.mp4 --expires-in 3600

3. **Generate Pre-signed URL**:
   - Access the video via the pre-signed URL in a browser.
   - Compare with EC2 hosting performance and cost.

## Testing and Validation
   - Uploaded sample.mp4 to S3 and generated a pre-signed URL.
   - Successfully accessed the video via the URL.
   - Decided to host on EC2 due to lower cost for my use case.

## Lessons Learned
   - Understood S3 storage classes (e.g., Standard, Intelligent-Tiering) and their use cases.
   - Learned to secure S3 objects with pre-signed URLs for temporary access.
   - Evaluated trade-offs between S3 and EC2 hosting.