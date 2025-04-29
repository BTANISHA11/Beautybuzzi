import os
import cv2
import numpy as np
from skimage.filters import gaussian
import streamlit as st
from PIL import Image
from static.constants import DEFAULT_IMAGE_PATH
from test import evaluate  # Assumes a parsing model is available

# Set page config
st.set_page_config(page_title="Beauty Buzz - Occasions", page_icon="💄", layout="wide")

# Custom CSS styling
def add_custom_css():
    custom_css = """
    <style>
    body {
        background-color: #f8f9fa;
        font-family: "Arial", sans-serif;
    }

    .header {
        text-align: center;
        font-size: 3em;
        color: #d63384;
        margin-top: 20px;
    }

    .subheader {
        font-size: 1.5em;
        color: #6f42c1;
    }

    .occasion-title {
        font-size: 1.5em;
        color: #495057;
        margin-bottom: 10px;
    }

    footer {
        text-align: center;
        font-size: 1em;
        color: #adb5bd;
        margin-top: 50px;
        border-top: 1px solid #dee2e6;
        padding-top: 10px;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 1.2em;
        color: #868e96;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Image sharpening
def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = img_out / 255.0
    img_out = np.clip(img_out, 0, 1) * 255
    return np.array(img_out, dtype=np.uint8)

# Makeup application function
def apply_makeup(image, parsing, part, color):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    if part == 17:  # Hair
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed

# Main Streamlit app
def render_occasions_page():
    add_custom_css()

    st.markdown("<h1 class='header'>💄 Beauty Buzz: Makeup for Every Occasion 💄</h1>", unsafe_allow_html=True)
    st.write("")

    st.markdown("<h3 class='subheader'>Choose your Occasion</h3>", unsafe_allow_html=True)

    occasion_params = {
        "Office Day": {"hair_color": [128, 128, 128], "lip_color": [255, 182, 193], "foundation_color": [255, 224, 189]},
        "Cocktail Party": {"hair_color": [0, 0, 255], "lip_color": [255, 0, 0], "foundation_color": [255 , 204, 204]},
        "Wedding": {"hair_color": [255, 215, 0], "lip_color": [139, 0, 0], "foundation_color": [255, 228, 196]},
        "Birthday Party": {"hair_color": [255, 20, 147], "lip_color": [255, 165, 0], "foundation_color": [255, 182, 193]},
        "Night Out": {"hair_color": [0, 0, 0], "lip_color": [128, 0, 128], "foundation_color": [255, 228, 196]},
        "Casual Day": {"hair_color": [139, 69, 19], "lip_color": [255, 222, 173], "foundation_color": [255, 239, 204]},
    }

    occasion = st.selectbox("Select an Occasion", list(occasion_params.keys()))

    image_mapping = {
        "Office Day": "office_day.jpg",
        "Cocktail Party": "cocktail_party.jpg",
        "Wedding": "wedding.jpg",
        "Birthday Party": "birthday_party.jpg",
        "Night Out": "night_out.jpg",
        "Casual Day": "casual_day.jpg",
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(script_dir, "images")
        img_path = os.path.join(image_folder, image_mapping[occasion])
        st.image(Image.open(img_path), caption=f"{occasion} Look")

    with col2:
        st.markdown(f"<h4 class='occasion-title'>{occasion} Makeup Suggestions:</h4>", unsafe_allow_html=True)
        suggestions = {
            "Office Day": "- **Foundation**: Matte, lightweight\n- **Lipstick**: Nude shades\n- **Eyeliner**: Minimalistic\n- **Blush**: Soft pink or peach",
            "Cocktail Party": "- **Foundation**: High-coverage\n- **Lipstick**: Bold red or berry tones\n- **Eyeliner**: Winged or cat-eye\n- **Blush**: Rosy tones",
            "Wedding": "- **Foundation**: Dewy finish\n- **Lipstick**: Deep red or maroon\n- **Eyeliner**: Heavy, bridal\n- **Blush**: Rich rose",
            "Birthday Party": "- **Foundation**: Luminous\n- **Lipstick**: Coral or pink\n- **Eyeliner**: Glitter or metallic\n- **Blush**: Bright pink",
            "Night Out": "- **Foundation**: High-definition\n- **Lipstick**: Dark plum or wine shades\n- **Eyeliner**: Smokey eyes\n- **Blush**: Darker peach",
            "Casual Day": "- **Foundation**: Tinted moisturizer\n- **Lipstick**: Lip balm or nude gloss\n- **Eyeliner**: None or light pencil\n- **Blush**: Subtle pink",
        }
        st.markdown(suggestions[occasion])

    img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    original_image = np.array(Image.open(img_file_buffer)) if img_file_buffer else np.array(Image.open(DEFAULT_IMAGE_PATH))
    transformed_image = original_image.copy()

    cp = 'cp/79999_iter.pth'
    parsing = evaluate(img_file_buffer if img_file_buffer else DEFAULT_IMAGE_PATH, cp)
    parsing = cv2.resize(parsing, (1024, 1024), interpolation=cv2.INTER_NEAREST)

    image_resized = cv2.resize(transformed_image, (1024, 1024))

    params = occasion_params[occasion]
    hair_color = params["hair_color"]
    lip_color = params["lip_color"]
    foundation_color = params["foundation_color"]

    if st.button(f"Apply Makeup for {occasion}"):
        table = {"hair": 17, "upper_lip": 12, "lower_lip": 13, "eyeliner": 14, "eyeshadow": 15, "blush": 16, "foundation": 18}
        colors = [hair_color, lip_color, lip_color, lip_color, lip_color, lip_color, foundation_color]

        for part, color in zip(table.values(), colors):
            image_resized = apply_makeup(image_resized, parsing, part, color)

        # Resize back to original
        final_transformed = cv2.resize(image_resized, (original_image.shape[1], original_image.shape[0]))

        # Display side by side
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(original_image)

        with col2:
            st.subheader("Transformed Image")
            st.image(final_transformed)

    st.markdown("<footer>© 2024 BeautyBuzz. All rights reserved.</footer>", unsafe_allow_html=True)

# Run the app
render_occasions_page()
