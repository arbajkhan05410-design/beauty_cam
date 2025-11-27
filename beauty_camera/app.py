import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import os

st.set_page_config(layout="wide", page_title="Beauty Camera")

st.title("📸 Beauty Camera Web App")

if not os.path.exists("saved"):
    os.makedirs("saved")

filter_name = st.selectbox(
    "Select Filter",
    ("None", "Beauty", "Warm", "Cool", "Cartoon", "Black & White", "HDR")
)

capture = st.button("📷 Capture Photo")

# Streamlit Camera Input
frame = st.camera_input("Camera")

# Filters
def beauty_filter(img):
    return cv2.bilateralFilter(img, 15, 75, 75)

def warm_filter(img):
    img[:, :, 2] = cv2.add(img[:, :, 2], 40)
    return img

def cool_filter(img):
    img[:, :, 0] = cv2.add(img[:, :, 0], 40)
    return img

def bw_filter(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def hdr_filter(img):
    return cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)

def cartoon_filter(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 250, 250)
    return cv2.bitwise_and(color, color, mask=edges)


if frame is not None:

    img = Image.open(frame)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # apply filter
    if filter_name == "Beauty":
        img = beauty_filter(img)
    elif filter_name == "Warm":
        img = warm_filter(img)
    elif filter_name == "Cool":
        img = cool_filter(img)
    elif filter_name == "Cartoon":
        img = cartoon_filter(img)
    elif filter_name == "Black & White":
        img = bw_filter(img)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif filter_name == "HDR":
        img = hdr_filter(img)

    # show filtered result
    st.image(img, channels="BGR", width=720)

    # save photo
    if capture:
        filename = f"saved/photo_{int(time.time())}.jpg"
        cv2.imwrite(filename, img)
        st.success(f"📸 Photo Saved: {filename}")