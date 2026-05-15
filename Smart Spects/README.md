# Vision Assistant for Visually Impaired Users

An AI-powered real-time object detection application designed to assist visually impaired users in navigating their surroundings using a PC webcam.

## Features

### Core Functionality
- **Real-time Object Detection**: Uses YOLOv8 deep learning model for accurate and fast object detection
- **Live Webcam Feed**: Captures and displays real-time video from PC camera
- **Smart Audio Feedback**: Converts detected objects into speech using Text-to-Speech
- **Direction Awareness**: Identifies object positions (left, center, right)
- **Distance Estimation**: Approximates object proximity (close, medium, far)

### Detection Capabilities
- **People**: Persons in various positions
- **Vehicles**: Cars, trucks, buses, motorcycles, bicycles
- **Furniture**: Chairs, tables, beds, couches
- **Electronics**: Laptops, phones, TVs, keyboards
- **Everyday Objects**: Books, bottles, cups, bags, and more
- **Critical Objects**: Priority alerts for important items

### Smart Features
- **Confidence Filtering**: Adjustable threshold to filter weak detections
- **Cooldown System**: Prevents repetitive announcements (3-5 seconds)
- **Priority Alerts**: Critical objects get immediate attention
- **Voice Toggle**: Enable/disable voice feedback
- **Statistics Tracking**: Monitor performance and usage

## Installation

### Prerequisites
- Python 3.8 or higher
- PC webcam
- Windows/macOS/Linux operating system
- Internet connection (for first-time model download)

### Step 1: Clone or Download
Download all files to a folder (e.g., `Vision-Assistant`)

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
Run the test commands to ensure everything works:
```bash
python camera.py      # Test camera
python detector.py    # Test detector
python audio.py       # Test audio
```

## Usage

### Basic Usage
Run the application with default settings:
```bash
python main.py
```

### Advanced Options
```bash
# Use different camera
python main.py --camera 1

# Adjust confidence threshold
python main.py --confidence 0.7

# Use different YOLO model
python main.py --model yolov8s.pt

# Disable voice feedback
python main.py --no-voice
```

### Command Line Arguments
- `--camera ID`: Camera device ID (default: 0)
- `--model PATH`: YOLO model file path (default: yolov8n.pt)
- `--confidence FLOAT`: Detection confidence threshold (default: 0.5)
- `--no-voice`: Disable voice feedback

## Controls

### Keyboard Shortcuts
- **`q` or `ESC`**: Quit application
- **`v`**: Toggle voice feedback on/off
- **`c`**: Clear speech history
- **`s`**: Show statistics
- **`+`**: Increase confidence threshold
- **`-`**: Decrease confidence threshold
- **`h`**: Show help message

### On-Screen Information
- **FPS**: Current frames per second
- **Detections**: Number of objects detected
- **Voice Status**: ON/OFF indicator
- **Confidence**: Current threshold
- **Critical Warning**: Alert for important objects
- **Timestamp**: Current time

## Understanding the Display

### Bounding Boxes
- **Red boxes**: Critical objects (people, vehicles, stairs, doors)
- **Green boxes**: Regular objects (furniture, electronics, etc.)

### Labels
Each detected object shows:
- **Object name**: Type of object detected
- **Confidence score**: Detection accuracy (0.00-1.00)
- **Direction**: Position relative to camera (left, center, right)
- **Distance**: Approximate proximity (close, medium, far)

## Audio Feedback

### Voice Announcements
The system announces objects in natural language:
- "Person near center"
- "Car approaching from left"
- "Chair on right side"
- "Warning: Vehicle very close"

### Smart Features
- **Cooldown Period**: Same object not announced repeatedly within 3-5 seconds
- **Priority System**: Critical objects get shorter cooldowns
- **Distance-based Language**: Different phrases for close vs. far objects
- **Directional Context**: Includes position information

## Configuration

### Adjusting Detection Sensitivity
- Use `+`/`-` keys during runtime
- Or set with `--confidence` parameter
- Range: 0.1 (very sensitive) to 1.0 (very strict)

### Voice Settings
- Toggle with `v` key
- Adjust cooldown period in `audio.py`
- Configure voice properties in TTS initialization

### Model Selection
Available YOLOv8 models:
- `yolov8n.pt`: Nano (fastest, good for real-time)
- `yolov8s.pt`: Small (balanced speed/accuracy)
- `yolov8m.pt`: Medium (more accurate, slower)
- `yolov8l.pt`: Large (very accurate, slowest)

## Troubleshooting

### Common Issues

#### Camera Not Found
```bash
# Try different camera IDs
python main.py --camera 1
python main.py --camera 2
```

#### Model Download Fails
- Check internet connection
- Model auto-downloads on first run
- Manual download: Models available from Ultralytics GitHub

#### Voice Not Working
- Check system audio settings
- Ensure speakers are connected
- Try running `python audio.py` separately

#### Performance Issues
- Lower confidence threshold
- Use smaller model (yolov8n.pt)
- Close other applications
- Check system resources

### Error Messages
- **"Could not open camera"**: Camera disconnected or in use
- **"Model not loaded"**: Corrupted model file, redownload
- **"TTS engine error"**: Audio system issues

## Technical Details

### Architecture
The application is modular with separate components:
- **`camera.py`**: Webcam handling and frame capture
- **`detector.py`**: YOLOv8 object detection
- **`audio.py`**: Text-to-speech and voice management
- **`main.py`**: Main application loop and UI

### Dependencies
- **OpenCV**: Computer vision and image processing
- **Ultralytics**: YOLOv8 implementation
- **pyttsx3**: Cross-platform text-to-speech
- **NumPy**: Numerical computations
- **PyTorch**: Deep learning framework

### Performance
- **Target FPS**: 30 frames per second
- **Processing Time**: ~20-30ms per frame
- **Memory Usage**: ~500MB (including model)
- **CPU Usage**: Moderate (depends on model size)

## Contributing

### Adding New Features
1. Modify relevant module files
2. Test individual components
3. Update documentation
4. Test full integration

### Reporting Issues
Include in bug reports:
- Operating system
- Python version
- Camera model
- Error messages
- Steps to reproduce

## License

This project is open source and available under the MIT License.

## Support

For additional support:
1. Check this README thoroughly
2. Review the code comments
3. Test individual modules
4. Check online resources for YOLOv8 and OpenCV

---

**Note**: This application is designed to assist visually impaired users but should not replace traditional mobility aids. Always prioritize safety and use in conjunction with other navigation tools.
