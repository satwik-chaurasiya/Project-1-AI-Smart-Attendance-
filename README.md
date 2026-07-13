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
