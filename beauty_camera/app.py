import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import time
import os

st.set_page_config(layout="wide", page_title="Beauty Camera")

st.title("📸 Beauty Camera – Streamlit Version (No OpenCV)")

if not os.path.exists("saved"):
    os.makedirs("saved")

filter_name = st.selectbox(
    "Select Filter",
    ("None", "Beauty Smooth", "Warm", "Cool", "Cartoon", "Black & White", "HDR")
)

capture = st.button("📷 Capture")

# Streamlit camera
frame = st.camera_input("Camera")

# Filter functions
def apply_filter(img, filter_name):

    if filter_name == "None":
        return img

    if filter_name == "Beauty Smooth":
        return img.filter(ImageFilter.SMOOTH_MORE)

    if filter_name == "Warm":
        r, g, b = img.split()
        r = r.point(lambda i: i + 40)
        return Image.merge("RGB", (r, g, b))

    if filter_name == "Cool":
        r, g, b = img.split()
        b = b.point(lambda i: i + 40)
        return Image.merge("RGB", (r, g, b))

    if filter_name == "Black & White":
        return img.convert("L").convert("RGB")

    if filter_name == "HDR":
        enhancer = ImageEnhance.Sharpness(img)
        return enhancer.enhance(3)

    if filter_name == "Cartoon":
        edge = img.filter(ImageFilter.FIND_EDGES)
        return Image.blend(img, edge, 0.5)

    return img


if frame is not None:
    img = Image.open(frame)

    # Apply filter
    filtered = apply_filter(img, filter_name)

    # Show image
    st.image(filtered, width=720)

    # Save image
    if capture:
        filename = f"saved/photo_{int(time.time())}.jpg"
        filtered.save(filename)
        st.success(f"📸 Saved: {filename}")