"""
Audio module for text-to-speech functionality
Provides voice feedback for detected objects
"""

import pyttsx3
import time
import threading
from queue import Queue, Empty
from typing import Dict, Set

class AudioFeedback:
    def __init__(self, voice_enabled=True, cooldown_period=3.0):
        """
        Initialize audio feedback system
        
        Args:
            voice_enabled (bool): Whether voice feedback is enabled
            cooldown_period (float): Cooldown period in seconds between repeated announcements
        """
        self.voice_enabled = voice_enabled
        self.cooldown_period = cooldown_period
        self.engine = None
        self.speech_queue = Queue()
        self.is_speaking = False
        
        # Track last spoken objects to avoid repetition
        self.last_spoken: Dict[str, float] = {}
        
        # Thread for handling speech
        self.speech_thread = None
        self.stop_speech = False
        
        # Initialize TTS engine
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize the text-to-speech engine"""
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to use a female voice which is often clearer
                for voice in voices:
                    if 'female' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 150)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.9)
            
            print("Text-to-speech engine initialized successfully")
            
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.voice_enabled = False
    
    def start_speech_thread(self):
        """Start the background speech thread"""
        if self.voice_enabled and self.speech_thread is None:
            self.stop_speech = False
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
            print("Speech thread started")
    
    def stop_speech_thread(self):
        """Stop the background speech thread"""
        self.stop_speech = True
        if self.speech_thread:
            self.speech_thread.join(timeout=1.0)
            self.speech_thread = None
            print("Speech thread stopped")
    
    def _speech_worker(self):
        """Background thread worker for handling speech"""
        while not self.stop_speech:
            try:
                # Get message from queue with timeout
                message = self.speech_queue.get(timeout=0.1)
                
                if message and self.engine:
                    self.is_speaking = True
                    self.engine.say(message)
                    self.engine.runAndWait()
                    self.is_speaking = False
                
                self.speech_queue.task_done()
                
            except Empty:
                continue
            except Exception as e:
                print(f"Error in speech worker: {e}")
                self.is_speaking = False
    
    def announce_detections(self, detections):
        """
        Process and announce detected objects
        
        Args:
            detections (list): List of detection dictionaries
        """
        if not self.voice_enabled or not detections:
            return
        
        current_time = time.time()
        
        # Filter detections based on cooldown and importance
        important_detections = []
        
        for detection in detections:
            class_name = detection['class_name']
            direction = detection['direction']
            distance = detection['distance']
            is_critical = detection['is_critical']
            
            # Create unique key for this object type and position
            object_key = f"{class_name}_{direction}"
            
            # Check if we should announce this object
            should_announce = False
            
            if is_critical:
                # Critical objects have shorter cooldown
                cooldown = self.cooldown_period / 2
            else:
                cooldown = self.cooldown_period
            
            # Check if enough time has passed since last announcement
            if object_key not in self.last_spoken:
                should_announce = True
            elif current_time - self.last_spoken[object_key] > cooldown:
                should_announce = True
            
            if should_announce:
                important_detections.append(detection)
                self.last_spoken[object_key] = current_time
        
        # Generate and queue speech messages
        for detection in important_detections:
            message = self._generate_speech_message(detection)
            if message:
                self.speech_queue.put(message)
    
    def _generate_speech_message(self, detection):
        """
        Generate a natural speech message for a detection
        
        Args:
            detection (dict): Detection dictionary
            
        Returns:
            str: Speech message
        """
        class_name = detection['class_name']
        direction = detection['direction']
        distance = detection['distance']
        is_critical = detection['is_critical']
        confidence = detection['confidence']
        
        # Only announce if confidence is reasonable
        if confidence < 0.3:
            return None
        
        # Generate different message formats based on importance and distance
        if is_critical:
            if distance == 'close':
                message = f"Warning: {class_name} very close {direction}"
            else:
                message = f"Caution: {class_name} {direction}"
        else:
            if distance == 'close':
                message = f"{class_name} near {direction}"
            elif distance == 'medium':
                message = f"{class_name} {direction}"
            else:
                message = f"{class_name} far {direction}"
        
        return message
    
    def speak_immediate(self, message):
        """
        Speak a message immediately (bypasses queue)
        
        Args:
            message (str): Message to speak
        """
        if not self.voice_enabled or not self.engine:
            return
        
        try:
            # Stop any current speech
            self.engine.stop()
            
            # Speak the new message
            self.engine.say(message)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Error speaking immediate message: {e}")
    
    def toggle_voice(self):
        """Toggle voice feedback on/off"""
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        print(f"Voice feedback {status}")
        
        if self.voice_enabled:
            self.speak_immediate("Voice feedback enabled")
        else:
            self.stop_speech_thread()
    
    def set_cooldown_period(self, seconds):
        """
        Set the cooldown period for repeated announcements
        
        Args:
            seconds (float): Cooldown period in seconds
        """
        self.cooldown_period = max(1.0, seconds)  # Minimum 1 second
        print(f"Cooldown period set to {self.cooldown_period} seconds")
    
    def clear_history(self):
        """Clear the history of spoken objects"""
        self.last_spoken.clear()
        print("Speech history cleared")
    
    def get_status(self):
        """
        Get current status of the audio system
        
        Returns:
            dict: Status information
        """
        return {
            'voice_enabled': self.voice_enabled,
            'is_speaking': self.is_speaking,
            'queue_size': self.speech_queue.qsize(),
            'cooldown_period': self.cooldown_period,
            'tracked_objects': len(self.last_spoken)
        }

# Test function
def test_audio():
    """Test the audio feedback system"""
    print("Testing audio feedback system...")
    
    audio = AudioFeedback()
    audio.start_speech_thread()
    
    # Test messages
    test_messages = [
        "Person detected in front",
        "Car approaching from the left",
        "Chair on the right side"
    ]
    
    for message in test_messages:
        audio.speak_immediate(message)
        time.sleep(2)
    
    print("Audio test completed")
    audio.stop_speech_thread()

if __name__ == "__main__":
    test_audio()
