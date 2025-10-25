# GitHub Actions CI/CD Setup Guide

## Overview

This project uses GitHub Actions for:

1. **Building** Docker images on every push
2. **Testing** the application automatically
3. **Deploying** to EC2 instance
4. **Training** ML models in the pipeline
5. **Notifying** Slack with deployment status

## Workflows

### 1. `deploy.yml` - Build & Deploy to EC2

**Triggers:** Push to `main` or `develop` branch

**Steps:**

1. Check out code
2. Install Python dependencies
3. Run tests
4. Build Docker image
5. Push to GitHub Container Registry (ghcr.io)
6. Deploy to EC2 instance
7. Verify deployment health
8. Send Slack notification

### 2. `mlops-pipeline.yml` - ML Training Pipeline

**Triggers:** Push to `main/develop`, PRs, or daily at 2 AM UTC

**Steps:**

1. Validate training/test datasets
2. Run DVC pipeline (preprocessing → training → evaluation)
3. Generate metrics
4. Run unit tests with coverage
5. Test API endpoints
6. Build Docker image
7. Send summary to GitHub

## Setting Up GitHub Actions

### Step 1: Add Repository Secrets

Go to: **Settings → Secrets and variables → Actions**

Click "New repository secret" and add these:

#### For EC2 Deployment:

**`EC2_HOST`**

```
Value: Your EC2 instance public IP (e.g., 54.123.45.67)
```

**`EC2_PRIVATE_KEY`**

```
Value: Content of your mlops-keypair.pem file
```

To get the private key content:

```bash
cat mlops-keypair.pem
# Copy the entire output including -----BEGIN PRIVATE KEY----- lines
```

**`SLACK_WEBHOOK_URL`** (Optional, for notifications)

```
Value: Your Slack webhook URL
```

To get Slack webhook:

1. Go to https://api.slack.com/apps
2. Create New App or select existing
3. Go to "Incoming Webhooks"
4. Click "Add New Webhook to Workspace"
5. Select channel and authorize
6. Copy the webhook URL

#### For Docker Registry:

The `GITHUB_TOKEN` is automatically available. No additional setup needed.

### Step 2: Verify Secrets Setup

```bash
# Check secrets (from your local machine)
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/TejasThange3/Mlops-Project/actions/secrets
```

### Step 3: Test the Workflow

```bash
# Make a small change and push
git add .
git commit -m "Test GitHub Actions workflow"
git push origin main
```

Go to: **GitHub repo → Actions tab** to see workflow running.

## Workflow Files Structure

```
.github/
└── workflows/
    ├── deploy.yml              # Build & Deploy to EC2
    └── mlops-pipeline.yml      # ML Pipeline & Testing
```

## Manual Workflow Triggers

### Trigger workflow via GitHub CLI:

```bash
# Install GitHub CLI
gh auth login

# Trigger workflow
gh workflow run deploy.yml --ref main

# View workflow status
gh workflow view
```

### Via GitHub UI:

1. Go to **Actions** tab
2. Select workflow
3. Click "Run workflow"
4. Choose branch and click "Run workflow"

## Understanding Workflow Results

### Successful Workflow

```
✅ validate-data    - Data validation passed
✅ train-model      - Model trained successfully
✅ test             - All tests passed
✅ api-test         - API responding correctly
✅ build-docker     - Docker image built and pushed
✅ deploy           - Deployed to EC2
```

### Failed Workflow

- Check the failed job logs in GitHub Actions
- Common issues:
  - EC2 instance not running
  - EC2_PRIVATE_KEY secret incorrect
  - EC2_HOST secret not set
  - Port 8000 already in use on EC2

## Monitoring Deployments

### From GitHub:

1. Go to **Actions** tab
2. Click on latest workflow run
3. View logs for each job
4. Download artifacts (metrics, test results)

### From EC2:

```bash
# SSH into instance
ssh -i mlops-keypair.pem ubuntu@your-ec2-ip

# View logs
docker logs mlops-water-potability-app

# Check running containers
docker ps

# View metrics
curl http://localhost:8000/metrics
```

## Advanced Configuration

### Modify Deployment Branch

In `deploy.yml`, change:

```yaml
on:
  push:
    branches:
      - main # Change to your branch
      - develop
```

### Add Approval Steps

Add to `deploy.yml` before deployment:

```yaml
deploy:
  needs: build
  environment:
    name: production
    url: http://${{ secrets.EC2_HOST }}:8000
```

Then in GitHub: Settings → Environments → Set required reviewers

### Add Performance Benchmarks

Extend `mlops-pipeline.yml`:

```yaml
- name: Performance Benchmark
  run: |
    time python src/predict_test.py
    # Track metrics over time
```

### Add Code Quality Checks

```yaml
- name: Run Linting
  run: |
    pip install flake8 black
    black --check src/
    flake8 src/
```

## Troubleshooting

### Workflow not triggering

```bash
# Check GitHub Actions is enabled
# Settings → Actions → General → Allow all actions

# Verify branch protection rules don't block
# Settings → Branches → Branch protection rules
```

### Deployment fails

```bash
# Check EC2 is running
aws ec2 describe-instances --instance-ids i-xxx

# Check security group allows port 8000
aws ec2 describe-security-groups --group-names mlops-security-group

# SSH and check Docker
ssh -i mlops-keypair.pem ubuntu@your-ip
docker ps
docker logs mlops-water-potability-app
```

### Docker image push fails

```bash
# Check GitHub token has packages:write permission
# Settings → Developer settings → Personal access tokens
```

### Slack notification not received

```bash
# Verify webhook URL is correct
# Check Slack app has permission to post

# Test webhook manually
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  YOUR_WEBHOOK_URL
```

## Security Best Practices

1. **Never commit secrets** - Always use GitHub Secrets
2. **Rotate keys regularly**:
   ```bash
   # Generate new EC2 keypair
   aws ec2 create-key-pair --key-name mlops-keypair-v2
   ```
3. **Use branch protection** - Require PR reviews before merge
4. **Enable CODEOWNERS** - Require review from specific users
5. **Audit logs** - Check GitHub audit log regularly

## Performance Optimization

### Cache Docker layers

```yaml
- uses: docker/setup-buildx-action@v2
- uses: docker/build-push-action@v4
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Parallel jobs

The workflow already runs `test` and `api-test` in parallel

### Skip expensive steps for PRs

```yaml
if: github.event_name == 'push'
```

## Cost Considerations

- **GitHub Actions**: First 2,000 minutes/month free
- **EC2**: Free tier (12 months) with t3.micro
- **Data Transfer**: Free within same region

## Next Steps

1. ✅ Set up EC2 instance using `aws_setup.py`
2. ✅ Configure GitHub Secrets (EC2_HOST, EC2_PRIVATE_KEY)
3. ✅ Push code to GitHub
4. ✅ Monitor first deployment in Actions tab
5. ✅ Verify application is running on EC2
6. ✅ Set up Slack notifications (optional)

## Support

- **GitHub Actions Docs**: https://docs.github.com/actions
- **GitHub CLI**: https://cli.github.com/
- **Troubleshooting**: https://docs.github.com/actions/troubleshooting
