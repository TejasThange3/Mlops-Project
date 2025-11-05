# MLOps Project - Complete Commands Reference

## Table of Contents

1. [Git Commands](#git-commands)
2. [DVC Commands](#dvc-commands)
3. [Docker Commands](#docker-commands)
4. [FastAPI Commands](#fastapi-commands)
5. [EC2 Deployment Commands](#ec2-deployment-commands)
6. [Testing Commands](#testing-commands)

---

## Git Commands

| Command                         | Definition                                               |
| ------------------------------- | -------------------------------------------------------- |
| `git init`                      | Initialize a new Git repository in the current directory |
| `git clone <repo-url>`          | Clone a remote repository to your local machine          |
| `git add <file>`                | Stage a file for commit                                  |
| `git add .`                     | Stage all modified files for commit                      |
| `git commit -m "message"`       | Create a commit with a descriptive message               |
| `git push origin main`          | Push commits to the remote main branch                   |
| `git pull origin main`          | Fetch and merge latest changes from remote main branch   |
| `git status`                    | Show the status of modified and staged files             |
| `git log`                       | Display commit history                                   |
| `git branch`                    | List all local branches                                  |
| `git checkout -b <branch-name>` | Create and switch to a new branch                        |
| `git merge <branch-name>`       | Merge a branch into the current branch                   |
| `git remote -v`                 | Show all configured remote repositories and their URLs   |
| `git config user.name "name"`   | Set the user name for commits                            |
| `git config user.email "email"` | Set the user email for commits                           |

---

## DVC Commands

| Command                                    | Definition                                                            |
| ------------------------------------------ | --------------------------------------------------------------------- |
| `dvc init`                                 | Initialize DVC in the project directory                               |
| `dvc add <file>`                           | Track a file or directory with DVC for versioning                     |
| `dvc remote add -d myremote <path-or-url>` | Add a remote storage location for DVC files                           |
| `dvc push`                                 | Upload tracked files to remote storage                                |
| `dvc pull`                                 | Download tracked files from remote storage                            |
| `dvc repro`                                | Execute the entire DVC pipeline (preprocessing, training, evaluation) |
| `dvc repro <stage-name>`                   | Execute a specific stage in the DVC pipeline                          |
| `dvc dag`                                  | Display the directed acyclic graph (pipeline structure)               |
| `dvc metrics show`                         | Display all tracked metrics from the latest run                       |
| `dvc metrics diff`                         | Compare metrics between different runs or commits                     |
| `dvc exp show`                             | Show all experiments and their results                                |
| `dvc exp run`                              | Run an experiment with the current configuration                      |
| `dvc params show`                          | Display current parameters from params.yaml                           |
| `dvc status`                               | Check the status of pipeline stages and outputs                       |
| `dvc cache dir`                            | Display the cache directory location                                  |
| `dvc cache remove`                         | Remove cached files to free up space                                  |

---

## Docker Commands

| Command                                                   | Definition                                                |
| --------------------------------------------------------- | --------------------------------------------------------- |
| `docker build -t <image-name>:<tag> .`                    | Build a Docker image from Dockerfile in current directory |
| `docker build -t <image-name>:latest .`                   | Build Docker image and tag it as latest                   |
| `docker images`                                           | List all Docker images on the system                      |
| `docker ps`                                               | List all running containers                               |
| `docker ps -a`                                            | List all containers (running and stopped)                 |
| `docker run -p <host-port>:<container-port> <image-name>` | Start a container from an image with port mapping         |
| `docker run -d <image-name>`                              | Start a container in detached mode (background)           |
| `docker exec -it <container-id> bash`                     | Execute a bash shell inside a running container           |
| `docker logs <container-id>`                              | Display logs from a running container                     |
| `docker logs -f <container-id>`                           | Stream logs in real-time (follow mode)                    |
| `docker stop <container-id>`                              | Stop a running container gracefully                       |
| `docker kill <container-id>`                              | Force stop a running container                            |
| `docker rm <container-id>`                                | Remove a stopped container                                |
| `docker rmi <image-id>`                                   | Remove a Docker image                                     |
| `docker push <registry>/<image-name>:<tag>`               | Push a Docker image to a registry                         |
| `docker pull <image-name>:<tag>`                          | Pull a Docker image from a registry                       |
| `docker login <registry>`                                 | Login to a Docker registry                                |
| `docker logout <registry>`                                | Logout from a Docker registry                             |
| `docker system prune -f`                                  | Remove unused containers, images, and networks            |
| `docker system prune -a`                                  | Remove all unused Docker resources                        |

---

## Docker Compose Commands

| Command                                   | Definition                                                        |
| ----------------------------------------- | ----------------------------------------------------------------- |
| `docker-compose up -d`                    | Start all services defined in docker-compose.yml in detached mode |
| `docker-compose up`                       | Start all services and display logs                               |
| `docker-compose down`                     | Stop and remove all running containers from docker-compose        |
| `docker-compose down --remove-orphans`    | Stop containers and remove orphaned containers from previous runs |
| `docker-compose ps`                       | List all containers managed by docker-compose                     |
| `docker-compose logs`                     | Display logs from all services                                    |
| `docker-compose logs <service-name>`      | Display logs from a specific service                              |
| `docker-compose logs -f`                  | Stream logs in real-time from all services                        |
| `docker-compose exec <service-name> bash` | Execute a bash shell in a running service container               |
| `docker-compose build`                    | Build images for services defined in docker-compose.yml           |
| `docker-compose build --no-cache`         | Build images without using cache                                  |
| `docker-compose restart`                  | Restart all running services                                      |
| `docker-compose stop`                     | Stop all running services                                         |

---

## FastAPI Commands

| Command                                                                                     | Definition                                               |
| ------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `python main.py`                                                                            | Start the FastAPI application (if configured in main.py) |
| `python -m uvicorn main:app --reload`                                                       | Start FastAPI with automatic reload on code changes      |
| `python -m uvicorn main:app --host 0.0.0.0 --port 8000`                                     | Start FastAPI on all interfaces on port 8000             |
| `python -m uvicorn main:app --reload --host 0.0.0.0`                                        | Start FastAPI with reload on all interfaces              |
| `curl http://localhost:8000/health`                                                         | Test the health check endpoint                           |
| `curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{...}'` | Make a prediction request to the API                     |

---

## Project Execution Commands

| Command                             | Definition                                         |
| ----------------------------------- | -------------------------------------------------- |
| `python src/preprocess_presplit.py` | Run data preprocessing stage                       |
| `python src/train_ensemble.py`      | Run model training with ensemble methods           |
| `python src/evaluate.py`            | Run model evaluation and generate metrics          |
| `python src/predict_test.py`        | Run batch predictions on test data                 |
| `python test_api.py`                | Run API endpoint tests                             |
| `pytest -v --tb=short`              | Run pytest with verbose output and short traceback |
| `pytest -v`                         | Run all tests with verbose output                  |

---

## EC2 Deployment Commands

| Command                                                          | Definition                                            |
| ---------------------------------------------------------------- | ----------------------------------------------------- |
| `ssh -i <key.pem> ubuntu@<EC2_PUBLIC_IP>`                        | SSH into an EC2 instance                              |
| `ssh -i <key.pem> -L 8000:localhost:8000 ubuntu@<EC2_PUBLIC_IP>` | SSH with port forwarding to access remote app locally |
| `sudo apt-get update`                                            | Update package manager index                          |
| `sudo apt-get upgrade -y`                                        | Upgrade all installed packages                        |
| `sudo apt-get install -y docker.io docker-compose`               | Install Docker and Docker Compose                     |
| `sudo usermod -aG docker ubuntu`                                 | Add ubuntu user to docker group                       |
| `newgrp docker`                                                  | Activate docker group membership without logout       |
| `sudo systemctl start docker`                                    | Start Docker service                                  |
| `sudo systemctl enable docker`                                   | Enable Docker to start on boot                        |
| `git clone <repo-url>`                                           | Clone the project repository                          |
| `cd <project-directory>`                                         | Navigate to project directory                         |
| `docker-compose up -d`                                           | Start the application in detached mode                |
| `docker-compose logs -f mlops-api`                               | Monitor application logs in real-time                 |
| `curl http://localhost:8000/health`                              | Check if API is responding                            |
| `sudo netstat -tulpn \| grep LISTEN`                             | List all listening ports and services                 |
| `sudo ss -tulpn \| grep 8000`                                    | Check if port 8000 is listening                       |

---

## Common Workflow

### Local Development Workflow

```bash
# 1. Clone repository
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize DVC (if not already initialized)
dvc init

# 4. Run the complete pipeline
dvc repro

# 5. Check metrics
dvc metrics show

# 6. Start the API
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. Test the API
curl http://localhost:8000/health
```

### GitHub Push Workflow

```bash
# 1. Make changes to code
# 2. Stage changes
git add .

# 3. Commit with message
git commit -m "Add new feature"

# 4. Push to main branch
git push origin main
```

### Docker Build and Test Workflow

```bash
# 1. Build Docker image
docker build -t mlops-water-potability:latest .

# 2. Run container
docker run -d -p 8000:8000 mlops-water-potability:latest

# 3. Check logs
docker logs -f <container-id>

# 4. Test API
curl http://localhost:8000/health

# 5. Stop container
docker stop <container-id>
```

### EC2 Deployment Workflow

```bash
# 1. SSH into EC2
ssh -i mlops-project-key.pem ubuntu@<EC2_PUBLIC_IP>

# 2. Install dependencies
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# 3. Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# 4. Clone repository
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project

# 5. Start application
docker-compose up -d

# 6. Verify deployment
docker-compose ps
curl http://localhost:8000/health

# 7. Monitor logs
docker-compose logs -f mlops-api
```

### DVC Pipeline Workflow

```bash
# 1. Initialize DVC
dvc init

# 2. Add data files
dvc add data/train_dataset.csv
dvc add data/test_dataset.csv

# 3. Configure remote storage
dvc remote add -d myremote /path/to/remote/storage

# 4. Push data to remote
dvc push

# 5. Run pipeline
dvc repro

# 6. View metrics
dvc metrics show

# 7. Compare different runs
dvc metrics diff

# 8. Check pipeline structure
dvc dag

# 9. Run specific stage
dvc repro train
```

---

## Quick Reference Cheat Sheet

### Most Used Commands

```bash
# Git
git add . && git commit -m "message" && git push origin main

# DVC
dvc repro                    # Run entire pipeline
dvc metrics show             # View results

# Docker
docker-compose up -d         # Start app
docker-compose down          # Stop app
docker-compose logs -f       # View logs

# FastAPI
python -m uvicorn main:app --reload

# Testing
curl http://localhost:8000/health
python test_api.py
pytest -v
```

---

## Environment Setup Commands

```bash
# Python virtual environment
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate           # On Windows

# Install dependencies
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip

# Install specific package
pip install <package-name>
```

---

**Last Updated**: November 5, 2025
**Project**: Water Potability Prediction - MLOps
