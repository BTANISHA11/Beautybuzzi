import io
import os
from datetime import datetime
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
python -m pip install opencv-python-headless
```
Or install all dependencies: `python -m pip install -r requirements.txt`"""
    st.error(msg)
    st.stop()
from test import evaluate
from recommend_hairstyle import get_face_shape, recommend_hairstyle, apply_hairstyle_overlay
from makeup import apply_makeup, apply_region_blend
from mediapipe_makeup import (
    get_landmarks, apply_lipstick, apply_eyeshadow, apply_blush,
    apply_eyeliner, apply_highlighter, apply_beard_tint, apply_brow_tint,
    detect_skin_tone, match_foundation, MEDIAPIPE_OK,
)

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
                    Real-time AI-powered makeup and grooming for women and men 💫
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

if "saved_looks" not in st.session_state:
    st.session_state.saved_looks = []

WOMEN_PRESETS = {
    "Custom": {},
    "Soft Glam": {
        "hair_color": "#3d2418",
        "lip_color": "#b65f73",
        "foundation_color": "#e4b49f",
        "eyeshadow_color": "#b88ca9",
        "blush_color": "#e8a0a6",
        "eyeliner_color": "#2a1b1b",
        "intensity": 0.62,
    },
    "Bridal Glow": {
        "hair_color": "#2a1a14",
        "lip_color": "#c56f84",
        "foundation_color": "#ecc1ad",
        "eyeshadow_color": "#d7b1bf",
        "blush_color": "#f1b0b8",
        "eyeliner_color": "#201515",
        "intensity": 0.72,
    },
    "Office Polished": {
        "hair_color": "#2e241f",
        "lip_color": "#9b6870",
        "foundation_color": "#ddb09d",
        "eyeshadow_color": "#b19cab",
        "blush_color": "#dca1a5",
        "eyeliner_color": "#352829",
        "intensity": 0.45,
    },
    "Date Night": {
        "hair_color": "#1d1412",
        "lip_color": "#8e2d49",
        "foundation_color": "#dca78d",
        "eyeshadow_color": "#7d536d",
        "blush_color": "#d17a88",
        "eyeliner_color": "#120d0d",
        "intensity": 0.82,
    },
}

MEN_PRESETS = {
    "Custom": {},
    "Fresh Grooming": {
        "hair_color": "#251913",
        "beard_color": "#3b2a21",
        "brow_color": "#251913",
        "lip_color": "#b77d71",
        "foundation_color": "#d9ab8f",
        "apply_lip": False,
        "intensity": 0.42,
    },
    "Sharp Beard": {
        "hair_color": "#16110f",
        "beard_color": "#231713",
        "brow_color": "#16110f",
        "lip_color": "#9f6c63",
        "foundation_color": "#c99980",
        "apply_lip": False,
        "intensity": 0.60,
    },
    "Camera Ready": {
        "hair_color": "#201611",
        "beard_color": "#34231a",
        "brow_color": "#201611",
        "lip_color": "#c48b7d",
        "foundation_color": "#ddb09b",
        "apply_lip": True,
        "intensity": 0.52,
    },
}

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🎨 Personalise Your Look")

# Gender selector
gender = st.sidebar.radio(
    "👤 I identify as",
    ["👩 Woman", "👨 Man"],
    index=0,
)

is_male = "Man" in gender

st.sidebar.markdown("---")

if is_male:
    preset_name = st.sidebar.selectbox("✨ Smart Look Preset", list(MEN_PRESETS.keys()))
    active_preset = MEN_PRESETS[preset_name]
else:
    preset_name = st.sidebar.selectbox("✨ Smart Look Preset", list(WOMEN_PRESETS.keys()))
    active_preset = WOMEN_PRESETS[preset_name]

compare_ratio = st.sidebar.slider("🪞 Before / After Slider", 0, 100, 50)

# ── Input mode ────────────────────────────────────────────────────────────────
input_mode = st.sidebar.radio(
    "📥 Input Mode",
    ["📤 Upload Photo", "📷 Webcam Snapshot"],
    horizontal=True,
)
img_file_buffer = None
webcam_img = None
if input_mode == "📤 Upload Photo":
    img_file_buffer = st.sidebar.file_uploader("Choose your photo", type=["jpg", "jpeg", "png"])
else:
    webcam_img = st.sidebar.camera_input("📸 Take a snapshot")

if img_file_buffer:
    image = np.array(Image.open(img_file_buffer).convert("RGB"))
    demo_image = img_file_buffer
elif webcam_img:
    image = np.array(Image.open(webcam_img).convert("RGB"))
    demo_image = webcam_img
else:
    demo_image = DEMO_IMAGE
    image = np.array(Image.open(demo_image).convert("RGB"))

show_foundation = st.sidebar.checkbox("🎨 Foundation Shade Match", value=False)

original_image = image.copy()
image = cv2.resize(image, (1024, 1024))

# Parsing with pre-trained BiSeNet model (hair segmentation + fallback makeup)
cp = 'cp/79999_iter.pth'
parsing = evaluate(demo_image, cp)
parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

# MediaPipe landmark detection (precise makeup blending)
lm = get_landmarks(original_image)
mp_ok = lm is not None

st.sidebar.markdown("---")

# ── Makeup / Grooming controls based on gender ────────────────────────────────
if is_male:
    st.sidebar.markdown("### 💈 Men's Grooming")
    hair_color    = st.sidebar.color_picker('🖤 Hair Color', active_preset.get("hair_color", '#1a0a00'))
    beard_color   = st.sidebar.color_picker('🧔 Beard / Stubble Color', active_preset.get("beard_color", '#2c1a0e'))
    brow_color    = st.sidebar.color_picker('✏️ Eyebrow Color', active_preset.get("brow_color", '#1a0a00'))
    lip_color_hex = st.sidebar.color_picker('👄 Lip Tint (optional)', active_preset.get("lip_color", '#c77a6a'))
    apply_lip     = st.sidebar.checkbox("Apply lip tint", value=active_preset.get("apply_lip", False))
    foundation_color = st.sidebar.color_picker('🧴 Skin Tone / Foundation', active_preset.get("foundation_color", '#f4c2a0'))
    intensity     = st.sidebar.slider("🔆 Effect Intensity", 0.1, 1.0, active_preset.get("intensity", 0.5), 0.05)
else:
    st.sidebar.markdown("### 💄 Makeup Studio")
    hair_color       = st.sidebar.color_picker('🖌️ Hair Color', active_preset.get("hair_color", '#000000'))
    lip_color_hex    = st.sidebar.color_picker('💋 Lip Color', active_preset.get("lip_color", '#edbad1'))
    foundation_color = st.sidebar.color_picker('🧴 Foundation', active_preset.get("foundation_color", '#f4c2c2'))
    eyeshadow_color  = st.sidebar.color_picker('👁️ Eyeshadow', active_preset.get("eyeshadow_color", '#d1a6e0'))
    blush_color      = st.sidebar.color_picker('🌸 Blush', active_preset.get("blush_color", '#ffcccb'))
    eyeliner_color   = st.sidebar.color_picker('✏️ Eyeliner', active_preset.get("eyeliner_color", '#000000'))
    intensity        = st.sidebar.slider("🔆 Effect Intensity", 0.1, 1.0, active_preset.get("intensity", 0.7), 0.05)

st.sidebar.markdown("---")

# ── Apply makeup — dual-path: MediaPipe (precise) or BiSeNet (fallback) ───────
hair_rgb       = ImageColor.getcolor(hair_color, "RGB")
foundation_rgb = ImageColor.getcolor(foundation_color, "RGB")

if is_male:
    beard_rgb = ImageColor.getcolor(beard_color, "RGB")
    brow_rgb  = ImageColor.getcolor(brow_color, "RGB")
    lip_rgb   = ImageColor.getcolor(lip_color_hex, "RGB")

    if mp_ok:
        # ── MediaPipe path ── precise jaw/brow landmark blending ──────────────
        image = apply_beard_tint(image, lm, beard_rgb, intensity=intensity * 0.45)
        image = apply_brow_tint(image, lm, brow_rgb, intensity=intensity * 0.70)
        if apply_lip:
            image = apply_lipstick(image, lm, lip_rgb, intensity=intensity * 0.50)
        # Hair colour via BiSeNet (MediaPipe does not segment hair strands)
        image = apply_makeup(image, parsing, 17, hair_rgb)
    else:
        # ── BiSeNet fallback ───────────────────────────────────────────────────
        image = apply_makeup(image, parsing, 17, hair_rgb)
        image = apply_makeup(image, parsing, 2, brow_rgb)
        image = apply_makeup(image, parsing, 3, brow_rgb)
        if apply_lip:
            for part in [12, 13]:
                image = apply_makeup(image, parsing, part, lip_rgb)
        face_parts = [1, 2, 3, 10, 11]
        foundation_mask = np.isin(parsing, face_parts)
        image = apply_region_blend(image, foundation_mask, foundation_rgb, alpha=intensity * 0.3)

else:
    lip_rgb       = ImageColor.getcolor(lip_color_hex, "RGB")
    eyeshadow_rgb = ImageColor.getcolor(eyeshadow_color, "RGB")
    blush_rgb     = ImageColor.getcolor(blush_color, "RGB")
    eyeliner_rgb  = ImageColor.getcolor(eyeliner_color, "RGB")

    if mp_ok:
        # ── MediaPipe path ── polygon-precise with LAB texture preservation ───
        image = apply_lipstick(image, lm, lip_rgb, intensity=intensity * 0.75)
        image = apply_eyeshadow(image, lm, eyeshadow_rgb, intensity=intensity * 0.45)
        image = apply_blush(image, lm, blush_rgb, intensity=intensity * 0.38)
        image = apply_eyeliner(
            image, lm, eyeliner_rgb,
            thickness=max(1, int(intensity * 3)),
            intensity=intensity * 0.90,
        )
        image = apply_highlighter(image, lm, intensity=intensity * 0.28)
        image = apply_brow_tint(image, lm, hair_rgb, intensity=intensity * 0.55)
        # Hair colour via BiSeNet
        image = apply_makeup(image, parsing, 17, hair_rgb)
    else:
        # ── BiSeNet fallback ───────────────────────────────────────────────────
        image = apply_makeup(image, parsing, 17, hair_rgb)
        for part in [12, 13]:
            image = apply_makeup(image, parsing, part, lip_rgb)
        for part in [2, 3]:
            image = apply_makeup(image, parsing, part, hair_rgb)
        for part in [4, 5]:
            image = apply_region_blend(image, parsing == part, eyeshadow_rgb, alpha=intensity * 0.5)
        face_mask = parsing == 1
        image = apply_region_blend(image, face_mask, blush_rgb, alpha=intensity * 0.15)
        face_parts = [1, 2, 3, 10, 11]
        foundation_mask = np.isin(parsing, face_parts)
        image = apply_region_blend(image, foundation_mask, foundation_rgb, alpha=intensity * 0.35)

# ── Display results ───────────────────────────────────────────────────────────
method_badge = (
    '<span class="badge">✨ MediaPipe</span>'
    if mp_ok else
    '<span class="badge" style="background:#888;">BiSeNet</span>'
)
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📷 Original")
    st.image(original_image, width="stretch")

with col2:
    label = "💈 Groomed Look" if is_male else "💄 Transformed Look"
    st.markdown(f"#### {label} {method_badge}", unsafe_allow_html=True)
    st.image(image, width="stretch")

compare_base = cv2.resize(original_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)
compare_alpha = np.clip(compare_ratio / 100.0, 0.0, 1.0)
compare_preview = cv2.addWeighted(compare_base, 1.0 - compare_alpha, image, compare_alpha, 0)

st.markdown("### 🪞 Compare Blend")
st.caption("Slide toward 0 to see the original and toward 100 to see the applied look.")
st.image(compare_preview, width="stretch")

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

save_cols = st.columns([1, 1.4])
with save_cols[0]:
    if st.button("❤️ Save This Look"):
        look_buf = io.BytesIO()
        result_pil.save(look_buf, format="PNG")
        st.session_state.saved_looks.insert(
            0,
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "gender": gender,
                "preset": preset_name,
                "engine": "MediaPipe" if mp_ok else "BiSeNet",
                "intensity": intensity,
                "image_bytes": look_buf.getvalue(),
            },
        )
        st.session_state.saved_looks = st.session_state.saved_looks[:6]
        st.success("Look saved to this session.")
with save_cols[1]:
    st.markdown(
        f"""
        <div style="background:white;border-radius:12px;padding:12px 16px;box-shadow:0 2px 10px rgba(0,0,0,0.06);">
            <b>AI Beauty Profile</b><br>
            <span style="color:#666;font-size:0.9rem;">Preset: {preset_name} · Engine: {'MediaPipe' if mp_ok else 'BiSeNet'} · Intensity: {intensity:.2f}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Foundation shade matching ─────────────────────────────────────────────────
if show_foundation:
    st.markdown("---")
    st.markdown("### 🎨 Foundation Shade Match")
    if mp_ok:
        skin_lab, skin_rgb = detect_skin_tone(original_image, lm)
        if skin_lab is not None:
            skin_hex = "#{:02x}{:02x}{:02x}".format(
                int(skin_rgb[0]), int(skin_rgb[1]), int(skin_rgb[2])
            )
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:16px 22px;
                        box-shadow:0 3px 14px rgba(183,110,121,0.09);margin-bottom:14px;">
                <b>Detected Skin Tone (cheek sample):</b>&nbsp;
                <span style="display:inline-block;width:26px;height:26px;border-radius:50%;
                             background:{skin_hex};border:2px solid #ddd;
                             vertical-align:middle;margin:0 8px;"></span>
                <code>{skin_hex.upper()}</code>
            </div>
            """, unsafe_allow_html=True)

            top3 = match_foundation(skin_lab)
            shade_cols = st.columns(3)
            medals = ["🥇 Best Match", "🥈 Close Match", "🥉 Alternative"]
            for i, (dist, name, hex_col) in enumerate(top3):
                with shade_cols[i]:
                    score = max(0, 100 - int(dist))
                    st.markdown(f"""
                    <div style="background:white;border-radius:12px;padding:16px;text-align:center;
                                box-shadow:0 2px 10px rgba(0,0,0,0.07);">
                        <span style="font-size:0.8rem;font-weight:600;color:#7c3c50;">{medals[i]}</span><br>
                        <b style="font-size:1rem;">{name}</b><br>
                        <div style="width:58px;height:58px;border-radius:50%;background:{hex_col};
                                    margin:10px auto;border:3px solid #eee;"></div>
                        <code style="font-size:0.82rem;">{hex_col.upper()}</code><br>
                        <span style="font-size:0.75rem;color:#888;">Match: {score}%</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Couldn't sample skin tone — try a photo with clearly visible cheeks.")
    else:
        if MEDIAPIPE_OK:
            st.warning("No face detected in this photo. Try a clearer, well-lit portrait.")
        else:
            st.info("Install MediaPipe for foundation matching: `pip install mediapipe`")

# ── Status + tips ─────────────────────────────────────────────────────────────
st.markdown("---")
if mp_ok:
    st.success(
        "✨ **MediaPipe active** — 468-landmark facial mesh · LAB texture-preserving blending · "
        "precise lip polygon · feathered eyeshadow · jaw-contour beard"
    )
elif MEDIAPIPE_OK:
    st.warning("No face detected. Using BiSeNet segmentation. Try a clearer photo.")
else:
    st.info("💡 Install MediaPipe for landmark-precise rendering: `pip install mediapipe`")

if is_male:
    st.info("💡 **Men's tip:** Use the beard colour picker to simulate stubble, short beard, or full beard shades before your next barber visit.")
else:
    st.info("💡 **Pro tip:** Try matching your blush to your lip colour for a cohesive, natural look.")

if st.session_state.saved_looks:
    st.markdown("### ❤️ Saved Looks")
    saved_cols = st.columns(min(3, len(st.session_state.saved_looks)))
    for idx, look in enumerate(st.session_state.saved_looks[:3]):
        with saved_cols[idx % len(saved_cols)]:
            st.image(look["image_bytes"], width="stretch")
            st.caption(f"{look['preset']} · {look['engine']} · {look['gender']} · {look['timestamp']}")
