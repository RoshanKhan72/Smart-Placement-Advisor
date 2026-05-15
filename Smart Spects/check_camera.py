import cv2

print("Checking available cameras...")
print("=" * 30)

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Camera {i}: Available - Resolution: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print(f"⚠️  Camera {i}: Available but can't read frame")
        cap.release()
    else:
        print(f"❌ Camera {i}: Not available")

print("\nTry running with: python main.py --camera X")
print("Where X is the available camera number")
