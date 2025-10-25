#!/usr/bin/env python3
"""
AWS Infrastructure Setup Script
Creates S3 bucket, EC2 instance, and configures necessary resources
"""

import boto3
import json
import sys
from botocore.exceptions import ClientError

# Configuration
REGION = "ap-south-1"  # Change to your preferred region
BUCKET_NAME = "mlops-water-potability-datasets"
INSTANCE_TYPE = "t3.micro"  # Free tier eligible
INSTANCE_NAME = "mlops-water-potability-server"
SECURITY_GROUP_NAME = "mlops-security-group"
KEY_PAIR_NAME = "mlops-keypair"
AVAILABILITY_ZONE = f"{REGION}a"

# Initialize AWS clients
s3_client = boto3.client('s3', region_name=REGION)
ec2_client = boto3.client('ec2', region_name=REGION)
iam_client = boto3.client('iam', region_name=REGION)

def create_s3_bucket():
    """Create S3 bucket for datasets"""
    print(f"\n📦 Creating S3 bucket: {BUCKET_NAME}")
    try:
        if REGION == 'us-east-1':
            s3_client.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3_client.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={'LocationConstraint': REGION}
            )
        print(f"✅ S3 bucket created: {BUCKET_NAME}")
        
        # Enable versioning
        s3_client.put_bucket_versioning(
            Bucket=BUCKET_NAME,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print("✅ Versioning enabled for S3 bucket")
        
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"⚠️  Bucket already exists: {BUCKET_NAME}")
            return True
        elif e.response['Error']['Code'] == 'BucketAlreadyExists':
            print(f"❌ Bucket already exists (owned by another account): {BUCKET_NAME}")
            return False
        else:
            print(f"❌ Error creating bucket: {e}")
            return False

def create_security_group():
    """Create security group for EC2 instance"""
    print(f"\n🔐 Creating security group: {SECURITY_GROUP_NAME}")
    try:
        response = ec2_client.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description='Security group for MLOps Water Potability application',
            Region=REGION
        )
        sg_id = response['GroupId']
        print(f"✅ Security group created: {sg_id}")
        
        # Add inbound rules
        # SSH access
        ec2_client.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'SSH access'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTP access'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTPS access'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 8000,
                    'ToPort': 8000,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Application API'}]
                }
            ]
        )
        print("✅ Inbound rules added (SSH, HTTP, HTTPS, Port 8000)")
        return sg_id
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidGroup.Duplicate':
            # Get existing security group
            response = ec2_client.describe_security_groups(GroupNames=[SECURITY_GROUP_NAME])
            sg_id = response['SecurityGroups'][0]['GroupId']
            print(f"⚠️  Security group already exists: {sg_id}")
            return sg_id
        else:
            print(f"❌ Error creating security group: {e}")
            return None

def create_key_pair():
    """Create key pair for EC2 access"""
    print(f"\n🔑 Creating key pair: {KEY_PAIR_NAME}")
    try:
        response = ec2_client.create_key_pair(KeyName=KEY_PAIR_NAME)
        # Save private key
        with open(f'{KEY_PAIR_NAME}.pem', 'w') as f:
            f.write(response['KeyMaterial'])
        print(f"✅ Key pair created and saved: {KEY_PAIR_NAME}.pem")
        print(f"⚠️  IMPORTANT: Keep {KEY_PAIR_NAME}.pem safe. You'll need it to SSH into the instance.")
        return KEY_PAIR_NAME
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
            print(f"⚠️  Key pair already exists: {KEY_PAIR_NAME}")
            return KEY_PAIR_NAME
        else:
            print(f"❌ Error creating key pair: {e}")
            return None

def create_iam_role():
    """Create IAM role for EC2 to access S3"""
    print(f"\n👤 Creating IAM role for S3 access")
    try:
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "ec2.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        response = iam_client.create_role(
            RoleName='mlops-ec2-s3-role',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for EC2 to access S3 bucket'
        )
        role_arn = response['Role']['Arn']
        print(f"✅ IAM role created: {role_arn}")
        
        # Attach S3 policy
        s3_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{BUCKET_NAME}",
                        f"arn:aws:s3:::{BUCKET_NAME}/*"
                    ]
                }
            ]
        }
        
        iam_client.put_role_policy(
            RoleName='mlops-ec2-s3-role',
            PolicyName='mlops-s3-access',
            PolicyDocument=json.dumps(s3_policy)
        )
        print("✅ S3 access policy attached")
        
        # Create instance profile
        iam_client.create_instance_profile(InstanceProfileName='mlops-ec2-profile')
        iam_client.add_role_to_instance_profile(
            InstanceProfileName='mlops-ec2-profile',
            RoleName='mlops-ec2-s3-role'
        )
        print("✅ Instance profile created")
        
        return role_arn
    except ClientError as e:
        if 'already exists' in str(e):
            print(f"⚠️  IAM role already exists")
            return f"arn:aws:iam::{boto3.client('sts').get_caller_identity()['Account']}:role/mlops-ec2-s3-role"
        else:
            print(f"❌ Error creating IAM role: {e}")
            return None

def create_ec2_instance():
    """Create EC2 instance"""
    print(f"\n🖥️  Creating EC2 instance: {INSTANCE_NAME}")
    
    # Get latest Ubuntu 22.04 LTS AMI
    ec2_resource = boto3.resource('ec2', region_name=REGION)
    images = ec2_resource.images.filter(
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
            {'Name': 'root-device-type', 'Values': ['ebs']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    
    ami_id = sorted(images, key=lambda x: x.creation_date)[-1].id
    print(f"📍 Using AMI: {ami_id} (Ubuntu 22.04 LTS)")
    
    # User data script to install Docker and pull application
    user_data_script = f"""#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io docker-compose git curl

# Start Docker
systemctl start docker
systemctl enable docker

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Clone the repository
cd /home/ubuntu
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project

# Download datasets from S3
mkdir -p data Data-set
aws s3 cp s3://{BUCKET_NAME}/train_dataset.csv Data-set/
aws s3 cp s3://{BUCKET_NAME}/test_dataset.csv Data-set/

# Pull Docker image
docker pull mlops-water-potability:latest

# Start application
docker-compose up -d

echo "✅ Application started successfully!"
"""
    
    try:
        response = ec2_client.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_PAIR_NAME,
            SecurityGroupIds=['sg-12345678'],  # Will be replaced with actual SG ID
            UserData=user_data_script,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': INSTANCE_NAME},
                        {'Key': 'Project', 'Value': 'MLOps-Water-Potability'}
                    ]
                }
            ],
            IamInstanceProfile={'Name': 'mlops-ec2-profile'},
            Monitoring={'Enabled': True}
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"✅ EC2 instance created: {instance_id}")
        print(f"⏳ Instance is starting... (this may take a few minutes)")
        
        # Wait for instance to start
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get instance details
        instance = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(f"✅ Instance is running!")
        print(f"📍 Public IP: {public_ip}")
        print(f"🌐 Access application at: http://{public_ip}:8000")
        
        return instance_id, public_ip
    except ClientError as e:
        print(f"❌ Error creating EC2 instance: {e}")
        return None, None

def main():
    """Main setup function"""
    print("=" * 60)
    print("AWS Infrastructure Setup for MLOps Water Potability")
    print("=" * 60)
    print(f"Region: {REGION}")
    print(f"S3 Bucket: {BUCKET_NAME}")
    print(f"EC2 Instance: {INSTANCE_NAME} ({INSTANCE_TYPE})")
    print("=" * 60)
    
    # Create S3 bucket
    if not create_s3_bucket():
        print("\n❌ Failed to create S3 bucket. Aborting.")
        sys.exit(1)
    
    # Create security group
    sg_id = create_security_group()
    if not sg_id:
        print("\n❌ Failed to create security group. Aborting.")
        sys.exit(1)
    
    # Create key pair
    key_name = create_key_pair()
    if not key_name:
        print("\n❌ Failed to create key pair. Aborting.")
        sys.exit(1)
    
    # Create IAM role
    role_arn = create_iam_role()
    if not role_arn:
        print("\n❌ Failed to create IAM role. Aborting.")
        sys.exit(1)
    
    # Create EC2 instance
    instance_id, public_ip = create_ec2_instance()
    if not instance_id:
        print("\n❌ Failed to create EC2 instance. Aborting.")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ AWS Infrastructure Setup Complete!")
    print("=" * 60)
    print(f"\nS3 Bucket: {BUCKET_NAME}")
    print(f"EC2 Instance ID: {instance_id}")
    print(f"Public IP: {public_ip}")
    print(f"Key Pair: {KEY_PAIR_NAME}.pem")
    print(f"\nAccess your application:")
    print(f"  🌐 Web UI: http://{public_ip}:8000")
    print(f"  📚 API Docs: http://{public_ip}:8000/docs")
    print(f"\nSSH into instance:")
    print(f"  ssh -i {KEY_PAIR_NAME}.pem ubuntu@{public_ip}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
