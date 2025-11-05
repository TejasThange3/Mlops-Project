# 🌊 Water Potability Prediction - MLOps Project

An end-to-end machine learning operations (MLOps) project that predicts water potability with **containerization**, **cloud deployment**, and **automated CI/CD**. This demonstrates enterprise-grade ML practices.

## 🎯 Project Highlights

- ✅ **Local Development** - DVC pipeline, FastAPI API, Jupyter notebooks
- ✅ **Containerization** - Docker & Docker Compose
- ✅ **Cloud Deployment** - AWS (S3, EC2, IAM)
- ✅ **Automated CI/CD** - GitHub Actions workflow
- ✅ **Model Versioning** - Track multiple model versions
- ✅ **API Documentation** - Interactive Swagger UI
- ✅ **Monitoring & Logging** - Production-ready tracking

## 📋 Quick Navigation

| Document                                                 | Purpose                  |
| -------------------------------------------------------- | ------------------------ |
| [QUICKSTART.md](./QUICKSTART.md)                         | Get started in 5 minutes |
| [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)                     | Containerization guide   |
| [AWS_DEPLOYMENT_GUIDE.md](./AWS_DEPLOYMENT_GUIDE.md)     | Cloud deployment         |
| [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)     | CI/CD pipeline           |
| [MODEL_VERSIONING_GUIDE.md](./MODEL_VERSIONING_GUIDE.md) | Model versioning         |
| [SIMPLE_COMMANDS.txt](./SIMPLE_COMMANDS.txt)             | Quick command reference  |

## 🏗️ Project Architecture

```
Developer Machine (Local)
        ↓
  GitHub Repository
        ↓
  GitHub Actions (Build, Test, Deploy)
        ↓
  AWS Infrastructure
        ├─ S3 Bucket (Datasets)
        └─ EC2 Instance
           └─ Docker Container
              └─ FastAPI Application
```

## 🚀 Getting Started

### Option 1: Local Development (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python -m uvicorn main:app --reload

# 4. Open browser
# Visit http://localhost:8000
```

### Option 2: Docker (10 minutes)

```bash
# 1. Build image
docker build -t mlops-water-potability:latest .

# 2. Start services
docker-compose up -d

# 3. Access application
# Visit http://localhost:8000
```

### Option 3: AWS Cloud (30 minutes)

```bash
# 1. Configure AWS
aws configure

# 2. Run setup script
pip install boto3
python aws_setup.py

# 3. Access application
# Visit http://EC2_PUBLIC_IP:8000
```

## 📊 Project Structure

```
Mlops-Project/
├── .github/workflows/
│   ├── deploy.yml                 # Docker build & EC2 deploy
│   └── mlops-pipeline.yml         # Training & testing pipeline
├── src/
│   ├── preprocess_presplit.py     # Data preprocessing
│   ├── train_ensemble.py          # Model training
│   ├── evaluate.py                # Metrics & evaluation
│   ├── predict_test.py            # Batch predictions
│   └── model_manager.py           # Version management
├── models/
│   ├── model.joblib               # Current model
│   ├── scaler.joblib              # Feature scaler
│   └── versions/                  # Model version history
├── static/
│   ├── index.html                 # Web interface
│   ├── css/style.css              # Styling
│   └── js/app.js                  # Frontend logic
├── data/
│   ├── train.csv                  # Training data
│   └── test.csv                   # Test data
├── main.py                        # FastAPI application
├── docker-compose.yml             # Container orchestration
├── Dockerfile                     # Container specification
├── dvc.yaml                       # ML pipeline
├── params.yaml                    # Hyperparameters
├── requirements.txt               # Python dependencies
├── aws_setup.py                   # AWS infrastructure setup
└── README.md                      # This file
```

## 🔄 Workflow

### 1. Development Phase

```bash
# Make changes locally
git add .
git commit -m "Add new feature"
git push origin main
```

### 2. GitHub Actions Phase

✅ **Automatically runs:**

- Data validation
- Model training (DVC pipeline)
- Unit tests
- API endpoint tests
- Docker image build
- Container push to registry

### 3. Deployment Phase

✅ **Automatically deploys to:**

- EC2 instance
- Updates running containers
- Health checks
- Slack notifications

### 4. Production Phase

✅ **Application serves:**

- Web UI at root path
- API at `/predict` endpoint
- Swagger docs at `/docs`
- Health check at `/health`

## 🌐 API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pH": 7.5,
    "Hardness": 150,
    "Solids": 10000,
    "Chloramines": 5.5,
    "Sulfate": 200,
    "Conductivity": 500,
    "Organic_carbon": 10,
    "Trihalomethanes": 100,
    "Turbidity": 3.5
  }'

# Interactive documentation
# Visit http://localhost:8000/docs
```

## 📈 Model Versioning

The system supports multiple model versions:

```bash
# View available versions
curl http://localhost:8000/models/versions

# Switch model version
curl -X POST http://localhost:8000/models/switch \
  -H "Content-Type: application/json" \
  -d '{"version": "V1"}'

# Get current model info
curl http://localhost:8000/models/current

# Retrain with user feedback
curl -X POST http://localhost:8000/retrain \
  -H "Content-Type: application/json" \
  -d '{
    "water_quality": {...},
    "actual_potability": 1
  }'
```

## 🐳 Docker & Containerization

Complete containerization with:

- **FastAPI** application service
- **PostgreSQL** database
- **Redis** cache layer
- Health checks for all services
- Persistent volumes for data

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# View metrics
docker stats
```

See [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) for details.

## ☁️ AWS Cloud Deployment

Fully automated AWS setup:

- S3 bucket for datasets
- EC2 instance (Ubuntu 22.04)
- Security groups & IAM roles
- Auto-deployment script

```bash
# One-command deployment
python aws_setup.py

# Access your deployed app
# http://EC2_PUBLIC_IP:8000
```

See [AWS_DEPLOYMENT_GUIDE.md](./AWS_DEPLOYMENT_GUIDE.md) for details.

## 🔄 GitHub Actions CI/CD

Two automated workflows:

### 1. `deploy.yml` - Build & Deploy

- Triggers on push to main/develop
- Builds Docker image
- Runs tests
- Deploys to EC2
- Sends Slack notifications

### 2. `mlops-pipeline.yml` - ML Training

- Validates datasets
- Runs DVC pipeline
- Trains models
- Evaluates performance
- Generates metrics

**Setup:**

1. Add GitHub Secrets: `EC2_HOST`, `EC2_PRIVATE_KEY`
2. Push to main branch
3. Watch Actions tab for automation

See [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md) for details.

## 📊 Metrics & Monitoring

The model achieves:

- **Training Accuracy**: 84.39%
- **ROC-AUC**: 92.77%
- **Precision**: 86.53%
- **Recall**: 71.06%
- **F1-Score**: 78.04%

View metrics:

```bash
# DVC metrics
dvc metrics show

# JSON output
cat metrics.json | python -m json.tool
```

## 🛠️ Technology Stack

| Category             | Tools                                |
| -------------------- | ------------------------------------ |
| **ML**               | scikit-learn, XGBoost, pandas, numpy |
| **API**              | FastAPI, Pydantic, Uvicorn           |
| **Containerization** | Docker, Docker Compose               |
| **Cloud**            | AWS (S3, EC2, IAM)                   |
| **Pipeline**         | DVC, Git                             |
| **CI/CD**            | GitHub Actions                       |
| **Frontend**         | HTML, CSS, JavaScript                |
| **Database**         | PostgreSQL, Redis                    |

## 🔐 Security Features

- ✅ API request validation (Pydantic)
- ✅ Security groups restrict access
- ✅ IAM roles follow least privilege
- ✅ Environment variables for secrets
- ✅ Health checks for liveness/readiness
- ✅ CORS configured for API

## 📈 Scaling Considerations

The architecture supports:

- **Horizontal scaling** - Add more EC2 instances
- **Load balancing** - AWS ALB/NLB
- **Auto-scaling** - Based on CPU/memory
- **Database replication** - RDS multi-AZ
- **CDN** - CloudFront for static content

## 🐛 Troubleshooting

Common issues and solutions:

### Docker container won't start

```bash
docker-compose logs app
# Check for port conflicts or memory issues
```

### API not responding

```bash
# Check health endpoint
curl http://localhost:8000/health

# View application logs
docker logs mlops-water-potability-app
```

### EC2 deployment failed

```bash
# SSH into instance
ssh -i mlops-keypair.pem ubuntu@EC2_IP

# Check Docker status
docker ps
docker logs mlops-water-potability-app
```

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for comprehensive debugging guide.

## 📚 Learning Resources

- [DVC Documentation](https://dvc.org/doc)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Docker Getting Started](https://docs.docker.com/get-started/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and commit
4. Push to branch: `git push origin feature/my-feature`
5. Open pull request

The CI/CD pipeline will automatically test your changes!

## 📄 License

This project is for educational purposes.

## 🎓 Learning Outcomes

After completing this project, you'll understand:

- ✅ End-to-end ML pipeline design
- ✅ Data versioning with DVC
- ✅ Docker containerization
- ✅ Cloud deployment on AWS
- ✅ CI/CD automation with GitHub Actions
- ✅ Model versioning and management
- ✅ API development with FastAPI
- ✅ Production ML best practices

## 🚀 Next Steps

1. **Local Setup** → [QUICKSTART.md](./QUICKSTART.md)
2. **Containerization** → [DOCKER_GUIDE.md](./DOCKER_GUIDE.md)
3. **AWS Deployment** → [AWS_DEPLOYMENT_GUIDE.md](./AWS_DEPLOYMENT_GUIDE.md)
4. **CI/CD Setup** → [GITHUB_ACTIONS_SETUP.md](./GITHUB_ACTIONS_SETUP.md)
5. **Model Versioning** → [MODEL_VERSIONING_GUIDE.md](./MODEL_VERSIONING_GUIDE.md)

## 📞 Support

- 📖 **Documentation** - Check the guides linked above
- 🐛 **Issues** - [GitHub Issues](https://github.com/TejasThange3/Mlops-Project/issues)
- 💬 **Discussions** - [GitHub Discussions](https://github.com/TejasThange3/Mlops-Project/discussions)

---

<div align="center">

**Built with ❤️ using Python, DVC, FastAPI, Docker, and AWS**

[GitHub](https://github.com/TejasThange3/Mlops-Project) • [Issues](https://github.com/TejasThange3/Mlops-Project/issues)

</div>
