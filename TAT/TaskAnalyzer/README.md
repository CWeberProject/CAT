# Task Activity Analyzer (TaskAnalyzer)

## Overview
TaskAnalyzer is a Python-based system that uses Claude 3.5 Sonnet AI to analyze recorded user interactions. It processes recorded sessions to:
- Determine the user's overall task/goal
- Break down the sequence of actions
- Provide detailed natural language descriptions of the workflow

## Features
- AI-powered analysis of user interactions
- Natural language output
- Integration with frame captures
- Contextual understanding of web activities
- Structured workflow breakdown
- Pattern recognition in user behavior

## Installation

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

## Usage

1. Run the analyzer:
```bash
python task_analyzer.py
```

2. When prompted, select a recording session from the list of available recordings in the `../Recordings` directory.

### Output
The analyzer creates an `analysis.txt` file in the recording session folder containing:
- Overall task description (one sentence)
- Step-by-step breakdown of user actions
- Detailed analysis of significant steps
- Contextual interpretation of user intentions

## Analysis Features

The system analyzes:
- Temporal sequences of actions
- Patterns in user behavior
- Web navigation context
- Visual information from screenshots
- User corrections and repeated actions
- Action grouping and workflow structure

## System Requirements
- Python 3.8+
- Anthropic API key
- Internet connection (for AI analysis)
- Access to recording session data

## Input Data Structure

The analyzer expects recording sessions with:
- `events.json`: Event sequence data
- `metadata.json`: Session information
- `frames/`: Directory containing event screenshots

## Limitations
- Analysis quality depends on recording completeness
- Large sessions may take longer to process
- API rate limits may apply
- Internet connection required for analysis