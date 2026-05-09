import os
import io
import cv2
import numpy as np
from skimage.filters import gaussian
import streamlit as st
from PIL import Image
from static.constants import DEFAULT_IMAGE_PATH
from test import evaluate

st.set_page_config(page_title="BeautyBuzz – Occasions", page_icon="🎭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600&display=swap');
body, [class*="css"] { font-family: 'Poppins', sans-serif; }
h1 {
    font-family: 'Playfair Display', serif !important;
    background: linear-gradient(90deg, #b76e79, #7c3c50);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.8rem !important; margin-bottom: 0.3rem !important;
}
.occ-card {
    background: white; border-radius: 16px; padding: 18px 22px;
    box-shadow: 0 4px 18px rgba(183,110,121,0.10);
    border-left: 5px solid #b76e79; margin-bottom: 14px;
}
.tip-badge {
    display: inline-block; background: #fce4e8; color: #7c3c50;
    border-radius: 20px; padding: 3px 12px; font-size: 0.82rem;
    font-weight: 600; margin: 2px 4px;
}
.stButton > button {
    border-radius: 25px !important;
    background: linear-gradient(90deg, #b76e79, #7c3c50) !important;
    color: white !important; border: none !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

WOMEN_OCCASIONS = {
    "💼 Office / Work": {
        "emoji": "💼",
        "desc": "Polished, professional and put-together. Let your work speak louder than your contour.",
        "lip":  [180, 130, 140],
        "hair": [90, 60, 40],
        "tags": ["Minimal", "Natural", "SPF Essential"],
        "tips": [
            "Stick to neutral or mauve lips — avoid bold reds.",
            "Matte or satin finish foundation for longevity through meetings.",
            "A single coat of brown/black mascara keeps eyes awake.",
            "Set everything with a translucent powder for 8-hour staying power.",
        ],
        "products": ["Matte foundation", "Nude lip liner + lipstick", "Brown mascara", "Setting powder", "Tinted SPF moisturiser"],
    },
    "💍 Wedding": {
        "emoji": "💍",
        "desc": "Timeless elegance. Whether you're the bride, guest or bridesmaid — look luminous all day.",
        "lip":  [80, 30, 100],
        "hair": [200, 160, 100],
        "tags": ["Glam", "Romantic", "Long-Wearing"],
        "tips": [
            "Primer is non-negotiable — you'll be photographed all day.",
            "Waterproof mascara and eyeliner so tears of joy don't ruin the look.",
            "For the bride: a dewy base catches the light beautifully in photos.",
            "Setting spray is your best friend.",
        ],
        "products": ["Long-wear foundation", "Deep rose lipstick", "Waterproof mascara", "Highlighter", "Setting spray"],
    },
    "🍸 Date Night": {
        "emoji": "🍸",
        "desc": "Effortlessly alluring. A little drama goes a long way.",
        "lip":  [60, 20, 90],
        "hair": [40, 20, 60],
        "tags": ["Sultry", "Bold Lip", "Smoky Eye"],
        "tips": [
            "Berry or wine lips with a nude eye, or bold eye with a nude lip — pick one focal point.",
            "A dab of highlighter on the cupid's bow makes lips look fuller.",
            "Blot lipstick and reapply for longer wear before dinner.",
            "Perfume behind the ears, wrists and the back of the knees.",
        ],
        "products": ["Berry/wine lipstick", "Eyeshadow palette (warm nudes + deep tones)", "Illuminating highlighter", "Volumising mascara", "Perfume"],
    },
    "🎉 Birthday / Party": {
        "emoji": "🎉",
        "desc": "It's your moment — be bold, be glam, be you.",
        "lip":  [60, 100, 200],
        "hair": [200, 80, 150],
        "tags": ["Fun", "Glitter", "Festive"],
        "tips": [
            "Glitter topper over eyeshadow = instant party look.",
            "Coral or hot-pink lips are photogenic and festive.",
            "Bright blush adds a playful flush under flash photography.",
            "Body shimmer on collarbones and shoulders for a glow-up.",
        ],
        "products": ["Bright lip colour", "Glitter eyeshadow", "Luminous blush", "Body shimmer", "Volumising mascara"],
    },
    "🌸 Casual Day Out": {
        "emoji": "🌸",
        "desc": "Effortless, fresh and comfortable. Less is more.",
        "lip":  [200, 160, 170],
        "hair": [120, 80, 50],
        "tags": ["No-Makeup Makeup", "Fresh", "Skin-First"],
        "tips": [
            "Tinted moisturiser instead of foundation — let skin breathe.",
            "A lip tint + balm gives just enough colour with comfort.",
            "Mascara and a groomed brow = done in 5 minutes.",
            "SPF every single day — even if it's cloudy.",
        ],
        "products": ["Tinted moisturiser SPF", "Tinted lip balm", "Brow gel", "Brown mascara"],
    },
    "🌙 Night Out": {
        "emoji": "🌙",
        "desc": "Club, cocktails or a late-night dinner — turn heads after dark.",
        "lip":  [50, 0, 80],
        "hair": [20, 0, 40],
        "tags": ["Dramatic", "Dark Lip", "Smoky"],
        "tips": [
            "Smoky eye + dark lip = maximum drama. Prime well.",
            "Use a lip liner slightly darker than your lip colour to define edges.",
            "Go full-coverage foundation — club lighting is unforgiving.",
            "Translucent powder in a compact for touch-ups.",
        ],
        "products": ["Full-coverage foundation", "Dark plum lipstick", "Smoky eyeshadow", "Black liquid liner", "Compact powder"],
    },
    "🎨 Festival / Outdoor": {
        "emoji": "🎨",
        "desc": "Creative, colourful and carefree. No rules here.",
        "lip":  [100, 180, 60],
        "hair": [180, 80, 200],
        "tags": ["Colourful", "Glitter", "Waterproof"],
        "tips": [
            "Use waterproof products — sweat and weather are not your friends.",
            "Face gems and glitter are having a major moment.",
            "Coloured eyeliner in teal, yellow or white makes a statement.",
            "Reapply SPF throughout the day — especially outdoors.",
        ],
        "products": ["Waterproof mascara", "Coloured eyeliner", "Face gems / glitter", "High SPF", "Setting spray"],
    },
    "🎓 Graduation / Formal": {
        "emoji": "🎓",
        "desc": "Celebratory and dignified — photos will be framed for decades.",
        "lip":  [100, 50, 120],
        "hair": [80, 50, 30],
        "tags": ["Classic", "Polished", "Long-Wear"],
        "tips": [
            "Classic red or rose lip is timeless in photographs.",
            "Winged eyeliner sharpens any look.",
            "Pin updos with bobby pins that match your hair colour.",
            "Bring blotting sheets for the ceremony.",
        ],
        "products": ["Classic red/rose lipstick", "Winged eyeliner", "Long-wear foundation", "Blotting sheets"],
    },
    "🏋️ Gym / Sport": {
        "emoji": "🏋️",
        "desc": "Workout without budging. Minimal but fresh.",
        "lip":  [200, 170, 160],
        "hair": [60, 40, 30],
        "tags": ["No-Makeup", "Sweat-Proof", "SPF"],
        "tips": [
            "Skip foundation — clogged pores during a workout can cause breakouts.",
            "Tinted sunscreen SPF 50+ is the only base you need.",
            "Waterproof mascara only if you must.",
            "Tie hair back with a soft scrunchie — no elastic bands that break hair.",
        ],
        "products": ["SPF 50 tinted sunscreen", "Waterproof mascara (optional)", "Lip balm SPF"],
    },
}

MEN_OCCASIONS = {
    "💼 Office / Work": {
        "emoji": "💼",
        "tips": [
            "A light tinted moisturiser or CC cream evens skin tone subtly.",
            "Concealer under the eyes for dark circles is invisible and effective.",
            "Keep brows groomed with a clear brow gel — messy brows age you.",
            "A tiny amount of lip balm prevents chapped lips in AC environments.",
        ],
        "grooming": ["Lightweight tinted moisturiser", "Under-eye concealer", "Clear brow gel", "Lip balm"],
        "skin_prep": "Cleanse + moisturise SPF in the AM. Eye cream + moisturiser at night.",
        "beard": "Keep beard trimmed and shaped. Beard oil daily for a polished appearance.",
    },
    "💍 Wedding": {
        "emoji": "💍",
        "tips": [
            "Even skin tone with a skin tint or BB cream — looks natural in photos.",
            "Matte powder eliminates shine under flash photography.",
            "Groom your beard the day before — not on the day itself.",
            "Get a fresh haircut 4–5 days before for the most natural shape.",
        ],
        "grooming": ["BB cream / skin tint", "Setting powder", "Beard trim kit"],
        "skin_prep": "Start a consistent routine 4+ weeks before. Vitamin C serum in the AM for glow.",
        "beard": "Shape beard 2 days before. Apply beard balm for a clean finish on the day.",
    },
    "🍸 Date Night": {
        "emoji": "🍸",
        "tips": [
            "Scent is your most powerful tool — wear a subtle, clean fragrance.",
            "Concealer on any blemishes and under eyes for a fresh look.",
            "A matte skin tint evens the complexion without looking made up.",
            "Check beard alignment — straggly edges are noticeable at close range.",
        ],
        "grooming": ["Light concealer", "Skin tint / BB cream", "Lip balm", "Fragrance"],
        "skin_prep": "Double cleanse, tone, serum, and a hydrating moisturiser on the evening.",
        "beard": "Trim and define clean edges with a razor or trimmer 1 day before.",
    },
    "🎉 Birthday / Party": {
        "emoji": "🎉",
        "tips": [
            "A light bronzer on the cheekbones gives a healthy, ready-to-party glow.",
            "Swipe on a hair product to tame flyaways for photos.",
            "A subtle highlighter on the brow bone can open up the eyes.",
        ],
        "grooming": ["Light bronzer", "Hair pomade or wax", "Skin tint"],
        "skin_prep": "Moisturise well before going out — skin holds a healthy glow under lighting.",
        "beard": "Condition the beard so it looks full and healthy in photos.",
    },
    "🌸 Casual Day Out": {
        "emoji": "🌸",
        "tips": [
            "SPF is the only non-negotiable. Skin tint with SPF does double duty.",
            "Lip balm prevents chapped lips in wind or cold.",
            "A tinted moisturiser is perfect for a relaxed day.",
        ],
        "grooming": ["SPF moisturiser or tinted SPF", "Lip balm"],
        "skin_prep": "Quick cleanse and SPF moisturiser. That's the entire routine.",
        "beard": "Apply a tiny drop of beard oil and brush through — takes 30 seconds.",
    },
    "🌙 Night Out": {
        "emoji": "🌙",
        "tips": [
            "Blot skin with a tissue before going out — shine looks worse under club lights.",
            "Concealer under eyes and on any blemishes.",
            "Hair product for hold and definition.",
            "Layer fragrance: body wash → deodorant → EDP or EDT.",
        ],
        "grooming": ["Blotting sheets", "Concealer", "Hair product", "Fragrance"],
        "skin_prep": "Cleanse and moisturise. Use a matte setting powder after moisturiser.",
        "beard": "Clean edges with a trimmer. Beard oil adds shine and scent.",
    },
    "🎨 Festival / Outdoor": {
        "emoji": "🎨",
        "tips": [
            "SPF 50 on all exposed skin — reapply every 2 hours.",
            "Waterproof everything — sweat and weather are real.",
            "A light BB cream provides coverage without looking done.",
        ],
        "grooming": ["High SPF 50 sunscreen", "Waterproof BB cream (optional)", "Lip balm SPF"],
        "skin_prep": "Heavy-duty SPF is the priority. Reapply religiously.",
        "beard": "Beard oil to protect facial hair from sun and wind.",
    },
    "🏋️ Gym / Sport": {
        "emoji": "🏋️",
        "tips": [
            "Cleanse before and after your workout.",
            "Skip all products at the gym — pores clog fast during exercise.",
            "SPF if you're training outdoors.",
        ],
        "grooming": ["Nothing except SPF if outdoors"],
        "skin_prep": "Clean face, no product during training. Cleanse + moisturise after.",
        "beard": "Rinse the beard after training. Reapply beard oil after the post-workout shower.",
    },
}

# ── Helper functions ───────────────────────────────────────────────────────────
def sharpen(img):
    gauss_out = gaussian(img * 1.0, sigma=5, channel_axis=-1)
    img_out = (img - gauss_out) * 1.5 + img
    return np.clip(img_out / 255.0, 0, 1) * 255 if img.max() > 1 else np.clip(img_out, 0, 1)

def apply_makeup(image, parsing, part, color):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b; tar_color[:, :, 1] = g; tar_color[:, :, 2] = r
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)
    image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    if part == 17:
        changed = np.array(sharpen(changed.astype(float)), dtype=np.uint8)
    changed[parsing != part] = image[parsing != part]
    return changed

# ── Page layout ────────────────────────────────────────────────────────────────
st.title("🎭 Makeup & Grooming for Every Occasion")
st.caption("AI-powered look recommendations tailored to you — select your gender and occasion to get started.")

with st.sidebar:
    st.markdown("### 🎭 Occasions Settings")
    gender = st.radio("I identify as", ["Woman", "Man", "Non-binary"], horizontal=True)
    if gender == "Non-binary":
        st.info("Showing all looks — mix and match what feels right for you.")

occasion_db = WOMEN_OCCASIONS if gender != "Man" else MEN_OCCASIONS

st.markdown("---")
selected_occasion = st.selectbox("🗓️ Choose your Occasion", list(occasion_db.keys()), index=0)
occ_data = occasion_db[selected_occasion]

c1, c2 = st.columns([1, 1])

with c1:
    st.markdown(f"### {selected_occasion}")
    if gender != "Man":
        st.markdown(f"*{occ_data.get('desc', '')}*")
        for t in occ_data.get("tags", []):
            st.markdown(f'<span class="tip-badge">{t}</span>', unsafe_allow_html=True)

    st.markdown("#### 💡 Tips & Techniques")
    for tip in occ_data["tips"]:
        st.markdown(f"- {tip}")

    if gender == "Man":
        st.markdown("#### 🧴 Recommended Grooming Products")
        for p in occ_data.get("grooming", []):
            st.markdown(f"- {p}")
        st.markdown(f"**Skin prep:** {occ_data.get('skin_prep', '')}")
        st.markdown(f"**Beard:** {occ_data.get('beard', '')}")
    else:
        st.markdown("#### 🛒 Key Products")
        for p in occ_data.get("products", []):
            st.markdown(f"- {p}")

with c2:
    if gender != "Man":
        st.markdown("#### 🎨 AI Virtual Try-On")
        img_file = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"], key="occ_upload")
        if st.button(f"✨ Try the {selected_occasion} Look"):
            src = img_file if img_file else DEFAULT_IMAGE_PATH
            try:
                orig = np.array(Image.open(src))
                parsing = evaluate(src, "cp/79999_iter.pth")
                parsing = cv2.resize(parsing, (512, 512), interpolation=cv2.INTER_NEAREST)
                img_r = cv2.resize(orig, (512, 512))
                lip_c = occ_data["lip"]
                hair_c = occ_data["hair"]
                for part, color in [(12, lip_c), (13, lip_c), (17, hair_c)]:
                    img_r = apply_makeup(img_r, parsing, part, color)
                final = cv2.resize(img_r, (orig.shape[1], orig.shape[0]))
                tab1, tab2 = st.tabs(["Before", "After"])
                with tab1:
                    st.image(orig, use_container_width=True)
                with tab2:
                    st.image(final, use_container_width=True)
                    buf = io.BytesIO()
                    Image.fromarray(final).save(buf, format="PNG")
                    st.download_button("⬇️ Download Look", buf.getvalue(), "occasion_look.png", "image/png")
            except Exception as e:
                st.warning(f"Couldn't process image: {e}. Showing tips only.")
        else:
            st.info("Upload a photo and click **Try the Look** to see the AI apply the colour palette.")
    else:
        st.markdown("#### 📸 Grooming Routine Checklist")
        st.markdown("""
        <div class="occ-card">
            <b>Before you go:</b><br>
            1. Cleanse your face<br>
            2. Apply your occasion-appropriate products<br>
            3. Style hair<br>
            4. Groom beard (if applicable)<br>
            5. Fragrance last
        </div>
        """, unsafe_allow_html=True)
        score = {"💼 Office / Work": 92, "💍 Wedding": 88, "🍸 Date Night": 85, "🎉 Birthday / Party": 78,
                 "🌸 Casual Day Out": 95, "🌙 Night Out": 80, "🎨 Festival / Outdoor": 75, "🏋️ Gym / Sport": 98}
        st.metric("Routine Simplicity Score", f"{score.get(selected_occasion, 85)}/100", delta="Easy to follow")

st.markdown("---")
st.markdown("### 📅 Occasion Quick Reference")
cols = st.columns(4)
for i, (occ_name, occ_info) in enumerate(occasion_db.items()):
    with cols[i % 4]:
        emoji = occ_info.get("emoji", "✨")
        short_name = occ_name.split(' ', 1)[1] if ' ' in occ_name else occ_name
        st.markdown(f"""
        <div class="occ-card" style="min-height:70px;">
            <b style="font-size:1.2rem;">{emoji}</b><br>
            <span style="font-size:0.82rem;color:#555;">{short_name}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("© 2025 BeautyBuzzi | Occasions powered by AI colour analysis")

