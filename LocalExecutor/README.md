# CAT Local Executor

This repository contains the Local Executor module for the Computer Action Tester (CAT) project. This module handles local GUI automation and communication with the remote server.

## Prerequisites

### Windows
- Python 3.8+
- Git

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev scrot
```

### macOS
```bash
brew install python-tk
```

## Installation Steps

### 1. Clone Repository

```bash
# Initialize a new git repository
git init

# Add the remote repository
git remote add origin https://github.com/AyoubSaidane/CAT.git

# Enable sparse checkout
git config core.sparseCheckout true

# Specify the LocalExecutor folder
echo "LocalExecutor" >> .git/info/sparse-checkout

# Pull the content
git pull origin main
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### 3. Configuration

1. Create a `.env` file in the LocalExecutor directory
2. Add the following configuration, replacing with your values:

```bash
# Remote machine configuration
REMOTE_USER=your_remote_user
REMOTE_HOST=your_remote_host
REMOTE_BASE_PATH=/path/to/remote/results
TASK_REMOTE_BASE_PATH=/path/to/remote/task
IMG_REMOTE_BASE_PATH=/path/to/remote/images

# Local machine configuration
LOCAL_BASE_PATH=/path/to/local/results
IMG_LOCAL_BASE_PATH=/path/to/local/images
TASK_LOCAL_PATH=/path/to/local/task.json
```
