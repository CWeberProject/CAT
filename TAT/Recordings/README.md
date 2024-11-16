# Recordings Directory

## Overview
This directory contains all recorded user interaction sessions. Each session is stored in a timestamped folder with a structured format for data organization.

## Directory Structure

```
Recordings/
└── recording_YYYYMMDD_HHMMSS/        # Session folder
    ├── frames/                       # Screenshot directory
    │   ├── click_[timestamp].png     # Click event screenshots
    │   ├── keypress_[timestamp].png  # Keypress event screenshots
    │   └── browser_[timestamp].png   # Browser navigation screenshots
    ├── events.json                   # Event sequence data
    ├── metadata.json                 # Session information
    ├── analysis.txt                  # AI-generated analysis
    └── debug.log                     # Session logging data
```

## File Descriptions

### events.json
Contains an array of event objects with:
```json
{
  "type": "mouse_click|key_press|browser_navigation",
  "timestamp": 1234.56,
  "x": 100,           // For mouse clicks
  "y": 200,           // For mouse clicks
  "button": "Button.left",  // For mouse clicks
  "key": "a",         // For keypresses
  "url": "https://...",  // For browser events
  "frame": "frames/event_123.png",
  "context": "web",   // If in browser
  "state": "pressed|released"  // For mouse clicks
}
```

### metadata.json
Session metadata including:
```json
{
  "session_start": 1234567890.123,
  "session_end": 1234567890.123,
  "duration": 123.45,
  "total_events": 100,
  "total_frames": 50,
  "event_types": {
    "mouse_clicks": 30,
    "key_presses": 60,
    "browser_navigations": 10,
    "web_events": 40
  }
}
```

### analysis.txt
AI-generated analysis containing:
- Overall task description
- Step-by-step breakdown
- Detailed workflow analysis
- Pattern recognition insights

### frames/
Screenshots captured before significant events:
- High-quality PNG format
- Timestamped for correlation with events
- Named according to trigger event type

### debug.log
Detailed session logging including:
- System status messages
- Error reports
- Performance metrics
- Event processing confirmations

## Storage Management

- Sessions are never automatically deleted
- Manual cleanup may be required for disk space management
- Consider archiving old sessions before deletion
- Each session can range from a few MB to several GB depending on duration and activity

## Best Practices

1. **Organization**
   - Keep original session folders intact
   - Don't modify filenames
   - Create backups of important sessions

2. **Maintenance**
   - Regularly review and archive old sessions
   - Monitor available disk space
   - Maintain consistent naming conventions

## Usage Notes

- Session folders are read-only after creation
- Analysis can be re-run on any session
- Screenshots can be viewed independently
- Events can be correlated with frames using timestamps

## Troubleshooting

Common issues:
- Missing frames: Check debug.log for capture errors
- Incomplete events.json: Session may have ended unexpectedly
- Missing metadata: Session may not have completed properly

## Security Considerations

- Sessions may contain sensitive information
- Screenshots might include personal data
- Consider security implications before sharing sessions
- Review content before distribution