import streamlit as st
from PIL import Image
import numpy as np
import time
import io
import json
from datetime import datetime

from mediapipe_makeup import MEDIAPIPE_OK, detect_skin_tone, get_landmarks, match_foundation

def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 850px;
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
    
    h2 {
        font-size: 2rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        color: #7c3c50;
    }
    
    h3 {
        font-size: 1.5rem !important;
        margin-top: 1.5rem !important;
        color: #b76e79;
    }
    
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #b76e79, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    /* Card styling */
    .css-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 4px 12px rgba(183, 110, 121, 0.15);
        margin-bottom: 20px;
        border-left: 4px solid #b76e79;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #b76e79;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #7c3c50;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* File uploader */
    .uploadedFileData {
        padding: 15px;
        border-radius: 8px;
        border: 2px dashed #b76e79;
        background-color: rgba(183, 110, 121, 0.05);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #b76e79;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: #fff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    
    .metric-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
        color: #7c3c50;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #b76e79;
    }
    
    /* Recommendations styling */
    .recommendation-item {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: rgba(183, 110, 121, 0.05);
        border-left: 3px solid #b76e79;
    }
    
    /* Image styling */
    img {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f9f0f2;
        border-radius: 10px 10px 0px 0px;
        color: #7c3c50;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #b76e79 !important;
        color: white !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

def analyze_skin(image):
    """Light-weight deterministic skin analysis.

    Uses simple image statistics and high-frequency energy to estimate
    acne (blemish density), dryness, oiliness (specular highlights),
    and sensitivity (redness). This is a heuristic fallback until
    a trained model is integrated.
    """
    # Ensure NumPy array (RGB)
    img = np.array(image.convert("RGB")) if hasattr(image, 'convert') else np.array(image)

    # Resize for faster processing
    try:
        import cv2 as _cv
        img_small = _cv.resize(img, (512, 512), interpolation=_cv.INTER_AREA)
    except Exception:
        img_small = img if img.shape[0] <= 512 else img[:512, :512]

    # Convert to float for computations
    arr = img_small.astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Brightness and contrast
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mean_lum = np.mean(lum)
    std_lum = np.std(lum)

    # Redness (sensitivity proxy)
    redness_map = np.clip(r - (g + b) / 2.0, 0, 255)
    redness_score = float(np.mean(redness_map) / 255.0) * 100.0

    # High-frequency energy as acne/blemish proxy (edges / texture)
    try:
        import cv2 as _cv
        gray = _cv.cvtColor(img_small.astype(np.uint8), _cv.COLOR_RGB2GRAY)
        dtype_const = _cv.CV_32F if hasattr(_cv, 'CV_32F') else (_cv.CV_64F if hasattr(_cv, 'CV_64F') else _cv.CV_8U)
        lap = np.abs(_cv.Laplacian(gray, dtype_const))
        hf_energy = float(np.mean(lap))
    except Exception:
        # fallback: use local std deviation
        hf_energy = float(std_lum)

    # Normalize heuristics to 0-100
    acne = min(max(int((hf_energy / (hf_energy + 10)) * 100), 0), 100)
    sensitivity = min(max(int(redness_score), 0), 100)

    # Oiliness: detect specular highlights (high luminance, low saturation)
    sat = 1.0 - (np.min(arr, axis=2) / (np.max(arr, axis=2) + 1e-6))
    spec_mask = (lum > (mean_lum + std_lum)) & (sat < 0.35)
    oiliness = int(np.clip(100.0 * (np.sum(spec_mask) / spec_mask.size), 0, 100))

    # Dryness: inverse of oiliness, adjusted by low brightness
    dryness = int(np.clip(100.0 * (1.0 - (np.sum(spec_mask) / spec_mask.size)) * (1.0 - mean_lum / 255.0), 0, 100))

    # Derive skin type heuristic
    if oiliness > 60 and acne > 40:
        skin_type = "Oily"
    elif dryness > 60:
        skin_type = "Dry"
    elif sensitivity > 50:
        skin_type = "Sensitive"
    elif 40 < oiliness <= 60:
        skin_type = "Combination"
    else:
        skin_type = "Normal"

    results = {
        "acne": acne,
        "dryness": dryness,
        "oiliness": oiliness,
        "sensitivity": sensitivity,
        "skin_type": skin_type,
    }
    return results

def get_product_recommendations(results):
    recommendations = {
        "cleanser": "",
        "treatment": "",
        "moisturizer": ""
    }
    
    # Cleansers
    if results['oiliness'] > 60:
        recommendations["cleanser"] = "Foaming Gel Cleanser with Salicylic Acid"
    elif results['dryness'] > 60:
        recommendations["cleanser"] = "Hydrating Cream Cleanser with Ceramides"
    elif results['sensitivity'] > 60:
        recommendations["cleanser"] = "Gentle Fragrance-Free Cleanser with Oat Extract"
    else:
        recommendations["cleanser"] = "Balanced pH Cleanser with Amino Acids"
    
    # Treatments
    if results['acne'] > 60:
        recommendations["treatment"] = "2% BHA Liquid Exfoliant or Benzoyl Peroxide Spot Treatment"
    elif results['dryness'] > 60:
        recommendations["treatment"] = "Hyaluronic Acid Serum with B5"
    elif results['sensitivity'] > 60:
        recommendations["treatment"] = "Centella Asiatica Serum with Green Tea Extract"
    else:
        recommendations["treatment"] = "Niacinamide 10% + Zinc 1% Serum"
    
    # Moisturizers
    if results['oiliness'] > 60:
        recommendations["moisturizer"] = "Oil-Free Gel Moisturizer with Hyaluronic Acid"
    elif results['dryness'] > 60:
        recommendations["moisturizer"] = "Rich Cream Moisturizer with Shea Butter and Ceramides"
    elif results['sensitivity'] > 60:
        recommendations["moisturizer"] = "Fragrance-Free Soothing Moisturizer with Colloidal Oatmeal"
    else:
        recommendations["moisturizer"] = "Lightweight Lotion with Peptides and Antioxidants"
    
    return recommendations

def render_ai_skin_analysis_page():
    local_css()

    if "skin_analysis_history" not in st.session_state:
        st.session_state.skin_analysis_history = []

    st.markdown('<h1>🔬 AI Skin Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        """
            <div style="text-align: left; margin-bottom: 15px; font-family: 'Poppins', sans-serif;">
                <p style="font-size: 1.1rem; color: #7c3c50; font-weight: 300;">
                    Upload a selfie and get a personalised skincare report with routines for your gender, age & lifestyle ✨
                </p>
            </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

    # ── Profile inputs ───────────────────────────────────────────────────────
    st.markdown("### 👤 Your Profile")
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        gender = st.selectbox("Gender", ["Woman", "Man", "Non-binary / Prefer not to say"])
    with pc2:
        age_group = st.selectbox("Age Group", ["Under 18", "18–25", "26–35", "36–45", "46–55", "55+"])
    with pc3:
        lifestyle = st.selectbox("Lifestyle / Climate", ["Urban / Polluted", "Suburban", "Outdoor / Active", "Dry Climate", "Humid Climate"])

    st.markdown("---")

    st.markdown("""
    <div class="css-card">
        <h3 style="margin-top: 0;">📸 How to get the best results</h3>
        <p>Upload a clear, well-lit selfie <strong>without makeup</strong>. Face the camera directly and avoid filters. Natural light gives the most accurate analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    input_mode = st.radio("Input Mode", ["Upload Photo", "Webcam Snapshot"], horizontal=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        if input_mode == "Upload Photo":
            uploaded_file = st.file_uploader(
                "Upload a clear selfie",
                type=["jpg", "jpeg", "png"],
                key="skin_analysis_upload",
            )
            camera_file = None
        else:
            camera_file = st.camera_input("Take a snapshot", key="skin_analysis_camera")
            uploaded_file = None
    with col2:
        st.markdown("""
        <div style="background-color: #f9f0f2; padding: 15px; border-radius: 10px; height: 90%; display: flex; align-items: center; justify-content: center; text-align: center;">
            <div><span style="font-size: 3rem;">📸</span><p style="margin-top: 10px;">Your photo appears here</p></div>
        </div>
        """, unsafe_allow_html=True)

    input_file = uploaded_file or camera_file

    if input_file is not None:
        image = Image.open(input_file).convert("RGB")
        st.image(image, caption='Your photo', width="stretch")

        if st.button("🔬 Analyse My Skin", key="skin_analysis_run"):
            progress_bar = st.progress(0)
            status_text  = st.empty()
            for i in range(101):
                status_text.text(f"Analysing… {i}%")
                progress_bar.progress(i)
                time.sleep(0.01)
            status_text.text("Analysis complete!")
            st.success("✅ Your skin has been successfully analysed!")

            results  = analyze_skin(image)
            products = get_product_recommendations(results)
            image_rgb = np.array(image)
            landmarks = get_landmarks(image_rgb)
            skin_lab, skin_rgb = detect_skin_tone(image_rgb, landmarks) if landmarks is not None else (None, None)
            foundation_matches = match_foundation(skin_lab) if skin_lab is not None else []

            # Overall skin score (0–100, higher = healthier)
            skin_score = max(0, 100 - int(
                results['acne'] * 0.35 +
                results['dryness'] * 0.25 +
                results['oiliness'] * 0.20 +
                results['sensitivity'] * 0.20
            ))
            score_color = "#2ecc71" if skin_score >= 70 else "#f39c12" if skin_score >= 40 else "#e74c3c"

            # Score card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg,#f9f0f2,#fff); border-radius:15px; padding:20px; text-align:center; margin-bottom:20px; box-shadow:0 4px 12px rgba(183,110,121,0.1);">
                <h2 style="margin:0; color:#7c3c50;">Your Skin Health Score</h2>
                <div style="font-size:4rem; font-weight:900; color:{score_color}; line-height:1.1;">{skin_score}</div>
                <div style="color:#999; font-size:0.9rem;">out of 100</div>
                <div style="margin-top:8px; font-size:1rem; color:#7c3c50; font-weight:600;">Detected Type: <strong>{results['skin_type']}</strong></div>
            </div>
            """, unsafe_allow_html=True)

            report_payload = {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "gender": gender,
                "age_group": age_group,
                "lifestyle": lifestyle,
                "skin_score": skin_score,
                "results": results,
                "products": products,
                "foundation_matches": [
                    {"distance": round(dist, 2), "name": name, "hex": hex_col}
                    for dist, name, hex_col in foundation_matches
                ],
            }

            st.session_state.skin_analysis_history.insert(
                0,
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "skin_score": skin_score,
                    "skin_type": results["skin_type"],
                    "oiliness": results["oiliness"],
                    "dryness": results["dryness"],
                    "acne": results["acne"],
                    "sensitivity": results["sensitivity"],
                },
            )
            st.session_state.skin_analysis_history = st.session_state.skin_analysis_history[:5]

            report_cols = st.columns([1.2, 1, 1])
            with report_cols[0]:
                st.download_button(
                    "⬇️ Download Skin Report",
                    data=json.dumps(report_payload, indent=2),
                    file_name="beautybuzzi_skin_report.json",
                    mime="application/json",
                )
            with report_cols[1]:
                if foundation_matches:
                    st.metric("Best Shade", foundation_matches[0][1])
            with report_cols[2]:
                st.metric("Face Mesh", "Active" if landmarks is not None else "Unavailable")

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Analysis", "💧 Products", "🗓️ Routine", "🎨 Tone Match", "📈 History"])

            with tab1:
                st.subheader("Your Skin Profile")
                col1, col2 = st.columns(2)
                metrics = [
                    ("Acne / Blemishes", results['acne'], "🔴"),
                    ("Dryness", results['dryness'], "🏜️"),
                    ("Oiliness", results['oiliness'], "💧"),
                    ("Sensitivity / Redness", results['sensitivity'], "🌸"),
                ]
                for i, (label, val, icon) in enumerate(metrics):
                    col = col1 if i % 2 == 0 else col2
                    bar_color = "#e74c3c" if val > 70 else "#f39c12" if val > 40 else "#2ecc71"
                    with col:
                        st.markdown(f"""
                        <div class="metric-container" style="margin-bottom:16px;">
                            <div class="metric-title">{icon} {label}</div>
                            <div class="metric-value" style="color:{bar_color};">{val}%</div>
                            <div style="background:#f0f0f0;border-radius:8px;height:8px;margin:8px 0;">
                                <div style="background:{bar_color};width:{val}%;height:8px;border-radius:8px;"></div>
                            </div>
                            <div style="color:#888;font-size:0.85rem;">{get_level_description(val)}</div>
                        </div>
                        """, unsafe_allow_html=True)

                # Gender-specific insights
                st.markdown("---")
                st.subheader("💡 Key Insights for You")
                if gender == "Man":
                    insights = [
                        "Men's skin is ~25% thicker and produces more sebum — daily SPF is still essential.",
                        "Shaving causes micro-abrasions; use an alcohol-free balm or serum post-shave.",
                        "Niacinamide is a great all-rounder for men: reduces pores, controls oil, and evens tone.",
                    ]
                elif gender == "Woman":
                    insights = [
                        "Hormonal fluctuations throughout the month can cause breakouts — track your cycle.",
                        "Estrogen supports collagen production; prioritise antioxidants as levels drop with age.",
                        "SPF every morning is the single most effective anti-ageing step.",
                    ]
                else:
                    insights = [
                        "Everyone benefits from SPF, hydration, and a gentle cleanser — start there.",
                        "Track your skin's response to products over 4–6 weeks before switching.",
                        "Patch-test new actives on your jaw before applying to your full face.",
                    ]
                if age_group in ["36–45", "46–55", "55+"]:
                    insights.append("Consider adding a retinol or peptide serum to support cell turnover and firmness.")
                if lifestyle == "Urban / Polluted":
                    insights.append("Use an antioxidant serum (Vitamin C) in the morning to neutralise pollution damage.")
                if lifestyle in ["Outdoor / Active", "Humid Climate"]:
                    insights.append("Reapply SPF every 90–120 minutes when outdoors, even on overcast days.")
                for tip in insights:
                    st.markdown(f"- {tip}")

                st.markdown("---")
                if landmarks is not None:
                    st.success("Face landmarks detected. Tone analysis and foundation matching are available for this image.")
                elif MEDIAPIPE_OK:
                    st.warning("No face landmarks detected in this image. Skin heuristics still ran, but tone matching is unavailable.")
                else:
                    st.info("MediaPipe is not available, so foundation matching is disabled on this machine.")

            with tab2:
                st.subheader("Personalised Product Recommendations")
                prod_cols = st.columns(3)
                prod_map = [("🧼 Cleanser", products["cleanser"]), ("💧 Treatment", products["treatment"]), ("🧴 Moisturiser", products["moisturizer"])]
                # Add gender-specific products
                if gender == "Man":
                    prod_map.append(("🪒 Post-Shave", "Alcohol-free soothing balm with allantoin and panthenol"))
                    prod_map.append(("☀️ SPF", "Invisible matte broad-spectrum SPF 50"))
                else:
                    prod_map.append(("☀️ SPF", "Lightweight SPF 50+ with antioxidants"))
                    prod_map.append(("🌙 Night Treatment", "Retinol 0.2–0.5% or peptide serum (PM use only)"))

                for idx, (label, text) in enumerate(prod_map):
                    with prod_cols[idx % 3]:
                        st.markdown(f"""
                        <div style="background:#fff;border-radius:12px;padding:15px;box-shadow:0 4px 12px rgba(0,0,0,0.05);margin-bottom:12px;text-align:center;border-top:4px solid #b76e79;">
                            <div style="font-size:1.5rem;">{label.split()[0]}</div>
                            <h4 style="color:#7c3c50;margin:8px 0 6px;">{' '.join(label.split()[1:])}</h4>
                            <p style="font-size:0.88rem;color:#555;">{text}</p>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("#### 🧪 Key Ingredients to Look For")
                ingredients = []
                if results['acne'] > 40:
                    ingredients += [("Salicylic Acid (BHA)", "Clears pores and reduces inflammation"), ("Benzoyl Peroxide", "Fights acne bacteria")]
                if results['dryness'] > 40:
                    ingredients += [("Hyaluronic Acid", "Attracts and retains moisture"), ("Ceramides", "Rebuilds the skin barrier")]
                if results['oiliness'] > 40:
                    ingredients += [("Niacinamide", "Regulates sebum production and minimises pores"), ("Zinc PCA", "Controls oil and has mild antibacterial action")]
                if results['sensitivity'] > 40:
                    ingredients += [("Centella Asiatica", "Calms redness and speeds repair"), ("Allantoin", "Soothes irritated skin")]
                if age_group in ["36–45", "46–55", "55+"]:
                    ingredients += [("Retinol / Retinal", "Boosts cell turnover and collagen"), ("Peptides", "Signal skin to produce more collagen")]
                if not ingredients:
                    ingredients = [("Niacinamide", "Great all-rounder for balanced skin"), ("Antioxidants (Vit C/E)", "Protects against environmental damage")]
                for name, desc in ingredients:
                    st.markdown(f"- **{name}:** {desc}")

            with tab3:
                st.subheader("Your Personalised Skincare Routine")
                am_steps = ["Gentle cleanser", f"Treatment serum: {products['treatment']}", f"Moisturiser: {products['moisturizer']}", "SPF 50+ (non-negotiable!)"]
                pm_steps = ["Cleanser (double-cleanse if you wore sunscreen/makeup)", f"Active treatment: {products['treatment']}", f"Moisturiser: {products['moisturizer']}"]
                if gender == "Man":
                    am_steps.insert(1, "Post-shave balm (on shaved areas)")
                if results['dryness'] > 60:
                    pm_steps.insert(2, "Hydrating toner or essence (layer for extra moisture)")
                if results['dryness'] > 70:
                    pm_steps.append("Occlusive balm on very dry patches to seal in moisture")
                if age_group in ["36–45", "46–55", "55+"]:
                    pm_steps.insert(2, "Retinol or peptide serum (2–3 nights per week, build up slowly)")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="css-card"><h3 style="margin-top:0;">☀️ Morning Routine</h3><ol>', unsafe_allow_html=True)
                    for s in am_steps:
                        st.markdown(f"<li>{s}</li>", unsafe_allow_html=True)
                    st.markdown("</ol></div>", unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="css-card"><h3 style="margin-top:0;">🌙 Evening Routine</h3><ol>', unsafe_allow_html=True)
                    for s in pm_steps:
                        st.markdown(f"<li>{s}</li>", unsafe_allow_html=True)
                    st.markdown("</ol></div>", unsafe_allow_html=True)

                st.markdown('<div class="css-card"><h3 style="margin-top:0;">📅 Weekly Boosters</h3><ul>', unsafe_allow_html=True)
                weekly = []
                if results['acne'] > 40:
                    weekly.append("1–2× weekly: Clay or charcoal mask to deep-clean pores")
                if results['oiliness'] > 40:
                    weekly.append("1× weekly: BHA chemical exfoliant (e.g. Paula's Choice 2% BHA Liquid)")
                if results['dryness'] > 40:
                    weekly.append("2–3× weekly: Hydrating sheet mask")
                if results['sensitivity'] > 40:
                    weekly.append("2× weekly: Soothing oat or aloe vera mask")
                if not weekly:
                    weekly.append("1× weekly: Gentle AHA exfoliant to maintain glow")
                for w in weekly:
                    st.markdown(f"<li>{w}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

            with tab4:
                st.subheader("🎨 Skin Tone & Foundation Match")
                if foundation_matches and skin_rgb is not None:
                    skin_hex = "#{:02x}{:02x}{:02x}".format(int(skin_rgb[0]), int(skin_rgb[1]), int(skin_rgb[2]))
                    st.markdown(f"""
                    <div style="background:#fff;border-radius:14px;padding:18px;box-shadow:0 4px 12px rgba(0,0,0,0.05);margin-bottom:16px;">
                        <strong>Detected Cheek Tone</strong><br>
                        <span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:{skin_hex};border:2px solid #ddd;margin:10px 8px 0 0;vertical-align:middle;"></span>
                        <span style="font-family:monospace;">{skin_hex.upper()}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    shade_cols = st.columns(3)
                    badges = ["Best Match", "Close Match", "Alternative"]
                    for idx, (dist, name, hex_col) in enumerate(foundation_matches):
                        with shade_cols[idx]:
                            match_score = max(0, 100 - int(dist))
                            st.markdown(f"""
                            <div style="background:#fff;border-radius:12px;padding:16px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.05);">
                                <div style="font-size:0.8rem;color:#7c3c50;font-weight:700;">{badges[idx]}</div>
                                <div style="font-size:1rem;font-weight:700;margin-top:6px;">{name}</div>
                                <div style="width:56px;height:56px;border-radius:50%;background:{hex_col};margin:12px auto;border:3px solid #eee;"></div>
                                <div style="font-family:monospace;font-size:0.82rem;">{hex_col.upper()}</div>
                                <div style="font-size:0.82rem;color:#666;margin-top:8px;">Match score: {match_score}%</div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("#### Shade Notes")
                    st.markdown("- Test your closest shade on the jawline, not the wrist.")
                    st.markdown("- If your neck is lighter than your face, match the neck for a more even result.")
                    st.markdown("- Choose a more neutral undertone if your skin looks different indoors vs daylight.")
                else:
                    st.info("Upload or capture a clear front-facing selfie in even lighting to enable shade matching.")

                st.markdown("---")
                st.subheader("🌿 Lifestyle Tips for Better Skin")
                life_tips = {
                    "💧 Hydration": "Drink 2–3 litres of water daily. Skin hydration starts from within.",
                    "😴 Sleep": "Aim for 7–9 hours. Skin repairs itself during deep sleep — this is when your PM products work hardest.",
                    "🥗 Diet": "Prioritise omega-3 fatty acids (salmon, walnuts), antioxidant-rich berries, and leafy greens.",
                    "🧘 Stress": "Chronic stress raises cortisol, triggering breakouts. Even 10 min of mindfulness helps.",
                    "🚭 Avoid": "Smoking accelerates skin ageing by breaking down collagen. Limit alcohol — it dehydrates the skin.",
                    "🏃 Exercise": "Cardio improves blood flow and skin cell renewal. Rinse your face post-workout to clear sweat.",
                }
                if lifestyle == "Urban / Polluted":
                    life_tips["🏙️ Pollution Shield"] = "Double cleanse every evening to remove PM2.5 particles. Vitamin C in the morning acts as an antioxidant shield."
                if lifestyle == "Outdoor / Active":
                    life_tips["☀️ Sun Protection"] = "Reapply SPF every 90 min outdoors. Wear a wide-brimmed hat for additional coverage."
                if lifestyle == "Dry Climate":
                    life_tips["🌵 Dry Climate"] = "Use a humidifier indoors. Layer hydration: toner → serum → moisturiser → occlusive."
                if lifestyle == "Humid Climate":
                    life_tips["🌴 Humid Climate"] = "Lightweight gel moisturisers and water-based products will feel more comfortable. Don't skip SPF — clouds don't block UV."

                for title, tip in life_tips.items():
                    st.markdown(f"""
                    <div style="background:#f9f0f2;border-radius:10px;padding:14px;margin-bottom:10px;border-left:4px solid #b76e79;">
                        <strong>{title}</strong><br><span style="color:#555;font-size:0.93rem;">{tip}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.info("📅 **Want a professional opinion?** Book a virtual consultation with one of our skin experts on the **Consultations** page.")
                if st.button("📅 Book a Consultation →", key="skin_analysis_book_consultation"):
                    st.switch_page("pages/6_Consultations.py")

            with tab5:
                st.subheader("📈 Recent Analysis History")
                history = st.session_state.skin_analysis_history
                if history:
                    latest = history[0]
                    metric_cols = st.columns(4)
                    metric_cols[0].metric("Latest Score", latest["skin_score"])
                    metric_cols[1].metric("Skin Type", latest["skin_type"])
                    metric_cols[2].metric("Oiliness", f"{latest['oiliness']}%")
                    metric_cols[3].metric("Dryness", f"{latest['dryness']}%")

                    if len(history) > 1:
                        trend_history = list(reversed(history))
                        st.line_chart({
                            "Skin Score": [item["skin_score"] for item in trend_history],
                            "Acne": [item["acne"] for item in trend_history],
                            "Oiliness": [item["oiliness"] for item in trend_history],
                            "Dryness": [item["dryness"] for item in trend_history],
                        })
                        score_delta = latest["skin_score"] - trend_history[0]["skin_score"]
                        if score_delta > 0:
                            st.success(f"Skin score trend is improving by {score_delta} points across this session.")
                        elif score_delta < 0:
                            st.warning(f"Skin score is down by {abs(score_delta)} points across this session. Review lifestyle and routine changes.")
                        else:
                            st.info("Skin score is stable across this session's analyses.")

                    for item in history:
                        st.markdown(f"""
                        <div style="background:#fff;border-radius:12px;padding:14px 16px;margin-bottom:10px;box-shadow:0 4px 10px rgba(0,0,0,0.04);">
                            <strong>{item['timestamp']}</strong> · {item['skin_type']} · Score <strong>{item['skin_score']}</strong><br>
                            <span style="color:#666;font-size:0.9rem;">Acne {item['acne']}% · Dryness {item['dryness']}% · Oiliness {item['oiliness']}% · Sensitivity {item['sensitivity']}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Run your first analysis to start building a quick session history.")
        
    # Decorative element
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
            
def get_level_description(value):
    if value < 30:
        return "Low"
    elif value < 70:
        return "Moderate"
    else:
        return "High"

render_ai_skin_analysis_page()

