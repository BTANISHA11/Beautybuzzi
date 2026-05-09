import io
import os
import numpy as np
from PIL import Image, ImageColor
import streamlit as st

# OpenCV is optional at import time; show a friendly Streamlit error if missing
try:
    import cv2
except Exception as e:
    st.set_page_config(layout="wide")
    msg = """OpenCV (`cv2`) is not installed in this environment.
Install it with:
```
python -m pip install opencv-python
```
Or install all dependencies: `python -m pip install -r requirements.txt`"""
    st.error(msg)
    st.stop()
from test import evaluate
from recommend_hairstyle import get_face_shape, recommend_hairstyle, apply_hairstyle_overlay
from makeup import apply_makeup, apply_region_blend

def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #403b3e;
    }
    
    h1 {
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-align: left;
        background: linear-gradient(90deg, #b76e79, #7c3c50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
 /* Decorative elements */
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #b76e79, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    .stButton > button {
        border-radius: 25px !important;
        background: linear-gradient(90deg, #b76e79, #7c3c50) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
    }
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #b76e79, #7c3c50);
        color: white;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-left: 8px;
        vertical-align: middle;
    }
      </style>
    """, unsafe_allow_html=True)
    
    

st.set_page_config(layout="wide", page_title="BeautyBuzzi – Virtual Try-On", page_icon="💄")
local_css()

st.markdown('<h1>✨ Virtual Beauty Try-On</h1>', unsafe_allow_html=True)
st.markdown(
    """
            <div style="text-align: left; margin-bottom: 10px; font-family: 'Poppins', sans-serif;">
                <p style="font-size: 1.1rem; color: #7c3c50; font-weight: 300;">
                    Real-time AI-powered makeup & grooming – for everyone 💫
                </p>
            </div>
    """,
            unsafe_allow_html=True
)
        
# Decorative element
st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
        

with open("static/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

DEMO_IMAGE = 'imgs/116.jpg'
HAIRSTYLE_DIR = 'hairstyles/'

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🎨 Personalise Your Look")

# Gender selector
gender = st.sidebar.radio(
    "👤 I identify as",
    ["👩 Woman", "👨 Man", "🌈 Non-binary"],
    index=0,
)

st.sidebar.markdown("---")

# Upload image
img_file_buffer = st.sidebar.file_uploader("📤 Upload your photo", type=["jpg", "jpeg", "png"])
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

st.sidebar.markdown("---")

# ── Makeup / Grooming controls based on gender ────────────────────────────────
if "Man" in gender:
    st.sidebar.markdown("### 💈 Men's Grooming")
    hair_color    = st.sidebar.color_picker('🖤 Hair Color', '#1a0a00')
    beard_color   = st.sidebar.color_picker('🧔 Beard / Stubble Color', '#2c1a0e')
    brow_color    = st.sidebar.color_picker('✏️ Eyebrow Color', '#1a0a00')
    lip_color_hex = st.sidebar.color_picker('👄 Lip Tint (optional)', '#c77a6a')
    apply_lip     = st.sidebar.checkbox("Apply lip tint", value=False)
    foundation_color = st.sidebar.color_picker('🧴 Skin Tone / Foundation', '#f4c2a0')
    intensity     = st.sidebar.slider("🔆 Effect Intensity", 0.1, 1.0, 0.5, 0.05)
else:
    st.sidebar.markdown("### 💄 Makeup Studio")
    hair_color       = st.sidebar.color_picker('🖌️ Hair Color', '#000000')
    lip_color_hex    = st.sidebar.color_picker('💋 Lip Color', '#edbad1')
    foundation_color = st.sidebar.color_picker('🧴 Foundation', '#f4c2c2')
    eyeshadow_color  = st.sidebar.color_picker('👁️ Eyeshadow', '#d1a6e0')
    blush_color      = st.sidebar.color_picker('🌸 Blush', '#ffcccb')
    eyeliner_color   = st.sidebar.color_picker('✏️ Eyeliner', '#000000')
    intensity        = st.sidebar.slider("🔆 Effect Intensity", 0.1, 1.0, 0.7, 0.05)

st.sidebar.markdown("---")

# ── Apply makeup / grooming ──────────────────────────────────────────────────
hair_rgb        = ImageColor.getcolor(hair_color, "RGB")
foundation_rgb  = ImageColor.getcolor(foundation_color, "RGB")

if "Man" in gender:
    beard_rgb = ImageColor.getcolor(beard_color, "RGB")
    brow_rgb  = ImageColor.getcolor(brow_color, "RGB")
    lip_rgb   = ImageColor.getcolor(lip_color_hex, "RGB")

    # Hair
    image = apply_makeup(image, parsing, 17, hair_rgb)
    # Eyebrows (parts 2=left brow, 3=right brow)
    image = apply_makeup(image, parsing, 2, brow_rgb)
    image = apply_makeup(image, parsing, 3, brow_rgb)
    # Optional lip tint
    if apply_lip:
        for part in [12, 13]:
            image = apply_makeup(image, parsing, part, lip_rgb)
    # Foundation (light blend)
    face_parts = [1, 2, 3, 10, 11]
    foundation_mask = np.isin(parsing, face_parts)
    image = apply_region_blend(image, foundation_mask, foundation_rgb, alpha=intensity * 0.3)
else:
    lip_rgb      = ImageColor.getcolor(lip_color_hex, "RGB")
    eyeshadow_rgb = ImageColor.getcolor(eyeshadow_color, "RGB")
    blush_rgb    = ImageColor.getcolor(blush_color, "RGB")

    # Hair
    image = apply_makeup(image, parsing, 17, hair_rgb)
    # Lips (upper & lower)
    for part in [12, 13]:
        image = apply_makeup(image, parsing, part, lip_rgb)
    # Eyebrows
    for part in [2, 3]:
        image = apply_makeup(image, parsing, part, ImageColor.getcolor(hair_color, "RGB"))
    # Eyeshadow (left eye=4, right eye=5, left eyelid=6, right eyelid=7)
    for part in [4, 5]:
        image = apply_region_blend(image, parsing == part, eyeshadow_rgb, alpha=intensity * 0.5)
    # Blush (cheeks – approximate using face sides via parsing part 1)
    face_mask = parsing == 1
    image = apply_region_blend(image, face_mask, blush_rgb, alpha=intensity * 0.15)
    # Foundation
    face_parts = [1, 2, 3, 10, 11]
    foundation_mask = np.isin(parsing, face_parts)
    image = apply_region_blend(image, foundation_mask, foundation_rgb, alpha=intensity * 0.35)

# ── Display results ──────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📷 Original")
    st.image(original_image, use_column_width=True)

with col2:
    label = "💈 Groomed Look" if "Man" in gender else "💄 Transformed Look"
    st.markdown(f"#### {label}")
    st.image(image, use_column_width=True)

# Download button
result_pil = Image.fromarray(image.astype(np.uint8))
buf = io.BytesIO()
result_pil.save(buf, format="PNG")
buf.seek(0)
st.download_button(
    label="⬇️ Download Result",
    data=buf,
    file_name="beautybuzzi_result.png",
    mime="image/png",
)

# ── Quick tip ────────────────────────────────────────────────────────────────
st.markdown("---")
if "Man" in gender:
    st.info("💡 **Men's tip:** Use the beard color picker to try different facial hair shades before your next barber visit!")
else:
    st.info("💡 **Pro tip:** Try matching your blush color with your lip color for a natural, cohesive look!")
