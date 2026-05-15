"""
Main application for AI-powered object detection for visually impaired users
Integrates camera, detection, and audio modules
"""

import cv2
import time
import argparse
import sys
from datetime import datetime

from camera import Camera
from detector import ObjectDetector
from audio import AudioFeedback

class VisionAssistant:
    def __init__(self, camera_id=0, model_path='yolov8n.pt', 
                 confidence_threshold=0.5, voice_enabled=True):
        """
        Initialize the Vision Assistant application
        
        Args:
            camera_id (int): Camera device ID
            model_path (str): Path to YOLO model
            confidence_threshold (float): Detection confidence threshold
            voice_enabled (bool): Enable voice feedback
        """
        self.camera = Camera(camera_id=camera_id)
        self.detector = ObjectDetector(
            model_path=model_path,
            confidence_threshold=confidence_threshold
        )
        self.audio = AudioFeedback(voice_enabled=voice_enabled)
        
        self.running = False
        self.fps = 0
        self.frame_count = 0
        self.last_fps_time = time.time()
        
        # Statistics
        self.total_frames = 0
        self.total_detections = 0
        
    def initialize(self):
        """
        Initialize all components
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("Initializing Vision Assistant...")
        
        # Initialize camera
        if not self.camera.initialize():
            print("Failed to initialize camera")
            return False
        
        # Load detection model
        if not self.detector.load_model():
            print("Failed to load detection model")
            return False
        
        # Start audio thread
        self.audio.start_speech_thread()
        
        print("Vision Assistant initialized successfully")
        return True
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            return
        
        self.running = True
        print("\n=== Vision Assistant Started ===")
        print("Controls:")
        print("  'q' - Quit application")
        print("  'v' - Toggle voice feedback")
        print("  'c' - Clear speech history")
        print("  's' - Show statistics")
        print("  '+/-' - Adjust confidence threshold")
        print("  'h' - Show help")
        print("================================\n")
        
        # Welcome message
        if self.audio.voice_enabled:
            self.audio.speak_immediate("Vision Assistant started")
        
        try:
            while self.running:
                start_time = time.time()
                
                # Capture frame
                success, frame = self.camera.get_frame()
                if not success:
                    print("Failed to capture frame")
                    break
                
                # Detect objects
                detections, annotated_frame = self.detector.detect_objects(frame)
                
                # Announce detections
                self.audio.announce_detections(detections)
                
                # Update statistics
                self.total_frames += 1
                self.total_detections += len(detections)
                
                # Calculate FPS
                self.frame_count += 1
                current_time = time.time()
                if current_time - self.last_fps_time >= 1.0:
                    self.fps = self.frame_count
                    self.frame_count = 0
                    self.last_fps_time = current_time
                
                # Draw UI overlay
                self._draw_ui_overlay(annotated_frame, detections)
                
                # Display frame
                cv2.imshow('Vision Assistant', annotated_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if not self._handle_keyboard_input(key):
                    break
                
                # Control frame rate (target 30 FPS)
                elapsed = time.time() - start_time
                if elapsed < 1/30:
                    time.sleep(1/30 - elapsed)
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        
        finally:
            self.cleanup()
    
    def _draw_ui_overlay(self, frame, detections):
        """
        Draw UI overlay on the frame
        
        Args:
            frame (numpy.ndarray): Input frame
            detections (list): List of detections
        """
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay for text background
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 80), (0, 0, 0), -1)
        alpha = 0.7
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        # Draw title
        cv2.putText(frame, 'Vision Assistant', (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw FPS
        cv2.putText(frame, f'FPS: {self.fps}', (10, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw detection count
        cv2.putText(frame, f'Detections: {len(detections)}', (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw voice status
        voice_status = "ON" if self.audio.voice_enabled else "OFF"
        voice_color = (0, 255, 0) if self.audio.voice_enabled else (0, 0, 255)
        cv2.putText(frame, f'Voice: {voice_status}', (width - 120, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, voice_color, 1)
        
        # Draw confidence threshold
        conf_text = f'Conf: {self.detector.confidence_threshold:.2f}'
        cv2.putText(frame, conf_text, (width - 120, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Draw critical object warning
        critical_detections = [d for d in detections if d['is_critical']]
        if critical_detections:
            cv2.putText(frame, '⚠ CRITICAL OBJECTS', (width - 200, 75),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Draw timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (width - 100, height - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def _handle_keyboard_input(self, key):
        """
        Handle keyboard input
        
        Args:
            key (int): Key code
            
        Returns:
            bool: True to continue running, False to quit
        """
        if key == ord('q') or key == 27:  # 'q' or ESC
            print("Quitting application...")
            if self.audio.voice_enabled:
                self.audio.speak_immediate("Goodbye")
            return False
        
        elif key == ord('v'):  # Toggle voice
            self.audio.toggle_voice()
        
        elif key == ord('c'):  # Clear speech history
            self.audio.clear_history()
            if self.audio.voice_enabled:
                self.audio.speak_immediate("Speech history cleared")
        
        elif key == ord('s'):  # Show statistics
            self._show_statistics()
        
        elif key == ord('+') or key == ord('='):  # Increase confidence
            self.detector.confidence_threshold = min(1.0, 
                self.detector.confidence_threshold + 0.05)
            print(f"Confidence threshold: {self.detector.confidence_threshold:.2f}")
        
        elif key == ord('-') or key == ord('_'):  # Decrease confidence
            self.detector.confidence_threshold = max(0.1, 
                self.detector.confidence_threshold - 0.05)
            print(f"Confidence threshold: {self.detector.confidence_threshold:.2f}")
        
        elif key == ord('h'):  # Show help
            self._show_help()
        
        return True
    
    def _show_statistics(self):
        """Display application statistics"""
        runtime = time.time() - self.last_fps_time + self.total_frames / max(1, self.fps)
        avg_detections = self.total_detections / max(1, self.total_frames)
        
        print("\n=== Statistics ===")
        print(f"Total frames processed: {self.total_frames}")
        print(f"Total detections: {self.total_detections}")
        print(f"Average detections per frame: {avg_detections:.2f}")
        print(f"Current FPS: {self.fps}")
        print(f"Confidence threshold: {self.detector.confidence_threshold:.2f}")
        
        audio_status = self.audio.get_status()
        print(f"Voice enabled: {audio_status['voice_enabled']}")
        print(f"Objects tracked: {audio_status['tracked_objects']}")
        print("==================\n")
        
        if self.audio.voice_enabled:
            self.audio.speak_immediate(f"Processed {self.total_frames} frames with {self.total_detections} detections")
    
    def _show_help(self):
        """Show help information"""
        print("\n=== Help ===")
        print("Vision Assistant helps visually impaired users navigate by detecting objects")
        print("and providing voice feedback about their surroundings.")
        print("\nControls:")
        print("  'q' - Quit application")
        print("  'v' - Toggle voice feedback on/off")
        print("  'c' - Clear speech history (allows immediate re-announcement)")
        print("  's' - Show application statistics")
        print("  '+/-' - Increase/decrease detection confidence threshold")
        print("  'h' - Show this help message")
        print("  'ESC' - Quit application")
        print("\nDetection Information:")
        print("  - Red boxes indicate critical objects (people, vehicles, etc.)")
        print("  - Green boxes indicate regular objects")
        print("  - Direction shows object position (left, center, right)")
        print("  - Distance shows approximate proximity (close, medium, far)")
        print("=============\n")
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        
        self.running = False
        
        # Stop audio thread
        self.audio.stop_speech_thread()
        
        # Release camera
        self.camera.release()
        
        # Close OpenCV windows
        cv2.destroyAllWindows()
        
        print("Cleanup completed")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Vision Assistant for Visually Impaired Users')
    parser.add_argument('--camera', type=int, default=0, help='Camera device ID (default: 0)')
    parser.add_argument('--model', type=str, default='yolov8n.pt', help='YOLO model path (default: yolov8n.pt)')
    parser.add_argument('--confidence', type=float, default=0.5, help='Detection confidence threshold (default: 0.5)')
    parser.add_argument('--no-voice', action='store_true', help='Disable voice feedback')
    
    args = parser.parse_args()
    
    # Create and run the application
    app = VisionAssistant(
        camera_id=args.camera,
        model_path=args.model,
        confidence_threshold=args.confidence,
        voice_enabled=not args.no_voice
    )
    
    try:
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        app.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
