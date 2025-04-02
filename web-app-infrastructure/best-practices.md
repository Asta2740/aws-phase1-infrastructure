# Best Practices for This AWS Web App

Here’s what I learned about keeping this project secure, cost-effective, and fast—tips you can use too!

## Security Tips
- **Hide Credentials**: Don’t hardcode them like in [dbconfig.php](code/dbconfig.php). Use environment variables or AWS Secrets Manager (see [db-connection.php](code/db-connection.php)).
- **Control Traffic**: Security groups should only allow needed ports (e.g., 22 for SSH, 80 for HTTP, 5432 for RDS from EC2).
- **Validate Input**: Check form data in [index.php](code/index.php) to avoid junk or attacks.
- **IAM**: Set specific permissions if others join your project.

## Cost-Saving Tricks
- **Free Tier**: Use t2.micro (750 hours/month) and set AWS Budget alerts.
- **Warm Pools**: My ASG has 1 stopped instance—cheap and ready to go.
- **S3 for Files**: Move the video from EC2 to S3 to save resources.

## Performance Boosts
- **ELB**: Offloads SSL/TLS to keep EC2 light.
- **ASG**: Scales based on CPU or traffic—set your own rules!
- **RDS**: Add Multi-AZ later for reliability.

## Learn More
- [AWS EC2 Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)
- [RDS Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/)
- [ELB Basics](https://aws.amazon.com/elasticloadbalancing/)
- [AWS Best Practices](https://aws.amazon.com/architecture/well-architected/)