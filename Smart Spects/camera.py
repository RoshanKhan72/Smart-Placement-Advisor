"""
Camera module for handling webcam operations
Provides real-time video capture functionality
"""

import cv2
import time

class Camera:
    def __init__(self, camera_id=0, resolution=(640, 480)):
        """
        Initialize camera with specified ID and resolution
        
        Args:
            camera_id (int): Camera device ID (default: 0)
            resolution (tuple): Camera resolution (width, height)
        """
        self.camera_id = camera_id
        self.resolution = resolution
        self.cap = None
        self.is_running = False
        
    def initialize(self):
        """
        Initialize the camera and set resolution
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                print(f"Error: Could not open camera {self.camera_id}")
                return False
                
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            
            # Set FPS for better performance
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            print(f"Camera {self.camera_id} initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            return False
    
    def get_frame(self):
        """
        Capture a single frame from the camera
        
        Returns:
            tuple: (success, frame) where frame is the captured image
        """
        if not self.is_running or self.cap is None:
            return False, None
            
        try:
            ret, frame = self.cap.read()
            if ret:
                return True, frame
            else:
                print("Error: Could not read frame from camera")
                return False, None
                
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return False, None
    
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            self.is_running = False
            print("Camera released")
    
    def __del__(self):
        """Destructor to ensure camera is released"""
        self.release()

# Test function
def test_camera():
    """Test camera functionality"""
    camera = Camera()
    if camera.initialize():
        print("Camera test successful. Press 'q' to quit.")
        
        while True:
            success, frame = camera.get_frame()
            if success:
                cv2.imshow('Camera Test', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        
        camera.release()
        cv2.destroyAllWindows()
    else:
        print("Camera test failed")

if __name__ == "__main__":
    test_camera()
