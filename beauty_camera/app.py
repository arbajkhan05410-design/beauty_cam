import streamlit as st
import cv2
import numpy as np
import os
from datetime import datetime

# -------------- FOLDERS -----------------
if not os.path.exists("photos"):
    os.makedirs("photos")

# -------------- FILTERS -----------------
def apply_filter(frame, index):
    if index == 0:
        return frame

    elif index == 1:  # Beauty Smooth
        blur = cv2.GaussianBlur(frame, (29, 29), 0)
        return cv2.addWeighted(frame, 0.4, blur, 0.6, 0)

    elif index == 2:  # Black & White
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    elif index == 3:  # Warm
        warm = frame.copy()
        warm[:, :, 2] = cv2.add(warm[:, :, 2], 40)
        warm[:, :, 1] = cv2.add(warm[:, :, 1], 20)
        return warm

    elif index == 4:  # Cool
        cool = frame.copy()
        cool[:, :, 0] = cv2.add(cool[:, :, 0], 40)
        cool[:, :, 1] = cv2.add(cool[:, :, 1], 20)
        return cool

    elif index == 5:  # Cartoon
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    return frame

# -------------- STREAMLIT APP -----------------
st.title("📸 Beauty Camera - Filters + Photo Capture (No Video Recording)")

st.write("Use filters → capture photos → saved automatically in `photos/` folder.")

filter_names = [
    "Normal",
    "Beauty Smooth",
    "Black & White",
    "Warm Tone",
    "Cool Tone",
    "Cartoon"
]

filter_selected = st.selectbox("Select Filter", filter_names)

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

filter_index = filter_names.index(filter_selected)

cap = None

if run:
    cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.write("Camera not working!")
        break

    frame = cv2.resize(frame, (720, 480))

    filtered = apply_filter(frame, filter_index)

    FRAME_WINDOW.image(filtered, channels="BGR")

    capture_btn = st.button("📸 Capture Photo")

    if capture_btn:
        filename = f"photos/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, filtered)
        st.success(f"Photo Saved → {filename}")

if cap:
    cap.release()