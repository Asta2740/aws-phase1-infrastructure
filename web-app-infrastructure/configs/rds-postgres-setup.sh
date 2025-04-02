#!/bin/bash
# Script to create an RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier database-1 \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 17.2 \
  --master-username postgres \
  --master-user-password yourpassword \  # Replace with secure password
  --allocated-storage 20 \
  --vpc-security-group-ids sg-0123456789abcdef0  # Replace with your SG ID
echo "RDS instance created!"