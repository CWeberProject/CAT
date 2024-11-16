# TAT (Task Analyzer Tool)

## Overview
TAT is a comprehensive system for recording, analyzing, and understanding user interactions with computer systems. It combines real-time interaction capture with AI-powered analysis to provide insights into user workflows and behaviors.

## System Architecture

```
TAT/
├── TaskRecorder/       # Recording component
├── TaskAnalyzer/       # Analysis component
└── Recordings/        # Shared storage for sessions
```

## Components

### 1. TaskRecorder
Records user interactions in real-time, including:
- Mouse clicks and keyboard events
- Browser activity and URL changes
- Screenshot capture at key moments
- Event timing and context

### 2. TaskAnalyzer
Processes recorded sessions using Claude 3.5 Sonnet AI to provide:
- Task goal identification
- Step-by-step workflow breakdown
- Natural language description of user actions
- Pattern recognition and behavioral analysis

### 3. Recordings Directory
Central storage for all recorded sessions, maintaining a structured format for:
- Event data
- Screenshots
- Session metadata
- Analysis results

## How It Works

1. **Recording Phase**
   - User starts TaskRecorder
   - System monitors and captures all interactions
   - Data is saved in structured format to Recordings directory

2. **Analysis Phase**
   - TaskAnalyzer processes recorded sessions
   - AI analyzes interaction patterns and context
   - Generates comprehensive workflow analysis

## Quick Start

1. **Set Up the Environment**
```bash
# Clone the repository
git clone [repository-url]
cd TAT

# Set up TaskRecorder
cd TaskRecorder
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up TaskAnalyzer
cd ../TaskAnalyzer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure API Access**
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

3. **Record a Session**
```bash
cd ../TaskRecorder
python task_recorder.py
# Press ESC to start/stop recording
```

4. **Analyze a Session**
```bash
cd ../TaskAnalyzer
python task_analyzer.py
# Select a session to analyze when prompted
```

## System Requirements

- Python 3.8+
- Operating System:
  - macOS: Full support
  - Windows: Basic support
  - Linux: Basic support
- Sufficient disk space for recordings
- Internet connection for AI analysis
- Anthropic API key

## Best Practices

1. **Recording Sessions**
   - Plan your workflow before recording
   - Avoid unnecessary actions
   - Keep sessions focused on specific tasks

2. **Analysis**
   - Analyze sessions soon after recording
   - Review generated analysis for accuracy
   - Use insights to improve workflows

## Contributing
Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License
[Specify your license here]
