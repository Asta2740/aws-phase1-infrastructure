# GitHub Documentation for Phase 1: Infrastructure Engineering – Cloud Foundations

Welcome to my AWS learning journey! This repository documents my hands-on projects and progress during **Phase 1: Infrastructure Engineering – Cloud Foundations**, spanning from **March 3, 2025**, to **March 29, 2025**. As an aspiring infrastructure engineer with a future goal of transitioning into security engineering, I’ve focused on mastering foundational AWS services, automation, monitoring, and security practices. This repository captures my work, organized chronologically to reflect my learning progression, and includes detailed project documentation, code snippets, and key takeaways.

## Introduction

Starting with no prior cloud experience, I embarked on this journey on March 3, 2025, to build a strong foundation in AWS infrastructure engineering. Phase 1 emphasizes hands-on experience with core AWS services—such as EC2, RDS, S3, Lambda, Step Functions, CloudWatch, and Network ACLs—while introducing automation, monitoring, and security concepts. Each project builds on the last, showcasing my growing skills and problem-solving abilities. This repository serves as both a personal record and a resource for others exploring AWS.

## Repository Structure

- **`README.md`**: This file provides an overview, timeline, and links to all projects.
- **Project Folders**: Each major project has its own folder (e.g., `serverless-portfolio/`, `ec2-automation/`) containing:
  - A `README.md` with project details, setup instructions, code snippets, testing steps, and lessons learned.
  - Relevant code files (e.g., Python scripts, JSON configurations).

## Projects

Below are the key projects completed during Phase 1, each linked to its detailed documentation:

1. **[Serverless Portfolio Site](./serverless-portfolio/README.md)**  
   - **Description**: Built a static website hosted on S3 with HTTPS via CloudFront, featuring a form that submits data to Lambda via API Gateway and stores it in S3.
   - **Key Services**: S3, CloudFront, Lambda, API Gateway.
   - **Skills Learned**: Serverless architecture, static hosting, API integration.

2. **[EC2 Automation with Lambda and Step Functions](./ec2-automation/README.md)**  
   - **Description**: Automated EC2 instance restarts based on high CPU utilization using Lambda and Step Functions, triggered by a CloudWatch alarm.
   - **Key Services**: EC2, Lambda, Step Functions, CloudWatch.
   - **Skills Learned**: Event-driven automation, orchestration.

3. **[CloudWatch Monitoring and Alarms](./cloudwatch-monitoring/README.md)**  
   - **Description**: Configured comprehensive monitoring for EC2 and Apache logs with CloudWatch, including custom queries and SNS alarms for 404 spikes.
   - **Key Services**: CloudWatch, EC2, SNS.
   - **Skills Learned**: Log analysis, alerting, dashboard creation.

4. **[Security Enhancements with Network ACLs](./security-enhancements/README.md)**  
   - **Description**: Implemented IP blocking using Network ACLs and Lambda, driven by EC2 log analysis of Apache errors and SSH attempts.
   - **Key Services**: EC2, Lambda, Network ACLs, RDS.
   - **Skills Learned**: Security automation, threat detection.

5. **[AWS S3 Exploration](./s3-exploration/README.md)**  
   - **Description**: Explored S3 concepts and tested hosting a video with pre-signed URLs, opting to keep it on EC2 for now.
   - **Key Services**: S3.
   - **Skills Learned**: Storage management, access control.

6. **[AWS CloudTrail Setup](./cloudtrail-setup/README.md)**  
   - **Description**: Enabled a management trail to log API activities for auditing and monitoring.
   - **Key Services**: CloudTrail.
   - **Skills Learned**: Audit logging, environment visibility.

## Key Learnings

Through these projects, I’ve developed practical skills in:
- **Core AWS Services**: Provisioning and managing EC2, RDS, S3, Lambda, and more.
- **Monitoring**: Setting up CloudWatch for logs, metrics, and alarms.
- **Automation**: Using Lambda and Step Functions for event-driven tasks.
- **Security**: Implementing threat detection and response with Network ACLs and log analysis.
- **Problem-Solving**: Debugging real-world issues like dictionary attacks and Lambda errors.

These skills lay a solid groundwork for advancing to Phase 2, focusing on networking, advanced automation, and containerization.

## Timeline

Here’s a chronological overview of my progress from March 3 to March 29, 2025:

- **March 3**: Researched cloud platforms and chose AWS.
- **March 4**: Created an AWS account and watched an introductory video.
- **March 5**: Launched my first EC2 instance and explored the AWS Management Console.
- **March 6**: Deepened EC2 knowledge (AMIs, instance types).
- **March 7**: Set up RDS and connected it to EC2.
- **March 8**: Built a simple web app with EC2 and RDS.
- **March 9**: Configured CloudWatch to monitor EC2 and RDS.
- **March 10**: Explored custom metrics (e.g., active sessions).
- **March 11**: Automated EC2 restarts with Lambda and Step Functions.
- **March 12**: Began security enhancements with Network ACLs and Lambda.
- **March 13**: Studied S3 and security best practices.
- **March 14**: Started the serverless portfolio site with S3, CloudFront, Lambda, and API Gateway.
- **March 15-23**: Continued refining projects, integrating CloudWatch monitoring and security scripts.
- **March 24**: Implemented IP blocking for Apache errors using Network ACLs.
- **March 25**: Set up CloudTrail and blocked SSH login attempts.
- **March 26**: Enhanced monitoring with CloudWatch Logs Insights and detected a dictionary attack.
- **March 27**: Explored AWS Amplify and GitHub for the portfolio site (incomplete).
- **March 28**: Took a break; no progress.
- **March 29**: Secured Python scripts with environment variables and studied S3.

## Next Steps

With Phase 1 complete, I plan to:
- Finish deploying the serverless portfolio site with AWS Amplify.
- Begin Phase 2, diving into VPC networking, advanced automation, and containerization (e.g., ECS, Docker).
- Explore certifications like AWS Cloud Practitioner to solidify my knowledge.