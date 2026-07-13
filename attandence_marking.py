import cv2
import os
import urllib.request
from datetime import datetime
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
model_path = os.path.join(script_dir, 'trainer.yml')
csv_path = os.path.join(script_dir, 'attendance.csv')

# Dynamic creation of the folder for unrecognized individuals
unknown_dir = os.path.join(script_dir, 'unknown_faces')
if not os.path.exists(unknown_dir):
    os.makedirs(unknown_dir)

# 1. Download Haar Cascade if missing
if not os.path.exists(xml_path):
    print("XML file not found. Downloading it automatically...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, xml_path)

face_identification = cv2.CascadeClassifier(xml_path)

# 2. Load Recognizer and Trained Model
recognizer = cv2.face.LBPHFaceRecognizer_create()
if os.path.exists(model_path):
    recognizer.read(model_path)
else:
    print("CRITICAL ERROR: 'trainer.yml' not found. Please run train_model.py first.")
    exit()

# 3. Load User Mappings (ID -> Name)
names_map = {0: "Unknown"}
mapping_path = os.path.join(script_dir, "user_mapping.txt")
if os.path.exists(mapping_path):
    with open(mapping_path, "r") as f:
        for line in f:
            if line.strip():
                uid, name = line.strip().split(',')
                names_map[int(uid)] = name

def mark_attendance(user_name):
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Date', 'Time'])
            
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')
        writer.writerow([user_name, date_str, time_str])
    print(f" Attendance recorded for {user_name} at {time_str}")

# 4. Camera Init Setup
cap = None
for index in [0, 1, 2, 3, -1]:
    test_cap = cv2.VideoCapture(index)
    if test_cap.isOpened():
        cap = test_cap
        break
    test_cap.release()

if cap is None:
    print("CRITICAL ERROR: No working camera could be detected.")
    exit()

already_logged = set() 
unknown_cooldown = {} # Prevent flooding the folder with hundreds of identical unknown images

# --- MAIN LOOP ---
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Smoother Face Detection Settings
    faces = face_identification.detectMultiScale(
        gray, 
        scaleFactor=1.2, # Smoothes out false positive variations
        minNeighbors=6,   # Higher value ensures only high-quality structures pass
        minSize=(50, 50)  # Skips tiny, noisy artifacts in the background
    )
    
    now = datetime.now()
    current_time_str = now.strftime('%H:%M:%S')
    
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        user_id, distance = recognizer.predict(face_roi) # distance is the internal confidence level
        
        # --- SMOOTHNESS / ACCURACY ADJUSTMENT ---
        # Adjust 75 if it's too aggressive or too lenient. 
        # Lower value (e.g., 65) = Stricter matching. Higher value (e.g., 85) = More lenient matching.
        if distance < 75:  
            name = names_map.get(user_id, "Unknown")
            confidence_percentage = round(100 - distance)
            confidence_str = f"{max(0, confidence_percentage)}%"
            color = (0, 255, 0) # Green box
            
            if name != "Unknown" and name not in already_logged:
                mark_attendance(name)
                already_logged.add(name)
        else:
            # Face is unrecognized (Distance is too large)
            name = "Unknown"
            confidence_str = "N/A"
            color = (0, 0, 255) # Red box
            
            # Save Unknown Intruder Image (Throttle it to once every 10 seconds)
            time_key = now.strftime('%Y%m%d_%H%M%S')
            last_saved = unknown_cooldown.get('last_time')
            
            if last_saved is None or (now - last_saved).total_seconds() > 10:
                print(f"⚠️ ALERT: Unknown face detected at {current_time_str}! Saving snapshot...")
                
                # Crop and save the image
                img_name = f"Unknown_{time_key}.jpg"
                cv2.imwrite(os.path.join(unknown_dir, img_name), frame[y:y+h, x:x+w])
                unknown_cooldown['last_time'] = now

        # Draw box and metadata text
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{user_id}: {name}--> ({confidence_str})", (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
    cv2.imshow('Smart Attendance Monitoring System', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()