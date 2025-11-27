import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import os
import imageio

st.set_page_config(page_title="Beauty Camera", layout="wide")

# Create folders
if not os.path.exists("photos"):
    os.makedirs("photos")

if not os.path.exists("videos"):
    os.makedirs("videos")

# ---------------- FILTERS ----------------
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
            blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        return cv2.bitwise_and(color, color, mask=edges)

    return frame


# ---------------- UI ----------------
st.title("📸 Beauty Camera with Video Recording")
st.write("Live Filters + Photo + Video Recording (Streamlit Version)")

col1, col2 = st.columns([3, 1])

with col2:
    filter_names = [
        "Normal",
        "Beauty Smooth",
        "Black & White",
        "Warm Tone",
        "Cool Tone",
        "Cartoon"
    ]

    filter_choice = st.selectbox("Choose Filter", filter_names)
    start_cam = st.checkbox("Start Camera")

    capture_photo = st.button("📸 Capture Photo")
    start_video = st.button("🎬 Start Recording")
    stop_video = st.button("⏹ Stop Recording")

with col1:
    frame_window = st.image([])

filter_index = filter_names.index(filter_choice)

video_buffer = []   # store frames for video recording
recording = False


# ---------------- CAMERA LOOP ----------------
if start_cam:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Camera not detected!")
            break

        frame = cv2.resize(frame, (720, 480))

        filtered = apply_filter(frame, filter_index)

        # Show frame
        frame_window.image(filtered, channels="BGR")

        # ---------------- PHOTO CAPTURE ----------------
        if capture_photo:
            filename = f"photos/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            cv2.imwrite(filename, filtered)
            st.success(f"Saved Photo: {filename}")

        # ---------------- VIDEO RECORDING ----------------
        if start_video:
            recording = True
            video_buffer = []
            st.info("Recording Started...")

        if recording:
            video_buffer.append(filtered)

        if stop_video and recording:
            recording = False
            filename = f"videos/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

            # Save using imageio
            writer = imageio.get_writer(filename, fps=20)
            for f in video_buffer:
                writer.append_data(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
            writer.close()

            st.success(f"Saved Video: {filename}")

        # Escape camera loop
        if not start_cam:
            break

    cap.release()