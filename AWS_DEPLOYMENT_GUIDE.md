# AWS Deployment Guide

## Prerequisites

1. **AWS Account** - Sign up at https://aws.amazon.com
2. **AWS CLI** - Download from https://aws.amazon.com/cli/
3. **Python 3.8+** - For running setup scripts
4. **Boto3** - `pip install boto3`

## Step 1: Configure AWS Credentials

### Option A: Using AWS CLI

```bash
aws configure
```

When prompted, enter:

- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `ap-south-1`)
- Default output format: `json`

### Option B: Using Environment Variables

```powershell
# On Windows PowerShell
$env:AWS_ACCESS_KEY_ID = "your-access-key-id"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
$env:AWS_DEFAULT_REGION = "ap-south-1"
```

### Option C: Using Credentials File

Create `~/.aws/credentials`:

```
[default]
aws_access_key_id = your-access-key-id
aws_secret_access_key = your-secret-access-key
```

Create `~/.aws/config`:

```
[default]
region = ap-south-1
output = json
```

## Step 2: Upload Datasets to S3

Before running the full setup, upload your training and test datasets:

```bash
# Create S3 bucket
aws s3 mb s3://mlops-water-potability-datasets --region ap-south-1

# Upload datasets
aws s3 cp Data-set/train_dataset.csv s3://mlops-water-potability-datasets/
aws s3 cp Data-set/test_dataset.csv s3://mlops-water-potability-datasets/

# Verify upload
aws s3 ls s3://mlops-water-potability-datasets/
```

## Step 3: Run AWS Setup Script

```bash
# Install required Python packages
pip install boto3

# Run setup script
python aws_setup.py
```

This script will:

1. ✅ Create S3 bucket with versioning
2. ✅ Create security group with proper inbound rules
3. ✅ Create EC2 key pair and save locally
4. ✅ Create IAM role for EC2→S3 access
5. ✅ Launch EC2 instance (Ubuntu 22.04 LTS)
6. ✅ Install Docker and Docker Compose
7. ✅ Clone the repository
8. ✅ Download datasets from S3
9. ✅ Start the application

## Step 4: Access Your Application

Once the script completes, you'll get:

```
✅ AWS Infrastructure Setup Complete!

S3 Bucket: mlops-water-potability-datasets
EC2 Instance ID: i-1234567890abcdef0
Public IP: 54.123.45.67
Key Pair: mlops-keypair.pem

Access your application:
  🌐 Web UI: http://54.123.45.67:8000
  📚 API Docs: http://54.123.45.67:8000/docs

SSH into instance:
  ssh -i mlops-keypair.pem ubuntu@54.123.45.67
```

## Step 5: SSH into Your Instance

```bash
# Connect to instance
ssh -i mlops-keypair.pem ubuntu@54.123.45.67

# View Docker containers
docker ps

# View application logs
docker logs mlops-water-potability-app

# Stop application
docker-compose down

# Start application
docker-compose up -d
```

## AWS Resources Created

| Resource       | Name                            | Description        |
| -------------- | ------------------------------- | ------------------ |
| S3 Bucket      | mlops-water-potability-datasets | Dataset storage    |
| EC2 Instance   | mlops-water-potability-server   | Application server |
| Security Group | mlops-security-group            | Firewall rules     |
| Key Pair       | mlops-keypair                   | SSH access         |
| IAM Role       | mlops-ec2-s3-role               | S3 permissions     |

## Cost Estimates (Monthly)

Using free tier eligible resources:

| Service        | Quantity    | Cost                   |
| -------------- | ----------- | ---------------------- |
| EC2 (t3.micro) | 1 instance  | Free (first 12 months) |
| S3 Storage     | < 5GB       | < $1                   |
| Data Transfer  | < 1GB/month | Free (same region)     |
| **Total**      |             | **Free or ~$1**        |

> Note: Costs may vary based on actual usage. Always monitor your AWS console.

## Monitoring Your Deployment

### View Instance Status

```bash
aws ec2 describe-instances \
  --instance-ids i-1234567890abcdef0 \
  --region ap-south-1
```

### View S3 Bucket Usage

```bash
aws s3 ls s3://mlops-water-potability-datasets/ --recursive --summarize
```

### CloudWatch Monitoring

1. Go to AWS Console → CloudWatch
2. Select your instance from the metrics
3. View CPU, network, and disk metrics

## Troubleshooting

### Can't connect to instance

```bash
# Check security group allows SSH (port 22)
aws ec2 describe-security-groups --group-names mlops-security-group

# Verify key pair permissions (Linux/Mac)
chmod 400 mlops-keypair.pem
```

### Application not responding on port 8000

```bash
# SSH into instance
ssh -i mlops-keypair.pem ubuntu@your-ip

# Check if Docker is running
docker ps

# View application logs
docker logs mlops-water-potability-app

# Check if port is listening
sudo netstat -tulpn | grep 8000
```

### S3 bucket access denied

```bash
# Verify IAM role is attached to instance
aws ec2 describe-instances --instance-ids i-xxx | grep IamInstanceProfile

# Check S3 bucket policy
aws s3api get-bucket-policy --bucket mlops-water-potability-datasets
```

### Out of free tier

```bash
# Stop instance (keeps data, saves costs)
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Start instance later
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# Terminate to delete
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

## Securing Your Deployment

### 1. Use HTTPS

```bash
# SSH into instance
ssh -i mlops-keypair.pem ubuntu@your-ip

# Install Certbot and Nginx
sudo apt-get install certbot python3-certbot-nginx nginx

# Get SSL certificate
sudo certbot certonly --standalone -d your-domain.com
```

### 2. Restrict SSH Access

```bash
# Allow SSH only from specific IP
aws ec2 authorize-security-group-ingress \
  --group-name mlops-security-group \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32 \
  --region ap-south-1
```

### 3. Enable VPC Flow Logs

```bash
# Create VPC flow log to monitor traffic
aws ec2 create-flow-logs \
  --resource-type NetworkInterface \
  --resource-ids eni-12345678 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name mlops-vpc-logs
```

## Cleanup (Delete Resources)

```bash
# Terminate EC2 instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Delete key pair
aws ec2 delete-key-pair --key-name mlops-keypair

# Delete security group (wait for instance to terminate first)
aws ec2 delete-security-group --group-name mlops-security-group

# Delete S3 bucket (must be empty first)
aws s3 rb s3://mlops-water-potability-datasets --force

# Delete IAM role
aws iam remove-role-from-instance-profile \
  --instance-profile-name mlops-ec2-profile \
  --role-name mlops-ec2-s3-role
aws iam delete-role --role-name mlops-ec2-s3-role
aws iam delete-instance-profile --instance-profile-name mlops-ec2-profile
```

## Next Steps: GitHub Actions CI/CD

Once your EC2 instance is running, set up GitHub Actions to:

1. Build Docker image on every push
2. Push to Docker Hub or AWS ECR
3. Automatically deploy new version to EC2
4. Run tests and security scans

See `.github/workflows` for CI/CD pipeline configuration.

## Support

- **AWS Documentation**: https://docs.aws.amazon.com/
- **EC2 Troubleshooting**: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/
- **S3 Documentation**: https://docs.aws.amazon.com/s3/
- **GitHub Issues**: https://github.com/TejasThange3/Mlops-Project/issues
