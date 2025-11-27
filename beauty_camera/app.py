import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from datetime import datetime

st.set_page_config(page_title="Beauty Camera", layout="wide")

st.title("📸 Beauty Camera with Filters + Photo Capture + Video Recorder")

# ---------- SAVE FOLDER ----------
SAVE_DIR = "saved_photos"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------- FILTERS ----------
def apply_filter(frame, filter_type):
    if filter_type == "None":
        return frame
    elif filter_type == "Gray":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == "Cartoon":
        gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 7)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(frame, 9, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon
    elif filter_type == "Blur":
        return cv2.GaussianBlur(frame, (25, 25), 0)
    return frame


# ---------- SIDEBAR ----------
st.sidebar.header("🎨 Controls")

filter_type = st.sidebar.selectbox(
    "Select Filter", ["None", "Gray", "Cartoon", "Blur"]
)

capture_btn = st.sidebar.button("📷 Capture Photo")
start_record_btn = st.sidebar.button("🎥 Start Recording")
stop_record_btn = st.sidebar.button("⏹ Stop Recording")

# Temporary file for recording video
if "recording" not in st.session_state:
    st.session_state.recording = False

if "video_writer" not in st.session_state:
    st.session_state.video_writer = None

if "video_path" not in st.session_state:
    st.session_state.video_path = None


# ---------- CAMERA ----------
camera_slot = st.empty()

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*"XVID")

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not found!")
        break

    frame = cv2.flip(frame, 1)
    filtered_frame = apply_filter(frame.copy(), filter_type)

    # Show in Streamlit
    camera_slot.image(filtered_frame, channels="BGR")

    # ---------- PHOTO CAPTURE ----------
    if capture_btn:
        filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        path = f"{SAVE_DIR}/{filename}"
        cv2.imwrite(path, filtered_frame)
        st.success(f"Photo saved: {path}")

        _, buffer = cv2.imencode(".jpg", filtered_frame)
        st.download_button(
            label="⬇ Download Captured Photo",
            data=buffer.tobytes(),
            file_name=filename,
            mime="image/jpeg"
        )

    # ---------- START VIDEO RECORD ----------
    if start_record_btn and not st.session_state.recording:
        st.session_state.video_path = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        st.session_state.video_writer = cv2.VideoWriter(
            st.session_state.video_path, fourcc, 20.0,
            (frame.shape[1], frame.shape[0])
        )
        st.session_state.recording = True
        st.success("🎥 Recording Started")

    # ---------- RECORDING ONGOING ----------
    if st.session_state.recording:
        st.session_state.video_writer.write(filtered_frame)

    # ---------- STOP VIDEO ----------
    if stop_record_btn and st.session_state.recording:
        st.session_state.recording = False
        st.session_state.video_writer.release()
        st.success("⏹ Recording Saved!")

        # Download Button
        with open(st.session_state.video_path, "rb") as f:
            st.download_button(
                label="⬇ Download Video",
                data=f,
                file_name=st.session_state.video_path,
                mime="video/avi"
            )

    # Streamlit loop break
    if not st.sidebar.button("Refresh Camera"):
        pass