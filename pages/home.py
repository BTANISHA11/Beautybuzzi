import cv2
import numpy as np
from skimage.filters import gaussian
import streamlit as st
from PIL import Image, ImageColor
from static.constants import DEFAULT_IMAGE_PATH, HAIR_COLOR_DEFAULT, MAIN_COLOR
from test import evaluate  # Assuming evaluate is a function that processes the image

# Function to include custom CSS
def add_custom_css(css_path="./static/styles.css"):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to sharpen the image
def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)

# Function to apply hair color
def hair(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r
    np.repeat(parsing[:, :, np.newaxis], 3, axis=2)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if part == 17:
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed

# Streamlit app
def render_home_page():
    # Load custom CSS for styling
    add_custom_css()

    # Title and Description
    st.title('Virtual Makeup Application 💄')
    st.markdown("""
        **Welcome to Beauty Buzz!**  
        Use our AI-powered makeup tool to transform your look. Upload an image, select your desired hair and lip colors, and let the magic happen!
    """)

    # Sidebar for parameters
    st.sidebar.title('Makeup Parameters')
    table = {
        'hair': 17,
        'upper_lip': 12,
        'lower_lip': 13,  # Corrected key name
    }

    img_file_buffer = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))
    else:
        demo_image = DEFAULT_IMAGE_PATH
        image = np.array(Image.open(demo_image))

    new_image = image.copy()

    st.subheader('Original Image')
    st.image(image)

    # Load model for parsing
    cp = 'cp/79999_iter.pth'
    ori = image.copy()
    h, w, _ = ori.shape
    image = cv2.resize(image, (1024, 1024))

    parsing = evaluate(img_file_buffer if img_file_buffer else demo_image, cp)
    parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

    # Hair and lip color pickers
    hair_color = st.sidebar.color_picker('Pick the Hair Color', HAIR_COLOR_DEFAULT)
    hair_color = ImageColor.getcolor(hair_color, "RGB")

    lip_color = st.sidebar.color_picker('Pick the Lip Color', MAIN_COLOR)
    lip_color = ImageColor.getcolor(lip_color, "RGB")

    colors = [hair_color , lip_color, lip_color]

    # Button to apply makeup
    if st.sidebar.button("Apply Makeup"):
        for part, color in zip([table['hair'], table['upper_lip'], table['lower_lip']], colors):  # Corrected key name
            image = hair(image, parsing, part, color)

        image = cv2.resize(image, (w, h))

        st.subheader('Output Image')
        st.image(image)

    # Footer with copyright information
    st.markdown("<footer>© 2024 BeautyBuzz. All rights reserved.</footer>", unsafe_allow_html=True)

# Run the homepage rendering function
render_home_page()