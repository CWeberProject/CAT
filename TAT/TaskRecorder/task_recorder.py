import os
import sys
import pyautogui
from pynput import mouse, keyboard
import time
import json
from datetime import datetime
import threading
import cv2
import numpy as np
from PIL import ImageGrab
import subprocess
from collections import deque
import platform

# Update the path for recordings
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Recordings')

class SmartTaskRecorder:
    def __init__(self):
        self.recording = False
        self.events = []
        self.start_time = None
        
        # Create timestamp and directory structure
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = os.path.join(RECORDINGS_DIR, f"recording_{self.timestamp}")
        self.frames_dir = os.path.join(self.session_dir, "frames")
        
        # Create directories
        os.makedirs(self.session_dir, exist_ok=True)
        os.makedirs(self.frames_dir, exist_ok=True)
        
        # Frame capture
        self.frame_buffer = deque(maxlen=30)  # 3 seconds at 10 FPS
        self.last_frame_time = time.time()
        
        # Browser tracking
        self.current_url = None
        self.last_window_title = None
        
        # Debug logging
        self.log_file = os.path.join(self.session_dir, "debug.log")
        
    def log_debug(self, message):
        """Write debug message to log file"""
        with open(self.log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            f.write(f"{timestamp}: {message}\n")

    def get_timestamp(self):
        return time.time() - self.start_time

    def get_active_browser_url(self):
        """Get URL from active browser - platform specific implementation"""
        if platform.system() == 'Darwin':  # macOS
            return self._get_macos_browser_url()
        elif platform.system() == 'Windows':
            return self._get_windows_browser_url()
        else:
            self.log_debug("Unsupported platform for browser URL detection")
            return None

    def _get_macos_browser_url(self):
        """Get browser URL on macOS using AppleScript"""
        browsers = {
            'Google Chrome': """
                tell application "Google Chrome"
                    get URL of active tab of front window
                end tell
            """,
            'Safari': """
                tell application "Safari"
                    get URL of current tab of front window
                end tell
            """
        }
        
        for browser, script in browsers.items():
            try:
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except Exception as e:
                self.log_debug(f"{browser} URL fetch error: {e}")
        return None

    def _get_windows_browser_url(self):
        """Get browser URL on Windows - placeholder for Windows implementation"""
        self.log_debug("Windows browser URL detection not yet implemented")
        return None

    def track_active_window(self):
        """Track the currently active window and detect web browsing"""
        try:
            url = self.get_active_browser_url()
            if url and url != self.current_url:
                self.current_url = url
                
                # Save frame before URL change
                frame_path = self.save_event_frame('browser_navigation')
                
                event = {
                    'type': 'browser_navigation',
                    'url': url,
                    'timestamp': self.get_timestamp()
                }
                
                if frame_path:
                    event['frame'] = frame_path
                    
                self.events.append(event)
                self.log_debug(f"Recorded browser navigation to: {url}")
                
        except Exception as e:
            self.log_debug(f"Error tracking window: {e}")

    def capture_frame(self):
        """Capture a single frame"""
        try:
            frame = ImageGrab.grab()
            frame_np = np.array(frame)
            frame_rgb = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
            
            # Add timestamp to frame
            timestamp = self.get_timestamp()
            height, width = frame_rgb.shape[:2]
            cv2.putText(
                frame_rgb,
                f"{timestamp:.3f}",
                (10, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            
            return frame_rgb
        except Exception as e:
            self.log_debug(f"Frame capture error: {e}")
            return None

    def save_event_frame(self, event_type):
        """Save current frame for an event"""
        try:
            if len(self.frame_buffer) > 0:
                frame = self.frame_buffer[-1]
                frame_id = f"{event_type}_{int(self.get_timestamp()*1000)}"
                frame_path = os.path.join(self.frames_dir, f"{frame_id}.png")
                
                cv2.imwrite(frame_path, frame)
                self.log_debug(f"Saved frame: {frame_path}")
                
                return os.path.relpath(frame_path, self.session_dir)
            return None
        except Exception as e:
            self.log_debug(f"Frame save error: {e}")
            return None

    def record_frames(self):
        """Continuously record frames"""
        self.log_debug("Starting frame recording")
        while self.recording:
            try:
                frame = self.capture_frame()
                if frame is not None:
                    self.frame_buffer.append(frame)
                    
                # Track browser activity
                self.track_active_window()
                    
                time.sleep(0.1)  # 10 FPS
            except Exception as e:
                self.log_debug(f"Frame recording error: {e}")

    def on_mouse_click(self, x, y, button, pressed):
        """Record mouse clicks"""
        if self.recording:
            frame_path = self.save_event_frame('click')
            
            event = {
                'type': 'mouse_click',
                'x': x,
                'y': y,
                'button': str(button),
                'state': 'pressed' if pressed else 'released',
                'timestamp': self.get_timestamp()
            }
            
            if frame_path:
                event['frame'] = frame_path
                
            if self.current_url:
                event['context'] = 'web'
                event['url'] = self.current_url
            
            self.events.append(event)
            self.log_debug(f"Recorded click event at ({x}, {y})")

    def on_key_press(self, key):
        """Handle key press events"""
        if key == keyboard.Key.esc:
            if not self.recording:
                self.start()
            else:
                self.stop()
            return True
            
        if self.recording:
            try:
                key_char = key.char if hasattr(key, 'char') else str(key)
                frame_path = self.save_event_frame('keypress')
                
                event = {
                    'type': 'key_press',
                    'key': key_char,
                    'timestamp': self.get_timestamp()
                }
                
                if frame_path:
                    event['frame'] = frame_path
                    
                if self.current_url:
                    event['context'] = 'web'
                    event['url'] = self.current_url
                
                self.events.append(event)
                self.log_debug(f"Recorded key press: {key_char}")
                
            except AttributeError:
                pass

    def start(self):
        """Start recording"""
        print("\nStarting recording...")
        self.log_debug("Starting new recording session")
        
        self.recording = True
        self.start_time = time.time()
        
        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_click=self.on_mouse_click
        )
        self.mouse_listener.start()
        
        # Start frame recording thread
        self.frame_thread = threading.Thread(target=self.record_frames)
        self.frame_thread.start()
        
        print("Recording in progress. Press ESC to stop...")
        self.log_debug("Recording started successfully")

    def stop(self):
        """Stop recording"""
        print("\nStopping recording...")
        self.log_debug("Stopping recording session")
        
        self.recording = False
        
        # Save all data
        try:
            # Save events
            events_path = os.path.join(self.session_dir, 'events.json')
            with open(events_path, 'w') as f:
                json.dump(self.events, f, indent=2)
            
            # Save metadata
            metadata = {
                'session_start': self.start_time,
                'session_end': time.time(),
                'duration': self.get_timestamp(),
                'total_events': len(self.events),
                'total_frames': len(os.listdir(self.frames_dir)),
                'event_types': {
                    'mouse_clicks': len([e for e in self.events if e['type'] == 'mouse_click']),
                    'key_presses': len([e for e in self.events if e['type'] == 'key_press']),
                    'browser_navigations': len([e for e in self.events if e['type'] == 'browser_navigation']),
                    'web_events': len([e for e in self.events if 'context' in e and e['context'] == 'web'])
                }
            }
            
            metadata_path = os.path.join(self.session_dir, 'metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            self.log_debug("Session data saved successfully")
            
        except Exception as e:
            self.log_debug(f"Error saving session data: {e}")
        
        print(f"Recording saved to: {self.session_dir}")
        print("Check debug.log for detailed information")
        print("\nPress ESC to start a new recording or Ctrl+C to exit")

def main():
    print("=== Smart Task Recorder ===")
    print("This program will record your actions with web awareness.")
    print("Press ESC to start recording")
    print("Press ESC again to stop recording")
    print("Press Ctrl+C in the terminal to exit the program")
    
    recorder = SmartTaskRecorder()
    
    with keyboard.Listener(on_press=recorder.on_key_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            if recorder.recording:
                recorder.stop()
            print("\nProgram terminated by user")

if __name__ == "__main__":
    main()
