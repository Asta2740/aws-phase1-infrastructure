# Best Practices & Observations

This file summarizes key takeaways from my Network ACL project, focusing on security, cost, and performance.

## Security Considerations
- **Granular Rules**: Network ACLs block at the subnet level, so I ensured rules were specific (e.g., `/32` CIDR for IPs).
- **IAM Least Privilege**: Policies are scoped to specific resources (e.g., log groups) to minimize risk.
- **Dynamic Threats**: Since IPs are dynamic, I treat this as a detection tool, not a permanent blocklist.

## Cost Optimization
- **Network ACLs vs. WAF**: Chose ACLs to stay within the free tier, avoiding ALB costs required for WAF.
- **Rule Management**: Need to add cleanup logic to avoid hitting the 20-rule default limit (or request an increase).

## Performance Tuning
- **Hourly Checks**: Scheduled `check_ips.py` via crontab for timely updates without overloading resources.
- **Lambda Efficiency**: Kept the function lightweight, processing only new IPs to minimize execution time.

## Areas for Improvement
- **Rule Cleanup**: Add logic to remove old deny rules from the NACL.
- **Monitoring**: Set up CloudWatch alarms for Lambda errors or timeouts.
- **Testing**: Simulate edge cases (e.g., no IPs, NACL full) to ensure robustness.

## Resources
- [AWS Network ACLs Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)