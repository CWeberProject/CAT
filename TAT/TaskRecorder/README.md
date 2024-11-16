# Task Activity Recorder (TaskRecorder)

## Overview
TaskRecorder is a Python-based system that captures and records user interactions with their computer. It provides detailed tracking of:
- Mouse clicks and keyboard events
- Browser activity and URL changes
- Screenshots captured before significant events
- Detailed event timing and context

## Features
- Real-time capture of user interactions
- Automatic browser URL tracking (supports Chrome and Safari)
- Screenshot capture for significant events
- Detailed event logging with timestamps
- Structured data output in JSON format
- Cross-platform support (optimized for macOS, basic support for Windows)

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

## Usage

Run the recorder:
```bash
python task_recorder.py
```

### Controls
- Press ESC to start recording
- Press ESC again to stop recording
- Press Ctrl+C in the terminal to exit the program

### Output
The recorder creates a timestamped folder in the `../Recordings` directory containing:
- `frames/`: Screenshot directory
  - `click_*.png`: Screenshots taken before mouse clicks
  - `keypress_*.png`: Screenshots taken before key presses
  - `browser_navigation_*.png`: Screenshots taken before URL changes
- `events.json`: Structured data about all recorded events
- `metadata.json`: Session information and statistics
- `debug.log`: Detailed logging information

## Data Structure

### events.json
Contains an array of event objects, each with:
- Event type (click, keypress, browser_navigation)
- Timestamp
- Coordinates (for mouse events)
- Browser context (when applicable)
- Reference to associated frame

### metadata.json
Contains session information:
- Start and end times
- Duration
- Total event count
- Event type distribution
- Frame count

## System Requirements
- Python 3.8+
- Operating System:
  - macOS: Full support with browser tracking
  - Windows: Basic support (browser tracking limited)
  - Linux: Basic support
- Sufficient disk space for frame storage

## Known Limitations
- Browser URL tracking is currently optimized for macOS
- High-frequency actions may impact performance
- Large sessions can generate significant disk usage