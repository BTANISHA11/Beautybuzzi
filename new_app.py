import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageColor

# Utility Function to Sharpen Image
def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = np.clip(img_out / 255.0, 0, 1)
    img_out = np.uint8(img_out * 255)
    return img_out


# Hair Coloring Utility Function
def hair(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part in [12, 13]:
        image_hsv[:, :, :2] = tar_hsv[:, :, :2]
    else:
        image_hsv[:, :, 0] = tar_hsv[:, :, 0]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    changed[parsing != part] = image[parsing != part]
    if part == 17:
        changed = sharpen(changed)
    return changed

# Add Custom CSS for Sidebar Styling
st.markdown("""
    <style>
    /* Sidebar Styling */
    .css-1v0mbdj {
        padding-top: 20px;
    }
    .css-1v0mbdj .sidebar-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .css-1v0mbdj .sidebar-content a {
        font-size: 18px;
        margin: 12px 0;
        text-align: center;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #000;
        font-weight: 500;
        text-decoration: none;
        padding: 10px 0;
    }
    .css-1v0mbdj .sidebar-content a:hover {
        background-color: #f1f1f1;
        border-radius: 5px;
    }
    .css-1v0mbdj img {
        max-width: 100%;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Content with Navigation Items
st.sidebar.image("./imgs/logo.png", use_column_width=True)  # Add logo
st.sidebar.markdown("##")  # Spacing after the logo

# Navigation Items
page = st.sidebar.radio(
    ["Home", "Features", "About", "Occasions", "Healthcare"], 
    index=0
)

# Horizontal Line and Settings Section
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")

# Main Content Rendering
if page == "Home":
    render_home_page()  # Assuming you have this function in your code

    # Layout for Parameters and Image Display
    col1, col2 = st.columns([3, 1])

    with col1:
        # File Uploader for Image
        DEMO_IMG = 'imgs/116.jpg'
        img_file_buffer = st.file_uploader(
            "Upload your image", type=["png", "jpg", "jpeg"]
        )

        if img_file_buffer is not None:
            image = np.array(Image.open(img_file_buffer))
        else:
            image = np.array(Image.open(DEMO_IMG))

        st.subheader("Original Image")
        st.image(image, use_column_width=True)

    with col2:
        # Parameters Section
        st.header("Parameters")
        table = {'hair': 17, 'upper_lip': 12, 'lower_lip': 13}

        # Default Hair and Lip Colors
        hair_color = st.color_picker("Pick the Hair Color", "#000000")
        hair_color = ImageColor.getcolor(hair_color, "RGB")

        lip_color = st.color_picker("Pick the Lip Color", "#edbad1")
        lip_color = ImageColor.getcolor(lip_color, "RGB")

        colors = [hair_color, lip_color, lip_color]

        # Apply Makeup Button
        if st.button("Apply Makeup"):
            cp = 'cp/79999_iter.pth'  # Path to model
            ori = image.copy()

            h, w, _ = ori.shape
            image = cv2.resize(image, (1024, 1024))

            parsing = evaluate(image, cp)  # Assuming this is a custom function for image parsing
            parsing = cv2.resize(parsing, ori.shape[:2], interpolation=cv2.INTER_NEAREST)

            parts = [table['hair'], table['upper_lip'], table['lower_lip']]

            for part, color in zip(parts, colors):
                image = hair(image, parsing, part, color)

            st.subheader("Output Image")
            st.image(image, use_column_width=True)
