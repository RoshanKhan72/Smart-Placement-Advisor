"""
Integration test script for Vision Assistant
Tests all modules without requiring webcam access
"""

import cv2
import numpy as np
import time

from detector import ObjectDetector
from audio import AudioFeedback

def create_test_image():
    """Create a simple test image for detection testing"""
    # Create a blank image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Add some rectangles to simulate objects
    cv2.rectangle(img, (100, 100), (200, 300), (255, 0, 0), -1)  # Blue rectangle
    cv2.rectangle(img, (400, 150), (500, 350), (0, 255, 0), -1)  # Green rectangle
    cv2.rectangle(img, (250, 200), (350, 400), (0, 0, 255), -1)  # Red rectangle
    
    # Add some text
    cv2.putText(img, 'TEST IMAGE', (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return img

def test_detector_and_audio():
    """Test detector and audio integration"""
    print("=== Integration Test ===")
    
    # Initialize detector
    detector = ObjectDetector(confidence_threshold=0.3)
    if not detector.load_model():
        print("❌ Failed to load detector")
        return False
    
    print("✅ Detector loaded successfully")
    
    # Initialize audio
    audio = AudioFeedback(voice_enabled=True, cooldown_period=1.0)
    audio.start_speech_thread()
    print("✅ Audio system initialized")
    
    # Create test image
    test_img = create_test_image()
    print("✅ Test image created")
    
    # Run detection test
    print("\nRunning detection test...")
    detections, annotated_img = detector.detect_objects(test_img)
    
    print(f"Found {len(detections)} objects:")
    for i, detection in enumerate(detections):
        print(f"  {i+1}. {detection['class_name']} ({detection['confidence']:.2f}) - {detection['direction']} - {detection['distance']}")
    
    # Test audio announcements
    print("\nTesting audio announcements...")
    audio.announce_detections(detections)
    
    # Wait for audio to complete
    time.sleep(3)
    
    # Test immediate speech
    print("Testing immediate speech...")
    audio.speak_immediate("Integration test completed successfully")
    
    time.sleep(2)
    
    # Cleanup
    audio.stop_speech_thread()
    
    print("\n✅ Integration test completed successfully!")
    return True

def test_audio_only():
    """Test audio system independently"""
    print("=== Audio Only Test ===")
    
    audio = AudioFeedback(voice_enabled=True, cooldown_period=0.5)
    audio.start_speech_thread()
    
    # Test various messages
    test_messages = [
        "Person detected in front",
        "Car approaching from left",
        "Chair on right side",
        "Warning: Vehicle very close"
    ]
    
    for message in test_messages:
        print(f"Speaking: {message}")
        audio.speak_immediate(message)
        time.sleep(2)
    
    audio.stop_speech_thread()
    print("✅ Audio only test completed!")

if __name__ == "__main__":
    print("Vision Assistant Integration Test")
    print("================================")
    
    choice = input("Choose test:\n1. Full integration test\n2. Audio only test\nEnter choice (1 or 2): ")
    
    if choice == "1":
        test_detector_and_audio()
    elif choice == "2":
        test_audio_only()
    else:
        print("Running full integration test by default...")
        test_detector_and_audio()
    
    print("\nTest completed. You can now run the main application with:")
    print("python main.py")
