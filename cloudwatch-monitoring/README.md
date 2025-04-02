# CloudWatch Monitoring and Alarms

## Project Overview
This project establishes a comprehensive monitoring system for an EC2 instance running Apache and a PostgreSQL RDS database, using AWS CloudWatch. Key tasks include installing and configuring the CloudWatch agent to collect system metrics (e.g., disk, memory) and logs (e.g., Apache access, authentication), setting up alarms for performance and security events, building a dashboard for visualization, and integrating a custom metric to track active user sessions. A standout achievement was detecting and analyzing a dictionary attack via Apache log monitoring, showcasing practical application of security monitoring skills.

## Architecture Diagram
[Insert architecture diagram here, e.g., using draw.io]

## Setup Instructions
1. **Install and Configure CloudWatch Agent**:
   - On your EC2 instance (Ubuntu):
        wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
  
        sudo dpkg -i amazon-cloudwatch-agent.deb
     
        Run the configuration wizard:
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

        Apply the custom config and Start the agent:
        sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s

        Verify it’s running:
        sudo systemctl status amazon-cloudwatch-agent

        Troubleshoot via logs:
        tail -f /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log

2. **IAM Role Setup**:
   - Attach the CloudWatchAgentServerPolicy to the EC2 instance’s IAM role for metric and log publishing permissions.

3. **Configure Metrics and Logs**:
   - Metrics: Collects disk_used_percent and mem_used_percent every 60 seconds.
   - Logs: Monitors /var/log/auth.log, /var/log/apache2/access.log, /var/log/apache2/modsec_audit.log, and agent logs.

4. **Set Up Alarms (From the agent and metrics)**:
   - EC2 Alarms :
        •	High CPU Utilization Alarm: Set to detect potential overload on your EC2 instance.
        •	Network Traffic (In/Out) Alarms: Established to monitor for unusual activity, such as traffic spikes.
        •	StatusCheckFailed Alarm: Added to alert you to instance health issues requiring immediate attention.
        •	Memory Usage & Disk Space Alarms: Configured using the CloudWatch agent to track resource utilization.

   - RDS Alarms :   
        •	CPU Utilization Alarm: Set to monitor performance, similar to EC2.
        •	Freeable Memory Alarm: Created to warn of memory pressure that could lead to swapping.
        •	Database Connections Alarm: Added, though you’re unsure of the ideal threshold.
        •	Storage Space Alarm: Set to alert you when storage runs low.
        •	High IOPS Alarms (Read/Write): Configured with a baseline (e.g., ReadIOPS > 1000 for 5 minutes) to detect disk bottlenecks, but you’d like more clarification on this.

   - Apache Logs: 404 errors > 10 in 5 minutes (via Logs Insights).
   - Actions: Sending notifications to an SNS topic (e.g., email).

5. **Custom Metric for Active Sessions:**:
    - Started building a custom metric to track active sessions on your website.
    - Used PHP session monitoring and created an RDS table (sessions) to store session data (session ID, IP, and last activity timestamp).
    - Updated index.php to log sessions into an RDS table.
    - Used a [Python Script](./Code/active_sessions.py) to automate the sending to the agent and automated with cron (every 5 minutes). 

6. **Visualization through a custom Dashboard**:
    -    Widgets added:
        -    EC2 CPU Utilization
        -    Memory Utilization
        -    Disk Utilization
        -    RDS CPU Utilization
        -    Active Sessions (custom metric)
        -    Network Traffic (In/Out)
        -    Apache 404 Errors (via Logs Insights)
        -    Alarms
        -    Log insights (Querys are in the [Code](./Code) section)

## Notes
- i Keep adding more things to the dashboard for a better visualization of my ec2 server so by the time i release this i will have added more things
- i studied the anaomly detection but decided not to opt for it as i close my system when i finish studying on it and atleast it needs a continuous  14 days worth of data to be accurate 

## Lessons Learned
-  Agent Configuration: Extended CloudWatch beyond default metrics (e.g., CPU, network) to include memory and disk via the agent.
- Real-World Security: Caught a dictionary attack using log analysis, highlighting the power of proactive monitoring.
- Custom Metrics: Successfully integrated application data (active sessions) into CloudWatch with error handling and IAM roles.
- Alarm Tuning: Learned to set practical thresholds (e.g., IOPS, connections) and link them to SNS for instant alerts.
- Dashboard Visualization: Built a unified view of system health, enhancing operational awareness.