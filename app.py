import cv2
import os
import numpy as np
from skimage.filters import gaussian
from test import evaluate
import streamlit as st
from PIL import Image, ImageColor

# ----------------- Image Processing Functions ------------------ #

def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = np.clip(img_out / 255.0, 0, 1) * 255
    return np.array(img_out, dtype=np.uint8)

def apply_makeup(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0], tar_color[:, :, 1], tar_color[:, :, 2] = b, g, r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part in [12, 13]:
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    if part == 17:
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed

def apply_hairstyle_overlay(base_image, hairstyle_path):
    try:
        overlay = cv2.imread(hairstyle_path, cv2.IMREAD_UNCHANGED)
        overlay = cv2.resize(overlay, (base_image.shape[1], base_image.shape[0]))

        if overlay.shape[2] == 4:
            alpha = overlay[:, :, 3] / 255.0
            for c in range(3):
                base_image[:, :, c] = base_image[:, :, c] * (1 - alpha) + overlay[:, :, c] * alpha
        return base_image.astype(np.uint8)
    except Exception as e:
        st.warning(f"Error applying hairstyle: {e}")
        return base_image

# ----------------- Streamlit App ------------------ #

st.set_page_config(layout="wide")
st.title('💄 Virtual Makeup + Hairstyle Try-On App')

st.sidebar.title('🎨 Customization Panel')
st.sidebar.markdown("Upload a face image and apply makeup and hairstyle overlays.")

DEMO_IMAGE = 'imgs/116.jpg'
HAIRSTYLE_DIR = 'hairstyles/'  # ensure this folder exists

# Upload image
img_file_buffer = st.sidebar.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
if img_file_buffer:
    image = np.array(Image.open(img_file_buffer).convert("RGB"))
    demo_image = img_file_buffer
else:
    demo_image = DEMO_IMAGE
    image = np.array(Image.open(demo_image))

original_image = image.copy()
ori = original_image.copy()
h, w, _ = ori.shape
image = cv2.resize(image, (1024, 1024))

# Evaluate parsing mask
cp = 'cp/79999_iter.pth'
parsing = evaluate(demo_image, cp)
parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

# Color selections
hair_color = st.sidebar.color_picker('🖌️ Hair Color', '#000000')
lip_color = st.sidebar.color_picker('💋 Lip Color', '#edbad1')
hair_color = ImageColor.getcolor(hair_color, "RGB")
lip_color = ImageColor.getcolor(lip_color, "RGB")

parts = [17, 12, 13]
colors = [hair_color, lip_color, lip_color]

for part, color in zip(parts, colors):
    image = apply_makeup(image, parsing, part, color)

# # Hairstyle selection
# st.sidebar.markdown("### 💇 Select Hairstyle Overlay")

# try:
#     hairstyles = sorted([f for f in os.listdir(HAIRSTYLE_DIR) if f.endswith('.png')])
#     selected_hairstyle = st.sidebar.selectbox("Choose Hairstyle", ["None"] + hairstyles)

#     if selected_hairstyle != "None":
#         image = apply_hairstyle_overlay(image, os.path.join(HAIRSTYLE_DIR, selected_hairstyle))
# except FileNotFoundError:
#     st.warning("Hairstyle folder not found! Please create a 'hairstyles/' folder with PNG files.")

# Resize final output back to original dimensions
image = cv2.resize(image, (w, h))

# ----------------- Display Side by Side ------------------ #
col1, col2 = st.columns(2)
with col1:
    st.subheader("🧑 Original Image")
    st.image(original_image, use_column_width=True)

with col2:
    st.subheader("💅 Transformed Image")
    st.image(image, use_column_width=True)
