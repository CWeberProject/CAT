import os
import sys
import json
from datetime import datetime
from anthropic import Anthropic
from PIL import Image
import base64
from io import BytesIO

# Update the path for recordings
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Recordings')

class TaskAnalyzer:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        
    def encode_image(self, image_path):
        """Convert image to base64 string"""
        with Image.open(image_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
            
    def analyze_session(self, session_folder):
        """Analyze a complete recording session"""
        # Load events data
        events_path = os.path.join(session_folder, 'events.json')
        with open(events_path, 'r') as f:
            events = json.load(f)
            
        # Load metadata
        metadata_path = os.path.join(session_folder, 'metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        # Process and attach frames to events
        frames_dir = os.path.join(session_folder, 'frames')
        events_with_context = []
        
        for event in events:
            event_context = {
                'type': event['type'],
                'timestamp': event['timestamp'],
                'details': {}
            }
            
            # Add event-specific details
            if event['type'] == 'mouse_click':
                event_context['details'] = {
                    'coordinates': f"({event['x']}, {event['y']})",
                    'button': event['button'],
                    'state': event['state']
                }
            elif event['type'] == 'key_press':
                event_context['details'] = {
                    'key': event['key']
                }
            elif event['type'] == 'browser_navigation':
                event_context['details'] = {
                    'url': event['url']
                }
                
            # Add web context if available
            if 'context' in event and event['context'] == 'web':
                event_context['web_context'] = event['url']
                
            # Add frame if available
            if 'frame' in event:
                frame_path = os.path.join(session_folder, event['frame'])
                if os.path.exists(frame_path):
                    event_context['frame'] = self.encode_image(frame_path)
                    
            events_with_context.append(event_context)
            
        # Create analysis prompt for Claude
        prompt = self.create_analysis_prompt(events_with_context, metadata)
        
        # Get analysis from Claude 3.5 Sonnet (latest)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5
        )
        
        # Extract the text content from the response
        return response.content[0].text if isinstance(response.content, list) else response.content

    def create_analysis_prompt(self, events, metadata):
        """Create a detailed prompt for Claude to analyze the session"""
        prompt = """As an expert in user interaction analysis and workflow understanding, please analyze this sequence of computer interactions. Your task is to:

1. Provide a concise one-sentence summary of the user's overall objective
2. Create a chronological breakdown of the main steps taken to accomplish this task
3. Give a detailed natural language description of each significant action, incorporating both interaction data and visual context from the frames

Focus on identifying patterns, understanding user intent, and creating a clear narrative of the workflow. Consider the temporal relationships between events and any web-based context to inform your analysis.

Session Information:
"""
        
        prompt += f"""
Duration: {metadata['duration']:.2f} seconds
Total Events: {metadata['total_events']}
Event Distribution: {json.dumps(metadata['event_types'], indent=2)}

Detailed Event Sequence:
"""
        
        for i, event in enumerate(events, 1):
            prompt += f"\nEvent {i}:"
            prompt += f"\nType: {event['type']}"
            prompt += f"\nTimestamp: {event['timestamp']:.2f}s"
            
            if 'web_context' in event:
                prompt += f"\nWeb Context: {event['web_context']}"
                
            if 'details' in event:
                prompt += f"\nDetails: {json.dumps(event['details'], indent=2)}"
                
            if 'frame' in event:
                prompt += f"\n[Frame available for visual context]"
                
            prompt += "\n---"
            
        prompt += """

Please structure your analysis as follows:

OVERALL OBJECTIVE:
[One clear sentence describing the user's goal]

STEP-BY-STEP BREAKDOWN:
1. [Step 1]
2. [Step 2]
...

DETAILED ANALYSIS:
[Provide a natural language description of the workflow, highlighting key actions and their significance. Reference specific events and visual context where relevant.]

Focus Points:
- Sequence and timing of actions
- Patterns in user behavior
- Context from web navigation
- Any corrections or repeated actions that might indicate user intent
- Logical grouping of related actions into meaningful steps
"""

        return prompt

def main():
    # Get API key from environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")
        
    # Initialize analyzer
    analyzer = TaskAnalyzer(api_key)
    
    # List available recordings
    recordings = [d for d in os.listdir(RECORDINGS_DIR) 
                 if os.path.isdir(os.path.join(RECORDINGS_DIR, d)) 
                 and d.startswith('recording_')]
    
    if not recordings:
        print("No recordings found in the Recordings directory.")
        return
        
    print("\nAvailable recordings:")
    for i, recording in enumerate(recordings, 1):
        print(f"{i}. {recording}")
        
    # Get user selection
    while True:
        try:
            selection = int(input("\nEnter the number of the recording to analyze: ")) - 1
            if 0 <= selection < len(recordings):
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    session_folder = os.path.join(RECORDINGS_DIR, recordings[selection])
    
    print(f"\nAnalyzing session: {recordings[selection]}")
    
    try:
        # Run analysis
        analysis = analyzer.analyze_session(session_folder)
        
        # Save analysis to file
        output_path = os.path.join(session_folder, 'analysis.txt')
        with open(output_path, 'w') as f:
            f.write(analysis)
            
        print(f"\nAnalysis saved to: {output_path}")
        print("\nAnalysis summary:")
        print("-" * 50)
        print(analysis)
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main()
