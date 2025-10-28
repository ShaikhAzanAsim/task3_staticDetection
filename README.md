# 🧠 Abandoned Object & Activity Detection using Background Subtraction (OpenCV)

This project detects **abandoned or stationary objects** in a store or monitored environment using **background subtraction** and **temporal tracking**.  
It compares each video frame against a *reference (ideal empty) background* and identifies objects that remain in the same position for a specified duration (e.g., 5–10 seconds).

---

## 🎯 Project Objective
Automatically detect **objects left behind** or **unattended regions** (e.g., a shopping bag left on a shelf, or a box placed in a previously empty area).

---

## 🧩 Features
✅ Compares each video frame against a static “empty” background image  
✅ Uses **frame differencing** and **morphological operations** for noise-free detection  
✅ Tracks motion over time to identify **persistent stationary objects**  
✅ Highlights such regions with **red bounding boxes** and labels them as “Abandoned”  
✅ Real-time visualization of intermediate steps (difference, mask, contours, etc.)  

---

## 🧾 Requirements

Install dependencies using pip:


pip install opencv-python

---
## ⚙️ Input Files

reference.png → A static image of the empty background (e.g., empty store, empty shelf).

output_1min.mp4 → A video file where objects appear, move, or are left behind.

---
## 🚀 How It Works

Load the reference (empty) background image

Compare each frame of the live/busy video with the reference

Detect changes via absolute difference and thresholding

Clean the binary mask using morphological operations

Track detected contours across consecutive frames

Flag regions that remain unchanged for n seconds as “Abandoned”

---

## 🧠 Algorithm Steps
Step	Description

1️⃣	Compute absolute difference between current frame and ideal background

2️⃣	Apply binary threshold to highlight changed areas

3️⃣	Morphologically close small holes and remove noise

4️⃣	Extract contours representing detected regions

5️⃣	Track each region across frames

6️⃣	If a region persists longer than the defined threshold (e.g., 5 seconds), label it as Abandoned

---

## 🧰 Parameters to Tune

Parameter	Description	Default

threshold_frames	Number of frames an object must persist to be considered “abandoned”	5 * fps

area < 500	Minimum contour area to ignore small noise	500

diff threshold	Pixel difference for foreground detection	50

---

## 🧑‍💻 Author

Shaikh Azan

📧 [azanasim1@gmail.com]

💡 Specializing in Computer Vision, AI, and Automation.

---

## 🪪 License

This project is licensed under the MIT License — feel free to use, modify, and distribute it.

