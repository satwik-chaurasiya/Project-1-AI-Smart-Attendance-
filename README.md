---
# AI-Based Smart Attendance Monitoring System
---
An automated, real-time facial recognition attendance system built using Python and OpenCV. This system leverages the **Local Binary Patterns Histograms (LBPH)** algorithm to recognize faces, log attendance automatically into a CSV spreadsheet with precise dates and times, and capture/alert against unauthorized or unrecognized individuals.

---

## 📌 Objectives
* **Automation:** Eliminate manual role-calling or biometric fingerprint scanning to save time and reduce hardware touchpoints.
* **Accuracy & Security:** Maintain data integrity by using unique Student/Employee IDs, allowing accurate logging even when users share identical names.
* **Intruder Detection:** Enhance premises security by identifying unauthorized personnel, sounding alerts, and logging snapshot evidence.
* **Seamless Operations:** Ensure offline-first, light-weight processing capable of running smoothly on standard computer webcams without demanding expensive GPU resources.

---

## 🚀 Core Features
* **Duplicate Name Support:** Relies on a primary key (`Student ID`) rather than strings, eliminating system errors when managing students with the same name.
* **Smart Data Validation:** Pre-checks local text databases and dataset files dynamically to ensure IDs aren't overwritten or duplicated during registration.
* **Automated Cascade Downloader:** Seamlessly downloads necessary tracking dependencies (`haarcascade_frontalface_default.xml`) if they are missing at initialization.
* **Intruder Logging Vault:** Automatically crops and captures unknown faces, saving them to a specialized `unknown_faces` folder with an anti-flood 10-second capture throttle.
* **Anti-Spam CSV Logger:** Tracks entries locally per session to avoid writing duplicate rows if a student remains standing in front of the camera window.

---

## 🛠️ Project Structure
```text
Project-1/
│
├── face_registration.py       # Run 1st: Registers users and saves 50 facial samples
├── model_training.py          # Run 2nd: Trains the LBPH framework on collected images
├── main.py                    # Run 3rd: The core camera tracking loop & attendance logger
│
├── user_mapping.txt           # Generated: Key-value map pairing IDs with Names
├── trainer.yml                # Generated: The trained mathematical matrix file
├── attendance.csv             # Generated: The actual Excel-compatible attendance sheet
│
└── unknown_faces/             # Generated: Folder containing snapshots of unrecognized faces
```
---
##⚙️ Methodology & How to Use 
---

**Follow these execution steps in precise order to set up your environment:**

**Step 1:** Register User ProfilesRun the registration script to record a new student profile. The script will request a unique ID and name, run a validation check against duplicates, and use your camera to collect 50 grayscale cropped facial matrices.
---

---
<img width="582" height="207" alt="image" src="https://github.com/user-attachments/assets/6d447d91-e93d-4d2a-8287-228e46fc18b4" />
---



```Bash
python face_registration.py
```
Note: If a name is already taken, the system gracefully generates an alert but permits registration by pinning it to a unique ID.
<img width="732" height="95" alt="image" src="https://github.com/user-attachments/assets/1f8c7a5a-9411-46e7-a866-e4b8a9655a9f" />

---
**Step 2:** Train the ModelCompile the dataset images into an optimized machine learning data matrix. This builds the trainer.yml file.
---
<img width="900" height="57" alt="image" src="https://github.com/user-attachments/assets/c0be6324-6209-41ad-bcc3-45e964518332" />

```Bash
python model_training.py
```
---
Step 3: Launch the Attendance MonitorStart the live monitoring station. The camera frame will open, highlighting known profiles in Green (automatically logging their timestamped arrival in attendance.csv) and unknown faces in Red.
---

```Bash
python attandence_marking.py
```
---
To exit the camera application: Press the q key on your keyboard while focusing on the video screen.📊 Sample Output LogsWhen attendance is captured, it updates the attendance.csv sheet cleanly:
---

<img width="435" height="112" alt="image" src="https://github.com/user-attachments/assets/e357af75-b8d3-4282-b6f2-513f2aa47689" />

---
