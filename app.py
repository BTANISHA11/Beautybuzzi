import cv2
import os
import numpy as np
from PIL import Image, ImageColor
import streamlit as st
from test import evaluate
from recommend_hairstyle import get_face_shape, recommend_hairstyle, apply_hairstyle_overlay
from makeup import apply_makeup, apply_region_blend

st.set_page_config(layout="wide")
st.title('💄 Virtual Makeup + Hairstyle + Foundation Try-On App')

st.sidebar.title('🎨 Customization Panel')
st.sidebar.markdown("Upload an image and apply hair color, lipstick, foundation, and hairstyle.")

DEMO_IMAGE = 'imgs/116.jpg'
HAIRSTYLE_DIR = 'hairstyles/'

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
image = cv2.resize(image, (1024, 1024))

# Parsing with pre-trained model
cp = 'cp/79999_iter.pth'
parsing = evaluate(demo_image, cp)
parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

# Color pickers
hair_color = st.sidebar.color_picker('🖌️ Hair Color', '#000000')
lip_color = st.sidebar.color_picker('💋 Lip Color', '#edbad1')
foundation_color = st.sidebar.color_picker('🧴 Foundation Color (full face)', '#f4c2c2')

hair_color = ImageColor.getcolor(hair_color, "RGB")
lip_color = ImageColor.getcolor(lip_color, "RGB")
foundation_color = ImageColor.getcolor(foundation_color, "RGB")

# Apply hair and lips
for part, color in zip([17, 12, 13], [hair_color, lip_color, lip_color]):
    image = apply_makeup(image, parsing, part, color)

# Apply foundation to entire face area (part 1 includes nose)
# Apply foundation to full face including nose, brows, jaw
face_parts = [1, 2, 3, 10, 11]
foundation_mask = np.isin(parsing, face_parts)
image = apply_region_blend(image, foundation_mask, foundation_color, alpha=0.35)


# Hairstyle recommendation & overlay
if st.sidebar.button("🎯 Recommend & Apply Best Hairstyle"):
    face_shape = get_face_shape(original_image)
    st.sidebar.write(f"🧠 Detected Face Shape: **{face_shape}**")

    recommended_file = recommend_hairstyle(face_shape)
    if recommended_file:
        st.sidebar.success(f"✨ Recommended Hairstyle: `{recommended_file}`")
        hairstyle_path = os.path.join(HAIRSTYLE_DIR, recommended_file)
        image = apply_hairstyle_overlay(image, hairstyle_path)
    else:
        st.sidebar.warning("❌ No suitable hairstyle found.")

# Display results
col1, col2 = st.columns(2)
with col1:
    st.subheader("🧑 Original Image")
    st.image(original_image, use_column_width=True)

with col2:
    st.subheader("💅 Transformed Image")
    st.image(image, use_column_width=True)
