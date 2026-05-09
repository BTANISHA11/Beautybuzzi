import streamlit as st
from PIL import Image


st.set_page_config(page_title="BeautyBuzzi - Features", page_icon="✨", layout="wide")


st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1180px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero-shell {
        background:
            radial-gradient(circle at top left, rgba(255,255,255,0.9), rgba(255,255,255,0.72) 40%, rgba(255,244,246,0.78) 100%),
            linear-gradient(135deg, #f8d9de 0%, #f7f0e8 100%);
        border-radius: 28px;
        padding: 34px;
        box-shadow: 0 22px 55px rgba(124, 60, 80, 0.12);
        margin-bottom: 24px;
        border: 1px solid rgba(124, 60, 80, 0.08);
    }

    .eyebrow {
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #8a5566;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.02;
        color: #432631;
        margin: 0 0 12px 0;
        font-weight: 800;
    }

    .hero-copy {
        color: #63434f;
        font-size: 1.05rem;
        line-height: 1.8;
        max-width: 760px;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 20px;
    }

    .pill {
        background: rgba(124, 60, 80, 0.08);
        color: #7c3c50;
        border-radius: 999px;
        padding: 9px 14px;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .section-title {
        color: #4e2d39;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 10px 0 14px 0;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 18px;
        margin-top: 8px;
    }

    .feature-card {
        background: linear-gradient(180deg, #ffffff 0%, #fff6f7 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 14px 28px rgba(124, 60, 80, 0.08);
        border: 1px solid rgba(124, 60, 80, 0.08);
        min-height: 220px;
    }

    .feature-icon {
        font-size: 1.9rem;
        margin-bottom: 10px;
    }

    .feature-title {
        color: #522f3b;
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .feature-copy {
        color: #6a4a56;
        line-height: 1.7;
        font-size: 0.94rem;
    }

    .ops-panel {
        background: #fff;
        border-radius: 24px;
        padding: 24px;
        border: 1px solid rgba(124, 60, 80, 0.08);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.05);
        margin-top: 24px;
    }

    .ops-item {
        padding: 12px 0;
        border-bottom: 1px solid rgba(124, 60, 80, 0.08);
        color: #5d404c;
        line-height: 1.7;
    }

    .ops-item:last-child {
        border-bottom: none;
    }

    @media (max-width: 768px) {
        .hero-shell {
            padding: 24px;
        }

        .hero-title {
            font-size: 2.3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


hero_image = Image.open("./pages/images/featureHome.png")
detail_image = Image.open("./pages/images/image1.png")

st.markdown(
    """
    <div class="hero-shell">
        <div class="eyebrow">Beauty Intelligence Platform</div>
        <div class="hero-title">BeautyBuzzi brings virtual try-on, skin intelligence, grooming guidance, and expert care into one workflow.</div>
        <div class="hero-copy">
            The current app combines Streamlit, PyTorch face parsing, MediaPipe face landmarks, image heuristics, and guided recommendation flows to support both women and men across makeup, skincare, hairstyles, products, occasions, and consultations.
        </div>
        <div class="pill-row">
            <div class="pill">MediaPipe Face Mesh</div>
            <div class="pill">BiSeNet Hair Segmentation</div>
            <div class="pill">Skin Tone Matching</div>
            <div class="pill">Men's Grooming Flows</div>
            <div class="pill">Webcam Snapshot Input</div>
            <div class="pill">Downloadable Results</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.image(hero_image, caption="Virtual try-on and beauty guidance across the app", width="stretch")

st.markdown('<div class="section-title">Core Product Capabilities</div>', unsafe_allow_html=True)

cards = [
    (
        "💄",
        "Precision Makeup Rendering",
        "Lipstick, eyeshadow, blush, eyeliner, brow tint, beard tint, and hair color can now use landmark-aware placement with soft LAB-space blending instead of flat overlays.",
    ),
    (
        "📸",
        "Upload or Webcam Snapshot",
        "Users can test looks from an uploaded image or capture a fresh webcam photo directly inside Streamlit, which makes the try-on loop much faster.",
    ),
    (
        "🎨",
        "Foundation Shade Matching",
        "Cheek-region tone sampling plus a curated shade set provides top-match suggestions with visual swatches for a more realistic complexion workflow.",
    ),
    (
        "🧴",
        "Personalised Skin Analysis",
        "The skin page generates a health score, condition heuristics, product suggestions, routines, tone matching, and a short in-session history of recent analyses.",
    ),
    (
        "💈",
        "Men's Grooming Support",
        "Beard tint, brow tint, post-shave guidance, hairstyle recommendations, and male-focused occasion suggestions make the experience useful beyond beauty-only flows.",
    ),
    (
        "🗓️",
        "Occasion and Routine Guidance",
        "Users get occasion-based looks, routine steps, lifestyle advice, consultation booking, and product suggestions organized into focused multi-page flows.",
    ),
]

st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
for icon, title, copy in cards:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('</div>', unsafe_allow_html=True)

st.image(detail_image, caption="BeautyBuzzi supports analysis, recommendations, and guided beauty journeys", width="stretch")

st.markdown('<div class="ops-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">What Makes This More Production-Ready</div>', unsafe_allow_html=True)
ops_items = [
    "Graceful fallback logic keeps the app usable when MediaPipe landmarks are unavailable by switching back to segmentation-based rendering.",
    "Gender-aware content paths are now present across analysis, products, occasions, and consultations instead of forcing a single beauty profile.",
    "Downloadable outputs and structured JSON skin reports make the app more usable beyond a one-time visual demo.",
    "The feature set stays inside Streamlit where it is reliable today, instead of claiming unsupported real-time browser streaming that the current stack does not provide.",
]
for item in ops_items:
    st.markdown(f'<div class="ops-item">{item}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

cta1, cta2, cta3 = st.columns(3)
with cta1:
    if st.button("Open Virtual Try-On"):
        st.switch_page("app.py")
with cta2:
    if st.button("Open Skin Analysis"):
        st.switch_page("pages/2_Skin_analysis.py")
with cta3:
    if st.button("Book Consultation"):
        st.switch_page("pages/6_Consultations.py")