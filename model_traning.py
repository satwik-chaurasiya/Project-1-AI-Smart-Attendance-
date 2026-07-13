import cv2
import os
import numpy as np
from PIL import Image

script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(script_dir, 'dataset')

# Initialize OpenCV's Local Binary Patterns Histograms face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(os.path.join(script_dir, 'haarcascade_frontalface_default.xml'))

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    face_samples = []
    ids = []
    
    for image_path in image_paths:
        # Convert image to grayscale using Pillow
        pil_img = Image.open(image_path).convert('L')
        img_numpy = np.array(pil_img, 'uint8')
        
        # Extract the ID from the filename (User.ID.sample.jpg)
        filename = os.path.basename(image_path)
        user_id = int(filename.split('.')[1])
        
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)
            
    return face_samples, ids

print("Training face recognizer model. Please wait...")
faces, ids = get_images_and_labels(dataset_path)

if len(faces) == 0:
    print("Error: No images found in the dataset folder. Register a user first.")
    exit()

recognizer.train(faces, np.array(ids))

# Save the trained model
model_path = os.path.join(script_dir, 'trainer.yml')
recognizer.write(model_path)
print(f"Model trained successfully! Saved to {model_path}")