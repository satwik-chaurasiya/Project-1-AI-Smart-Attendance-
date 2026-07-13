import cv2
import os
import urllib.request

script_dir = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')

# 1. Download Haar Cascade if missing
if not os.path.exists(xml_path):
    print("XML file not found. Downloading it automatically...")
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    try:
        urllib.request.urlretrieve(url, xml_path)
        print("Download complete!")
    except Exception as e:
        print(f"Failed to download XML automatically: {e}")

face_classifier = cv2.CascadeClassifier(xml_path)

# 2. Setup Dataset Directory
dataset_path = os.path.join(script_dir, 'dataset')
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

mapping_path = os.path.join(script_dir, "user_mapping.txt")

# --- MODIFIED FEATURE: Strict ID Check, Flexible Name Check ---
def check_if_id_exists(search_id):
    # Check 1: Search inside the text mapping file for the ID only
    if os.path.exists(mapping_path):
        with open(mapping_path, "r") as f:
            for line in f:
                if line.strip():
                    existing_id, existing_name = line.strip().split(',')
                    if existing_id == str(search_id):
                        print(f"\n❌ CRITICAL ERROR: ID '{search_id}' is already taken by '{existing_name}'!")
                        return True

    # Check 2: Check dataset folder for lingering images
    all_files = os.listdir(dataset_path)
    for file in all_files:
        if file.startswith(f"User.{search_id}."):
            print(f"\n❌ CRITICAL ERROR: Image files for ID '{search_id}' already exist in the dataset folder!")
            return True
            
    return False

# 3. User Registration Inputs with Loop Validation
while True:
    user_id = input("Enter a UNIQUE numeric Student ID (e.g., 101, 102): ").strip()
    user_name = input("Enter the student's name: ").strip()
    
    if not user_id.isdigit():
        print("❌ Invalid ID! The ID must be a number.")
        print("--- Please try again ---\n")
        continue
        
    if not user_name:
        print("❌ Invalid Name! Name cannot be blank.")
        print("--- Please try again ---\n")
        continue

    # We ONLY halt if the ID exists. Same names are now allowed!
    if check_if_id_exists(user_id):
        print("Registration halted. You must assign a new, unique ID number for this student.")
        print("--- Restarting Input Process ---\n")
    else:
        # Check if the name is a duplicate just to gently warn the admin
        is_duplicate_name = False
        if os.path.exists(mapping_path):
            with open(mapping_path, "r") as f:
                for line in f:
                    if line.strip() and line.strip().split(',')[1].lower() == user_name.lower():
                        is_duplicate_name = True
                        break
        
        if is_duplicate_name:
            print(f"\n⚠️ NOTE: Another student is already named '{user_name}'.")
            print(f"✅ Allowed! Differentiating this student using ID: {user_id}.")
        else:
            print("\n✅ Verification passed! Creating new profile.")
        break

# 4. Save name mapping since the ID is confirmed unique
with open(mapping_path, "a") as f:
    f.write(f"{user_id},{user_name}\n")

print("\nLook at the camera. Capturing 50 samples...")

# 5. Start Camera Capture Loop
cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        count += 1
        file_name = f"User.{user_id}.{count}.jpg"
        cv2.imwrite(os.path.join(dataset_path, file_name), gray[y:y+h, x:x+w])
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Captured: {count}/50", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("Registering Face", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
        break

cap.release()
cv2.destroyAllWindows()
print(f"Successfully registered {user_name} (ID: {user_id})!")