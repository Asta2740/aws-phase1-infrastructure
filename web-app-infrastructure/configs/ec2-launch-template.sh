#!/bin/bash
# Script to launch an EC2 instance (simplified for study purposes)
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \  # Replace with your AMI ID
  --instance-type t2.micro \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \  # Replace with your SG ID
  --subnet-id subnet-0123456789abcdef0 \  # Replace with your subnet ID
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'
echo "EC2 instance launched!"