import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Beauty Camera", layout="wide")

st.markdown("""
    <h1 style='text-align:center; color:white;'>📸 Beauty Camera – Streamlit</h1>
""", unsafe_allow_html=True)

# Create folder
if not os.path.exists("Captured"):
    os.makedirs("Captured")


# ==================== FILTER FUNCTIONS ====================
def apply_filter(img, filter_name):
    if filter_name == "None":
        return img

    # Grey
    elif filter_name == "Grey":
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

    # Blur
    elif filter_name == "Blur":
        return cv2.GaussianBlur(img, (25, 25), 0)

    # Bright
    elif filter_name == "Bright":
        return cv2.convertScaleAbs(img, alpha=1.4, beta=40)

    # Contrast
    elif filter_name == "Contrast":
        return cv2.convertScaleAbs(img, alpha=1.8, beta=0)

    # Beauty Smooth
    elif filter_name == "Beauty Smooth":
        return cv2.bilateralFilter(img, 18, 75, 75)

    # Skin Glow (soft warm contrast)
    elif filter_name == "Skin Glow":
        blur = cv2.GaussianBlur(img, (0, 0), 25)
        glow = cv2.addWeighted(img, 1.4, blur, -0.4, 0)
        return glow

    # Warm Tone
    elif filter_name == "Warm Tone":
        warm = img.copy()
        warm[:, :, 2] = cv2.add(warm[:, :, 2], 40)   # Increase Red
        warm[:, :, 1] = cv2.add(warm[:, :, 1], 15)   # Slight Green
        return warm

    # Cool Tone
    elif filter_name == "Cool Tone":
        cool = img.copy()
        cool[:, :, 0] = cv2.add(cool[:, :, 0], 40)   # Increase Blue
        return cool

    # Pink Tint
    elif filter_name == "Pink Tint":
        pink = img.copy()
        pink[:, :, 2] = cv2.add(pink[:, :, 2], 70)
        pink[:, :, 1] = cv2.subtract(pink[:, :, 1], 30)
        return pink

    # HDR
    elif filter_name == "HDR":
        return cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)

    # Sharpen
    elif filter_name == "Sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)

    # Cartoon
    elif filter_name == "Cartoon":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(blur, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 15, 75, 75)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return cv2.bitwise_and(color, edges)

    # Edge Outline
    elif filter_name == "Edge Outline":
        edges = cv2.Canny(img, 80, 150)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    return img



# ==================== UI ====================
left, right = st.columns([1, 2])

with left:
    st.subheader("🎨 Apply Filter")
    filter_name = st.selectbox(
        "Select Filter",
        [
            "None", "Grey", "Blur", "Bright", "Contrast",
            "Beauty Smooth", "Skin Glow", "Warm Tone", "Cool Tone",
            "Pink Tint", "HDR", "Sharpen", "Cartoon", "Edge Outline"
        ]
    )

    capture_btn = st.button("📸 Capture Photo")


with right:
    st.subheader("📡 Live Camera")
    cam = st.camera_input("Start Camera")



# ==================== PROCESSING ====================
if cam:
    img = Image.open(cam)
    img = np.array(img)

    # Convert to BGR for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Apply filter
    output = apply_filter(img, filter_name)

    st.subheader("✨ Preview with Filter")
    st.image(output, channels="BGR")

    if capture_btn:
        filename = f"Captured/photo_{len(os.listdir('Captured'))+1}.jpg"
        cv2.imwrite(filename, output)
        st.success(f"Saved: {filename}")