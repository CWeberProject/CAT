# CAT (Computer Automated Tasks)

CAT is a system designed to automate computer interactions using advanced AI vision and natural language processing. The system operates in two parts: a GPU-powered server component (OmniParser) for AI processing, and a local component (LocalExecutor) for GUI automation.

## Installation

The system requires two separate installations:
- Server setup: [OmniParser/README.md](OmniParser/README.md)
- Client setup: [LocalExecutor/README.md](LocalExecutor/README.md)

## Running the System

1. Start the server:
```bash
# On the GPU server
cd OmniParser
python CAT_server.py
```

2. Start the client:
```bash
# On your local machine
cd LocalExecutor
python CAT_local.py
```

## How It Works

1. LocalExecutor captures screen information and sends it to OmniParser
2. OmniParser processes the image using AI vision models
3. Natural language instructions are interpreted into computer actions
4. LocalExecutor executes the determined actions
5. The process repeats for continuous automation

## Acknowledgments

This project builds upon the [OmniParser](https://github.com/microsoft/OmniParser) framework by Microsoft. We thank the original authors for their groundbreaking work in computer vision and automation.
