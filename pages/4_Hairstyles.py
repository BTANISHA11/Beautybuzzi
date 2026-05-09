import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.set_page_config(page_title="BeautyBuzzi – Hairstyles", page_icon="✂️", layout="wide")

st.markdown("""
<style>
h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #b76e79, #7c3c50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
h2, h3 { color: #7c3c50; }
.decorative-line {
    height: 3px;
    background: linear-gradient(90deg, transparent, #b76e79, transparent);
    margin: 18px 0; border-radius: 2px;
}
.style-card {
    background: #fff; border-radius: 14px; padding: 16px; margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(183,110,121,0.12); border-left: 5px solid #b76e79;
}
.tag {
    display: inline-block; background: #f8e1e5; color: #7c3c50;
    border-radius: 20px; padding: 2px 10px; font-size: 0.8rem;
    font-weight: 600; margin-right: 5px; margin-top: 4px;
}
.stButton > button {
    border-radius: 25px !important;
    background: linear-gradient(90deg, #b76e79, #7c3c50) !important;
    color: white !important; border: none !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hairstyle databases ────────────────────────────────────────────────────────
WOMEN_STYLES = {
    "Oval": {
        "Short": [
            {"name": "Pixie Cut", "desc": "Chic, close-cropped style that highlights bone structure. Very low maintenance.", "tags": ["Trendy", "Low Maintenance", "Bold"]},
            {"name": "Textured Crop", "desc": "Short layers with soft texture. Works beautifully with straight or wavy hair.", "tags": ["Casual", "Modern"]},
        ],
        "Medium": [
            {"name": "Layered Bob", "desc": "Versatile chin-to-collarbone length with layers for movement.", "tags": ["Classic", "Versatile"]},
            {"name": "Wolf Cut", "desc": "Shaggy layers with curtain bangs. Trending for 2025.", "tags": ["Trendy 2025", "Edgy"]},
            {"name": "Blunt Bob", "desc": "Sleek, one-length cut that looks polished and modern.", "tags": ["Polished", "Chic"]},
        ],
        "Long": [
            {"name": "Long Layers", "desc": "Classic long cut with face-framing layers for volume and movement.", "tags": ["Classic", "Feminine"]},
            {"name": "Butterfly Cut", "desc": "Shorter interior layers create a butterfly-wing silhouette when styled.", "tags": ["Trendy 2025", "Voluminous"]},
        ],
    },
    "Round": {
        "Short": [
            {"name": "Asymmetric Pixie", "desc": "One side longer — adds angles and elongates a round face.", "tags": ["Edgy", "Face-Slimming"]},
        ],
        "Medium": [
            {"name": "Long Bob with Side Part", "desc": "Collarbone-length with a deep side part to create an illusion of length.", "tags": ["Face-Slimming", "Elegant"]},
            {"name": "Shag with Curtain Bangs", "desc": "Curtain bangs draw the eye inward, making the face appear longer.", "tags": ["Boho", "Trendy 2025"]},
        ],
        "Long": [
            {"name": "Straight Long with Side-Swept Bangs", "desc": "Length and side-swept bangs both elongate a round face shape.", "tags": ["Elongating", "Classic"]},
            {"name": "Long Waves with Volume at Crown", "desc": "Crown volume adds height; waves break up roundness.", "tags": ["Romantic", "Voluminous"]},
        ],
    },
    "Square": {
        "Short": [
            {"name": "Soft Pixie with Wispy Layers", "desc": "Wispy layers soften a strong jawline.", "tags": ["Softening", "Low Maintenance"]},
        ],
        "Medium": [
            {"name": "Soft Waves Lob", "desc": "Waves at the ends of a mid-length cut soften angular features.", "tags": ["Romantic", "Softening"]},
            {"name": "Curly Bob", "desc": "Natural curls create softness around a square jawline.", "tags": ["Natural", "Softening"]},
        ],
        "Long": [
            {"name": "Loose Waves or Curls", "desc": "Softens the jawline. Avoid blunt, one-length cuts.", "tags": ["Softening", "Romantic"]},
            {"name": "Side-Parted Long Layers", "desc": "A side parting and long layers create asymmetry that balances square features.", "tags": ["Elegant", "Versatile"]},
        ],
    },
    "Heart": {
        "Short": [
            {"name": "Chin-Length Bob", "desc": "Adds width at the jawline to balance a wider forehead.", "tags": ["Balancing", "Classic"]},
        ],
        "Medium": [
            {"name": "Medium Waves with Side-Swept Bangs", "desc": "Bangs minimise a broad forehead; waves add lower-face volume.", "tags": ["Balancing", "Romantic"]},
            {"name": "Wavy Lob with Centre Part", "desc": "Centre part draws the eye down and balances a heart shape.", "tags": ["Boho", "Elegant"]},
        ],
        "Long": [
            {"name": "Long Waves", "desc": "Volume at the bottom balances a narrower chin.", "tags": ["Feminine", "Romantic"]},
        ],
    },
    "Oblong": {
        "Short": [
            {"name": "Blunt Bob with Bangs", "desc": "Bangs and a blunt cut create width and reduce apparent length.", "tags": ["Width-Adding", "Bold"]},
        ],
        "Medium": [
            {"name": "Wavy Bob with Full Bangs", "desc": "Full bangs shorten the face; waves add width.", "tags": ["Width-Adding", "Vintage"]},
        ],
        "Long": [
            {"name": "Layered Long with Waves", "desc": "Waves add width — avoid sleek straight styles.", "tags": ["Width-Adding", "Romantic"]},
        ],
    },
}

MEN_STYLES = {
    "Oval": {
        "Short": [
            {"name": "Crew Cut", "desc": "Timeless, neat and professional. Works for all settings.", "tags": ["Classic", "Professional"]},
            {"name": "Buzz Cut", "desc": "Ultra-low maintenance. Uniform short length all over.", "tags": ["Minimalist", "Bold"]},
            {"name": "Textured Quiff", "desc": "Short back and sides with length on top styled upward.", "tags": ["Trendy 2025", "Smart Casual"]},
        ],
        "Medium": [
            {"name": "Modern Pompadour", "desc": "Voluminous top swept back with tapered sides.", "tags": ["Classic", "Bold"]},
            {"name": "Curtains / Middle Part", "desc": "Popularised by 90s icons and back in full trend.", "tags": ["Trendy 2025", "Retro-Modern"]},
            {"name": "Slick Back", "desc": "Longer hair combed back for a polished, sharp look.", "tags": ["Sophisticated", "Professional"]},
        ],
        "Long": [
            {"name": "Man Bun", "desc": "Pulled back into a bun. Pairs well with undercut sides.", "tags": ["Casual", "Bohemian"]},
            {"name": "Surfer Waves", "desc": "Effortless tousled waves. Best with naturally wavy hair.", "tags": ["Casual", "Beach Vibes"]},
        ],
    },
    "Round": {
        "Short": [
            {"name": "High Fade with Textured Top", "desc": "High fade elongates the face; textured top adds height.", "tags": ["Face-Elongating", "Trendy"]},
            {"name": "Faux Hawk", "desc": "Strip of height down the centre adds perceived length.", "tags": ["Bold", "Edgy"]},
        ],
        "Medium": [
            {"name": "Quiff with High Fade", "desc": "Height at the top and tight sides elongates a round face.", "tags": ["Smart Casual", "Modern"]},
        ],
        "Long": [
            {"name": "Straight Long with Centre Part", "desc": "Length and a centre part elongate and narrow the face.", "tags": ["Bohemian", "Elongating"]},
        ],
    },
    "Square": {
        "Short": [
            {"name": "Soft Textured Crop", "desc": "Messy texture on top softens a square jawline.", "tags": ["Casual", "Softening"]},
            {"name": "Short Curls / Waves", "desc": "Natural texture breaks hard angles.", "tags": ["Natural", "Softening"]},
        ],
        "Medium": [
            {"name": "Side Part with Taper", "desc": "Layered sides with a clean side part. Balanced and polished.", "tags": ["Professional", "Classic"]},
        ],
        "Long": [
            {"name": "Wavy Long Hair", "desc": "Waves soften strong angles. Avoid very straight, one-length looks.", "tags": ["Bohemian", "Softening"]},
        ],
    },
    "Heart": {
        "Short": [
            {"name": "Short Back and Sides with Textured Top", "desc": "Minimises the forehead and adds width at the jawline.", "tags": ["Balanced", "Classic"]},
        ],
        "Medium": [
            {"name": "Side Swept Medium with Beard", "desc": "A beard adds visual weight at the jaw to balance a broader forehead.", "tags": ["Rugged", "Balanced"]},
        ],
        "Long": [
            {"name": "Long Layers with Beard", "desc": "Length adds jaw volume; layers reduce a wide-forehead appearance.", "tags": ["Bohemian", "Balanced"]},
        ],
    },
    "Oblong": {
        "Short": [
            {"name": "Flat Top", "desc": "Adds width. Classic barbershop look.", "tags": ["Width-Adding", "Bold"]},
        ],
        "Medium": [
            {"name": "Waves or Curls Mid-Length", "desc": "Adds horizontal volume to counteract the elongated shape.", "tags": ["Natural", "Width-Adding"]},
        ],
        "Long": [
            {"name": "Tousled Long with Layers", "desc": "Layers add width; tousling breaks up vertical lines.", "tags": ["Casual", "Width-Adding"]},
        ],
    },
}

HAIR_CARE_MEN = {
    "Straight": "Lightweight pomade or wax for definition. Shampoo 2–3× a week. Avoid heavy conditioners that flatten fine hair.",
    "Wavy": "Salt spray or curl-enhancing cream to define waves. Air-dry when possible. Shampoo 2× weekly, condition every wash.",
    "Curly": "Sulfate-free shampoo + curl-defining cream or gel. Deep condition weekly. Blot gently — don't rub with a towel.",
    "Coily / Afro": "Moisturise daily with a leave-in conditioner. Protective styles help retain length. Weekly moisturising shampoo.",
    "Fine / Thinning": "Volumising shampoo; avoid heavy products. Look into DHT-blocking shampoos (ketoconazole or saw palmetto). Minoxidil can help slow thinning.",
}

HAIR_CARE_WOMEN = {
    "Straight": "Smoothing serum before heat styling. Dry shampoo extends styles. Always use heat protectant spray.",
    "Wavy": "Scrunch in sea-salt spray or curl cream while damp. Diffuse or air-dry. Avoid touching hair while drying.",
    "Curly": "Use the LOC method (Liquid → Oil → Cream) for max moisture. Silk pillowcase overnight. Refresh next-day curls with water mist.",
    "Coily / Afro": "Deep condition weekly. Protective styles reduce breakage and retain length. Satin/silk pillowcase essential.",
    "Fine / Limp": "Avoid heavy masks or oils at the roots. Volumising mousse + upside-down blow-dry for lift.",
}

avoid_map = {
    "Round":   "Very round bobs with no layers, centre parts with no crown volume (emphasise width).",
    "Square":  "Blunt one-length cuts, straight-across fringes, and very short sides that expose jaw angles.",
    "Heart":   "Very voluminous styles at the forehead/crown without width at the jaw.",
    "Oblong":  "Sleek, one-length long styles or high pompadours that add further height.",
    "Oval":    "Oval faces suit almost everything — experiment freely!",
}

# ── Face-shape detection ───────────────────────────────────────────────────────
def detect_face_shape(image_array):
    try:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = detector.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))
        if len(faces) == 0:
            return None
        x, y, w, h = faces[0]
        ratio = w / h
        if ratio > 0.95:
            return "Round"
        elif ratio < 0.75:
            return "Oblong"
        elif 0.85 <= ratio <= 0.95:
            return "Square"
        elif 0.75 <= ratio < 0.85:
            return "Oval"
        else:
            return "Heart"
    except Exception:
        return None

# ── Page ───────────────────────────────────────────────────────────────────────
st.markdown('<h1>✂️ AI Hairstyle Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#7c3c50;font-size:1.1rem;">Smart hairstyle recommendations for every face shape, gender & preference 💇</p>', unsafe_allow_html=True)
st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    gender = st.selectbox("👤 Gender", ["Woman", "Man"])
with col_b:
    length_pref = st.selectbox("📏 Preferred Length", ["Short", "Medium", "Long"])
with col_c:
    hair_texture = st.selectbox("🌀 Hair Texture", ["Straight", "Wavy", "Curly", "Coily / Afro", "Fine / Thinning"])
with col_d:
    vibe = st.selectbox("✨ Style Vibe", ["All", "Classic", "Trendy", "Casual", "Professional", "Romantic", "Edgy", "Bohemian"])

st.markdown("---")
st.markdown("### 📸 Upload Photo for AI Face-Shape Detection (optional)")
uploaded = st.file_uploader("Upload a front-facing photo", type=["jpg", "jpeg", "png"])

auto_shape = None
if uploaded:
    img = np.array(Image.open(uploaded).convert("RGB"))
    st.image(img, caption="Uploaded photo", width=280)
    with st.spinner("Detecting face shape…"):
        auto_shape = detect_face_shape(img)
    if auto_shape:
        st.success(f"🧠 AI detected face shape: **{auto_shape}**")
    else:
        st.warning("Could not auto-detect — please select your face shape manually below.")

face_shapes = ["Oval", "Round", "Square", "Heart", "Oblong"]
default_idx = face_shapes.index(auto_shape) if auto_shape in face_shapes else 0
face_shape = st.selectbox("🔷 Face Shape", face_shapes, index=default_idx)

st.markdown("---")

# Recommendations
db = WOMEN_STYLES if gender == "Woman" else MEN_STYLES
shape_styles = db.get(face_shape, {})
length_styles = shape_styles.get(length_pref, [])
if vibe != "All":
    length_styles = [s for s in length_styles if any(vibe.lower() in t.lower() for t in s["tags"])]

st.markdown(f"### 💡 Top Picks — **{face_shape}** face · {gender} · {length_pref}")
if length_styles:
    for style in length_styles:
        tag_html = " ".join(f'<span class="tag">{t}</span>' for t in style["tags"])
        st.markdown(f"""
        <div class="style-card">
            <h3 style="margin:0 0 6px 0;">{style['name']}</h3>
            <p style="color:#555;margin:0 0 8px 0;">{style['desc']}</p>
            {tag_html}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No styles match your filters — try changing the length or vibe. Showing all styles for your face shape:")
    for l, styles in shape_styles.items():
        for style in styles:
            tag_html = " ".join(f'<span class="tag">{t}</span>' for t in style["tags"])
            st.markdown(f"""
            <div class="style-card">
                <strong>{style['name']}</strong> <small style="color:#aaa;">({l})</small><br>
                <span style="color:#555;font-size:0.9rem;">{style['desc']}</span><br>{tag_html}
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<div style="background:#fff8f0;border-radius:12px;padding:16px;border-left:5px solid #e67e22;">
    <strong>⚠️ Styles to avoid for {face_shape} face:</strong><br>
    <span style="color:#555;">{avoid_map.get(face_shape, "")}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🧴 Hair Care Guide for Your Texture")
care_db = HAIR_CARE_WOMEN if gender == "Woman" else HAIR_CARE_MEN
care_tip = care_db.get(hair_texture, "")
st.markdown(f"""
<div style="background:#f9f0f2;border-radius:12px;padding:18px;border-left:5px solid #b76e79;">
    <strong>💆 {hair_texture} Hair Tips:</strong><br>
    <span style="color:#555;">{care_tip}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🔥 Trending Styles in 2025")
if gender == "Woman":
    trends = [
        ("🦋 Butterfly Cut", "Interior short layers fan out like butterfly wings."),
        ("🐺 Wolf Cut", "Shaggy 70s-inspired layers for all hair types."),
        ("💫 Bixie", "Between a bob and pixie — collarbone-skimming with short layers."),
        ("🌿 Bubble Braid", "Sectioned ponytail with rubber bands creating a bubble effect."),
        ("🎀 Bow Updo", "Sculptural updo styled to resemble a bow. Fun and maximalist."),
    ]
else:
    trends = [
        ("🪞 Curtains / Middle Part", "Centre-parted, collar-skimming length. Clean and effortlessly cool."),
        ("🔪 Edgar Cut", "Blunt fringe with high fade sides."),
        ("🌊 Textured Quiff", "Voluminous, naturally textured top vs the slick 2010s version."),
        ("🐺 Modern Shag", "Layered tousled look. Low effort, high style."),
        ("🪭 Undercut Long Top", "Buzzed sides + long top — high contrast, maximum versatility."),
    ]

tc = st.columns(len(trends))
for i, (name, desc) in enumerate(trends):
    with tc[i]:
        st.markdown(f"""
        <div class="style-card" style="border-left-color:#a86090;padding:12px;">
            <strong style="font-size:0.95rem;">{name}</strong><br>
            <span style="font-size:0.82rem;color:#555;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
with st.expander("💈 Pro Salon Tips"):
    if gender == "Man":
        st.markdown("""
- **Book every 3–6 weeks** for short cuts; 8–12 weeks for longer styles.
- **Show a reference photo** — barbers work visually.
- **Invest in good product:** Pomade (shine + hold), clay (matte + texture), wax (flexible hold).
- **Scalp health:** Anti-dandruff shampoo 1–2×/week if needed.
- **Beard:** Oil daily and trim every 1–2 weeks for a clean look.
        """)
    else:
        st.markdown("""
- **Trim every 6–8 weeks** to prevent split ends, even while growing it out.
- **Bring 2–3 reference photos** — one cut, one colour, one styling.
- **Silk pillowcase** dramatically reduces breakage and frizz overnight.
- **Heat protectant** before any heat styling above 150°C / 300°F.
- **Protein vs moisture:** Too much protein = brittle; rotate between protein and deep conditioning masks.
        """)


