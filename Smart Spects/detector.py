"""
Object detection module using YOLOv8
Provides real-time object detection with confidence filtering
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt', confidence_threshold=0.5):
        """
        Initialize the object detector
        
        Args:
            model_path (str): Path to YOLO model file
            confidence_threshold (float): Minimum confidence for detections
        """
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.class_names = []
        
        # Critical objects that need priority alerts
        self.critical_objects = {
            'person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle',
            'traffic light', 'stop sign', 'stairs', 'door'
        }
        
        # Object categories for better descriptions
        self.object_categories = {
            'person': 'person',
            'car': 'vehicle', 'truck': 'vehicle', 'bus': 'vehicle', 
            'motorcycle': 'vehicle', 'bicycle': 'vehicle',
            'chair': 'furniture', 'couch': 'furniture', 'bed': 'furniture',
            'dining table': 'furniture', 'toilet': 'furniture',
            'laptop': 'electronic', 'cell phone': 'electronic',
            'tv': 'electronic', 'keyboard': 'electronic',
            'book': 'object', 'cup': 'object', 'bottle': 'object',
            'backpack': 'object', 'handbag': 'object', 'tie': 'object',
            'suitcase': 'object', 'frisbee': 'object', 'skis': 'object',
            'snowboard': 'object', 'sports ball': 'object', 'kite': 'object',
            'baseball bat': 'object', 'baseball glove': 'object',
            'skateboard': 'object', 'surfboard': 'object',
            'tennis racket': 'object', 'banana': 'object', 'apple': 'object',
            'sandwich': 'object', 'orange': 'object', 'broccoli': 'object',
            'carrot': 'object', 'hot dog': 'object', 'pizza': 'object',
            'donut': 'object', 'cake': 'object'
        }
        
    def load_model(self):
        """
        Load the YOLO model
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"Loading YOLO model: {self.model_path}")
            self.model = YOLO(self.model_path)
            self.class_names = self.model.names
            print(f"Model loaded successfully. Classes: {len(self.class_names)}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def detect_objects(self, frame):
        """
        Detect objects in the given frame
        
        Args:
            frame (numpy.ndarray): Input image frame
            
        Returns:
            tuple: (detections, annotated_frame)
                - detections: List of detection dictionaries
                - annotated_frame: Frame with bounding boxes drawn
        """
        if self.model is None:
            print("Model not loaded")
            return [], frame
        
        try:
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            annotated_frame = frame.copy()
            
            for result in results:
                boxes = result.boxes
                
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    
                    # Get class name
                    class_name = self.class_names[class_id]
                    
                    # Calculate center point and size
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    width = int(x2 - x1)
                    height = int(y2 - y1)
                    
                    # Determine direction
                    direction = self._get_direction(center_x, frame.shape[1])
                    
                    # Estimate distance (rough approximation based on box size)
                    distance = self._estimate_distance(width, height, class_name)
                    
                    # Create detection dictionary
                    detection = {
                        'class_name': class_name,
                        'confidence': float(confidence),
                        'bbox': {
                            'x1': int(x1), 'y1': int(y1),
                            'x2': int(x2), 'y2': int(y2),
                            'center_x': center_x, 'center_y': center_y,
                            'width': width, 'height': height
                        },
                        'direction': direction,
                        'distance': distance,
                        'is_critical': class_name in self.critical_objects
                    }
                    
                    detections.append(detection)
                    
                    # Draw bounding box and label
                    self._draw_detection(annotated_frame, detection)
            
            return detections, annotated_frame
            
        except Exception as e:
            print(f"Error during detection: {e}")
            return [], frame
    
    def _get_direction(self, center_x, frame_width):
        """
        Determine the direction of object based on its position
        
        Args:
            center_x (int): X coordinate of object center
            frame_width (int): Width of the frame
            
        Returns:
            str: Direction ('left', 'center', 'right')
        """
        third = frame_width // 3
        
        if center_x < third:
            return 'left'
        elif center_x > 2 * third:
            return 'right'
        else:
            return 'center'
    
    def _estimate_distance(self, width, height, class_name):
        """
        Estimate distance based on bounding box size
        
        Args:
            width (int): Width of bounding box
            height (int): Height of bounding box
            class_name (str): Name of the detected class
            
        Returns:
            str: Estimated distance ('close', 'medium', 'far')
        """
        # Simple distance estimation based on object size
        # This is a rough approximation and may not be very accurate
        area = width * height
        
        # Different thresholds for different object types
        if class_name == 'person':
            if area > 15000:
                return 'close'
            elif area > 5000:
                return 'medium'
            else:
                return 'far'
        elif class_name in ['car', 'truck', 'bus']:
            if area > 20000:
                return 'close'
            elif area > 8000:
                return 'medium'
            else:
                return 'far'
        else:
            if area > 10000:
                return 'close'
            elif area > 3000:
                return 'medium'
            else:
                return 'far'
    
    def _draw_detection(self, frame, detection):
        """
        Draw bounding box and label on the frame
        
        Args:
            frame (numpy.ndarray): Input frame
            detection (dict): Detection dictionary
        """
        bbox = detection['bbox']
        class_name = detection['class_name']
        confidence = detection['confidence']
        direction = detection['direction']
        distance = detection['distance']
        is_critical = detection['is_critical']
        
        # Choose color based on importance
        if is_critical:
            color = (0, 0, 255)  # Red for critical objects
        else:
            color = (0, 255, 0)  # Green for normal objects
        
        # Draw bounding box
        cv2.rectangle(frame, 
                     (bbox['x1'], bbox['y1']), 
                     (bbox['x2'], bbox['y2']), 
                     color, 2)
        
        # Create label text
        label = f"{class_name}: {confidence:.2f}"
        label_info = f"{direction}, {distance}"
        
        # Draw label background
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        info_size = cv2.getTextSize(label_info, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
        
        cv2.rectangle(frame,
                     (bbox['x1'], bbox['y1'] - 40),
                     (bbox['x1'] + max(label_size[0], info_size[0]) + 10, bbox['y1']),
                     color, -1)
        
        # Draw text
        cv2.putText(frame, label, 
                   (bbox['x1'] + 5, bbox['y1'] - 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        cv2.putText(frame, label_info,
                   (bbox['x1'] + 5, bbox['y1'] - 8),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

# Test function
def test_detector():
    """Test the detector with a sample image"""
    detector = ObjectDetector()
    if detector.load_model():
        print("Detector test successful")
    else:
        print("Detector test failed")

if __name__ == "__main__":
    test_detector()
