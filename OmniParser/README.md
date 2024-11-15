# CAT - OmniParser

This repository contains the OmniParser module for automated computer interaction testing. Follow these instructions to set up and run the project on your remote machine.

## Prerequisites

- Git
- Python 3.8+
- CUDA-compatible GPU
- Anthropic API key

## Installation Steps

After connecting via SSH to your remote machine, you can follow these installation steps:

### 1. Clone Specific Folder

```bash
# Initialize a new git repository
git init

# Add the remote repository
git remote add origin https://github.com/AyoubSaidane/CAT.git

# Enable sparse checkout
git config core.sparseCheckout true

# Specify the OmniParser folder
echo "OmniParser" >> .git/info/sparse-checkout

# Pull the content
git pull origin master
```

### 2. Install Dependencies

```bash
# Navigate to OmniParser directory
cd OmniParser

# Install basic requirements
pip install -r requirements.txt

# Install PyTorch with CUDA support
pip install torch=='2.4.1+cu121' torchvision=='0.19.1+cu121' torchaudio=='2.4.1+cu121' --index-url https://download.pytorch.org/whl/cu121

# Install additional dependencies
pip install flash_attn
pip install anthropic
```

### 3. Install Model

```bash
# Run the download script to get required model weights
bash download.sh
```

### 4. Configuration

1. Locate the `.env` file in the OmniParser directory
2. Open the file in your preferred text editor
3. Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual Anthropic API key
