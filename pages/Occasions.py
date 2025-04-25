import os
import cv2
import numpy as np
from skimage.filters import gaussian
import streamlit as st
from PIL import Image
from static.constants import DEFAULT_IMAGE_PATH
from test import evaluate  # Assuming evaluate processes the image and returns parsing

# Set page config
st.set_page_config(page_title="Beauty Buzz - Occasions", page_icon="💄", layout="wide")

# Embed custom CSS
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

# Function to include custom CSS
def add_custom_css():
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)

# Function to sharpen the image
def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = img_out / 255.0
    img_out = np.clip(img_out, 0, 1) * 255
    return np.array(img_out, dtype=np.uint8)

# Function to apply makeup
def apply_makeup(image, parsing, part, color):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part in [12, 13]:  # Lips
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    elif part in [14]:  # Eyeliner
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    elif part in [15]:  # Eyeshadow
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    elif part in [16]:  # Blush
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    else:  # Hair
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    if part == 17:  # Hair
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed

# Streamlit app
def render_occasions_page():
    # Load custom CSS for styling
    add_custom_css()

    # Title and Description
    st.markdown("<h1 class='header'>💄 Beauty Buzz: Makeup for Every Occasion 💄</h1>", unsafe_allow_html=True)
    st.write("")

    # Occasion Options
    st.markdown("<h3 class='subheader'>Choose your Occasion</h3>", unsafe_allow_html=True)
    
    # Fixed parameters for occasions
    occasion_params = {
        "Office Day": {"hair_color": [128, 128, 128], "lip_color": [255, 182, 193], "foundation_color": [255, 224, 189]},  # Grey hair, pink lips, light foundation
        "Cocktail Party": {"hair_color": [0, 0, 255], "lip_color": [255, 0, 0], "foundation_color": [255 , 204, 204]},      # Blue hair, red lips, light pink foundation
        "Wedding": {"hair_color": [255, 215, 0], "lip_color": [139, 0, 0], "foundation_color": [255, 228, 196]},          # Gold hair, deep red lips, peach foundation
        "Birthday Party": {"hair_color": [255, 20, 147], "lip_color": [255, 165, 0], "foundation_color": [255, 182, 193]},# Pink hair, orange lips, rosy foundation
        "Night Out": {"hair_color": [0, 0, 0], "lip_color": [128, 0, 128], "foundation_color": [255, 228, 196]},          # Black hair, purple lips, tan foundation
        "Casual Day": {"hair_color": [139, 69, 19], "lip_color": [255, 222, 173], "foundation_color": [255, 239, 204]},   # Brown hair, nude lips, light foundation
    }

    # Dropdown to select an occasion
    occasion = st.selectbox("Select an Occasion", list(occasion_params.keys()))

    # Display Occasion Image and Details
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
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(script_dir, "images")
        
        # Display occasion image
        image = Image.open(os.path.join(image_folder, image_mapping[occasion]))
        st.image(image, caption=f"{occasion} Look")

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
        st.write(suggestions[occasion])

    # File upload for image
    img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if img_file_buffer:
        image = np.array(Image.open(img_file_buffer))
    else:
        image = np.array(Image.open(DEFAULT_IMAGE_PATH))

    st.subheader("Original Image")
    st.image(image)

    # Load model for parsing
    cp = 'cp/79999_iter.pth'
    ori = image.copy()
    h, w, _ = ori.shape
    image = cv2.resize(image, (1024, 1024))

    parsing = evaluate(img_file_buffer if img_file_buffer else DEFAULT_IMAGE_PATH, cp)
    parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

    # Get fixed parameters for the selected occasion
    params = occasion_params[occasion]
    hair_color = params["hair_color"]
    lip_color = params["lip_color"]
    foundation_color = params["foundation_color"]

    # Apply makeup on button click
    if st.button(f"Apply Makeup for {occasion}"):
        table = {"hair": 17, "upper_lip": 12, "lower_lip": 13, "eyeliner": 14, " eyeshadow": 15, "blush": 16, "foundation": 18}
        colors = [hair_color, lip_color, lip_color, lip_color, lip_color, lip_color, foundation_color]  # Adjust as needed

        for part, color in zip(table.values(), colors):
            image = apply_makeup(image, parsing, part, color)

        image = cv2.resize(image, (w, h))
        st.subheader("Transformed Image")
        st.image(image)

    # Footer with copyright information
    st.markdown("<footer>© 2024 BeautyBuzz. All rights reserved.</footer>", unsafe_allow_html=True)
# Run the occasions page rendering function
render_occasions_page()