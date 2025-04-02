# Web Application Infrastructure on AWS

This repository documents my personal journey of learning AWS Cloud Foundations while building a web application infrastructure. It covers key concepts, technical implementations, and best practices I explored over several days, The project focuses on launching a scalable, secure web application using AWS services like EC2, RDS, Elastic Load Balancing (ELB), Auto Scaling Groups (ASG), and more.

## Project Overview

The goal was to build a functional web application hosted on AWS, starting with basic cloud concepts and progressing to a full infrastructure setup. Key topics include:
- **Cloud Basics**: Understanding AWS’s market position, infrastructure (regions, AZs), and core services (EC2, S3, RDS).
- **EC2 Mastery**: Launching instances, configuring AMIs, and managing networking/security.
- **Scalability**: Implementing ELB and ASG for traffic distribution and auto-scaling.
- **Database Integration**: Setting up and connecting an RDS PostgreSQL instance.
- **Web App Deployment**: Hosting a PHP-based app with Apache on EC2.
- **Security & Cost Management**: Using IAM, security groups, and budget alerts.

## Key Concepts & Implementations

### Day 1-2: AWS Foundations
- **Concepts**: AWS’s 32% market share, 200+ services, global infrastructure (regions, AZs, edge locations).
- **Core Services**: EC2 (virtual servers), EBS (block storage), RDS (databases), S3 (object storage).
- **Implementation**: Created a free tier AWS account and explored the Management Console.
- **Takeaway**: AWS is ideal for infrastructure engineers due to its dominance and resources like AWS Skill Builder.

### Day 3: EC2 Deep Dive
- **What**: Launched my first EC2 instance (a virtual server).
- **Why**: EC2 replaces physical servers, letting me host my app in the cloud.
- **How**: Used the AWS Console to:
  1. Pick an Amazon Machine Image (AMI) like Amazon Linux.
  2. Chose a t2.micro instance (free tier eligible).
  3. Set up networking (VPC, security groups,key pairs) and storage (EBS).
- **Result**: A running server I could SSH into—my app’s foundation!

### Day 4-7: Enhancing EC2 and Storage
- **What**: Added features like Elastic IPs, security groups, and explored EBS snapshots.
- **Why**: To make my server reliable and secure.
- **How**: 
  - Assigned an Elastic IP (static public IP) for consistent access but i dropped it to stay without the free tier.
  - Configured security groups (firewalls) to allow specific traffic (e.g., SSH on port 22).
  - Learned EBS snapshots are backups of my storage.
  - Set a zero-spend budget to avoid charges.
- **Result**: A more robust EC2 setup with cost control.

### Networking & Troubleshooting
- **What**: Launched two instances (Ubuntu and Debian) and fixed a networking issue.
- **Why**: To test connectivity and learn troubleshooting.
- **How**: 
  - Placed both in the same subnet and tried pinging them.
  - Fixed a “no ping” issue by adding an ICMP rule to the security group.
  - Set up SSH access with key pairs and PuTTY (port 22 open).
- **Result**: Two instances talking to each other—networking basics nailed!

### Scaling with ELB and ASG
- **What**: Added an Application Load Balancer (ALB) and Auto Scaling Group (ASG).
- **Why**: To handle traffic spikes and keep my app available.
- **How**: 
  - Created an ALB to distribute traffic across instances.
  - Set up an ASG with a launch template to add/remove instances based on demand.
  - Added a warm pool (1 stopped instance) for quick scaling.
  - Installed Apache on EC2 and tweaked the index page.
- **Takeaway**: ELB + ASG = seamless scaling; secondary IPs unnecessary here.

### Adding a Database with RDS
- **What**: Launched a PostgreSQL RDS instance and built a PHP web app.
- **Why**: To store and manage app data easily.
- **How**: 
  - Created a free tier PostgreSQL 17.2 instance.
  - Connected it to EC2 in the same VPC, using a security group for port 5432.
  - Built a table (`entries`) and a PHP app to:
    - Submit name/quota data.
    - Display entries with a delete option.
    - Play a video on submit (stored on EC2).
  - Code is in [index.php](code/index.php), [dbconfig.php](code/dbconfig.php), and [db-connection.php](code/db-connection.php).
- **Result**: A working web app with a database backend!.



## Architecture Diagram

(Placeholder: See [web-app-architecture.png](diagrams/web-app-architecture.png) for a visual of EC2, ALB, ASG, and RDS setup.)

# Try It Yourself

1. **Launch an EC2 Instance**: Use [ec2-launch-template.sh](configs/ec2-launch-template.sh).
2. **Set Up RDS**: Run [rds-postgres-setup.sh](configs/rds-postgres-setup.sh).
3. **Configure Apache**: Apply [apache-config.conf](configs/apache-config.conf).
4. **Deploy the App**: Upload [index.php](code/index.php), [dbconfig.php](code/dbconfig.php), and [db-connection.php](code/db-connection.php).

## Why It Matters

This setup is like a mini social media platform—scalable, secure, and database-driven. It’s a practical intro to AWS for anyone starting out.



## Notes :
 - i added the index.php you will find a strang thing which is a hard coded password to enter the page i just did that to mess with the hackers as the moment i launched my intsance i found way too many directory attack on the site so i just added this to mess with the people that try to access it along with some security measrues that you will find in one of the subfolders of the repo
 - At the end i disabled the ELB and Elastic ip to prevent going above the free tier i am just learning and doing practicale work so i can gain the knowledge and experince
 - See [best-practices.md](best-practices.md) for tips on security, cost, and performance!