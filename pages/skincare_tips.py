import streamlit as st

st.set_page_config(page_title="BeautyBuzzi – Skincare Tips", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600&display=swap');
body, [class*="css"] { font-family: 'Poppins', sans-serif; }
h1 {
    font-family: 'Playfair Display', serif !important;
    background: linear-gradient(90deg, #b76e79, #7c3c50);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.8rem !important;
}
.tip-card {
    background: white; border-radius: 14px; padding: 16px 20px;
    box-shadow: 0 3px 14px rgba(183,110,121,0.09);
    border-left: 5px solid #b76e79; margin-bottom: 12px;
}
.ingredient-card {
    background: #fff8f9; border-radius: 12px; padding: 14px 18px;
    border: 1px solid #f0d0d5; margin-bottom: 10px;
}
.myth-true { border-left: 4px solid #00b894; background: #f0fff8; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; }
.myth-false { border-left: 4px solid #d63031; background: #fff5f5; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; }
.season-card { background: white; border-radius: 14px; padding: 16px; box-shadow: 0 3px 12px rgba(0,0,0,0.06); margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Skincare Tips & Routines")
st.caption("Science-backed tips, personalised routines, and ingredient education for every skin type and gender.")

# ── Gender selector ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Personalise")
    gender = st.radio("I identify as", ["Woman", "Non-binary", "Man"], index=0)
    age_group = st.selectbox("Age Group", ["Under 18", "18–25", "26–35", "36–45", "46–55", "55+"])
    skin_type = st.selectbox("Skin Type", ["Normal", "Oily", "Dry", "Combination", "Sensitive"])
    season = st.selectbox("Current Season", ["Spring", "Summer", "Autumn / Fall", "Winter"])

# ── Tab navigation ─────────────────────────────────────────────────────────────
tabs = st.tabs(["🌟 Daily Routine", "🧪 Ingredients Glossary", "💡 Tips & Myths", "🍎 Diet & Lifestyle", "📅 Seasonal Guide"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — DAILY ROUTINE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader(f"Your Personalised Routine — {gender} · {age_group} · {skin_type} Skin")

    # Routine content based on gender and skin type
    if gender == "Man":
        am_steps = [
            ("🧼 Cleanser", "Gel or foam cleanser for your skin type. Avoid bar soap — it's too stripping."),
            ("💧 Toner (Optional)", "Niacinamide toner helps control oil and tighten pores."),
            ("🌿 Serum", "Vitamin C serum in the AM for antioxidant protection and brightness."),
            ("🧴 Moisturiser + SPF", "The single most impactful step for every man. SPF 30 minimum — daily, always."),
        ]
        pm_steps = [
            ("🧼 Cleanser", "Remove the day's grime, sweat and product build-up."),
            ("🔬 Treatment", "Retinol 0.1–0.5% if 30+. Niacinamide for oily/acne-prone. AHA/BHA for texture 1–2×/week."),
            ("🧴 Moisturiser", "Heavier than daytime. Skin repairs itself overnight."),
        ]
        if age_group in ["36–45", "46–55", "55+"]:
            pm_steps.insert(1, ("👁️ Eye Cream", "Pat (don't rub) an eye cream to reduce dark circles and fine lines."))
        weekly = [
            "Exfoliate 1–2× with a chemical exfoliant (BHA for oily/acne, AHA for texture/dry).",
            "Clay mask 1× a week for oily or combo skin.",
            "Moisturising mask for dry or sensitive skin.",
        ]
        beard_tips = [
            "Wash beard 2–3× a week with a dedicated beard wash (regular shampoo is too harsh).",
            "Apply beard oil daily to hydrate both the hair and skin underneath.",
            "Brush through with a boar-bristle brush to train growth direction and distribute product.",
            "Trim regularly — even if growing it out, tidying the edges makes a huge difference.",
        ]
    else:
        am_steps = [
            ("🧼 Cleanser", f"{'Gentle, creamy cleanser' if skin_type in ['Dry', 'Sensitive'] else 'Gel or foam cleanser'} — morning cleanse removes overnight oil and sweat."),
            ("💧 Toner / Essence", "Hydrating toner (hyaluronic acid, centella) or exfoliating toner (AHA/BHA). Not both."),
            ("💊 Vitamin C Serum", "Brightens, protects from free radicals, and boosts sunscreen efficacy. Morning only."),
            ("🌿 Moisturiser", f"{'Rich cream or balm' if skin_type == 'Dry' else 'Lightweight gel moisturiser' if skin_type == 'Oily' else 'Medium-weight lotion'} for your skin type."),
            ("☀️ SPF 30–50", "The single most anti-ageing product you will ever use. Apply every morning, rain or shine."),
        ]
        pm_steps = [
            ("🧴 Double Cleanse", "Oil cleanser first to dissolve SPF and makeup. Follow with your regular cleanser."),
            ("🔬 Active Treatment", f"{'Retinol 3–5× per week — the gold standard for anti-ageing.' if age_group in ['36–45', '46–55', '55+'] else 'Niacinamide, AHA, BHA or a dedicated treatment serum.'}"),
            ("💧 Hydrating Serum", "Hyaluronic acid or peptides. Layer before moisturiser on damp skin."),
            ("🧴 Night Moisturiser / Cream", "Can be richer than your daytime formula — skin regenerates at night."),
        ]
        if age_group in ["46–55", "55+"]:
            pm_steps.append(("💆 Facial Massage", "2–3 minutes of upward gua sha or jade roller massage boosts circulation and reduces puffiness."))
        weekly = [
            "Exfoliate 1–2× (AHA for dry/dull skin, BHA for oily/acne-prone).",
            "Sheet mask or overnight mask for extra hydration once a week.",
            "Face massage or gua sha — great for lymphatic drainage and glow.",
            "Clean your makeup brushes every 1–2 weeks to prevent bacteria build-up.",
        ]
        beard_tips = []

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### ☀️ Morning Routine")
        for i, (step, desc) in enumerate(am_steps, 1):
            st.markdown(f"""
            <div class="tip-card">
                <b style="color:#b76e79;">Step {i}: {step}</b><br>
                <span style="font-size:0.9rem;color:#444;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown("#### 🌙 Evening Routine")
        for i, (step, desc) in enumerate(pm_steps, 1):
            st.markdown(f"""
            <div class="tip-card" style="border-left-color:#7c3c50;">
                <b style="color:#7c3c50;">Step {i}: {step}</b><br>
                <span style="font-size:0.9rem;color:#444;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("#### 📆 Weekly Extras")
    for w in weekly:
        st.markdown(f"- {w}")

    if beard_tips:
        st.markdown("#### 🧔 Beard Care")
        for b in beard_tips:
            st.markdown(f"- {b}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — INGREDIENTS GLOSSARY
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("🧪 Key Skincare Ingredients — What They Do & Who They're For")
    ingredients = [
        ("Hyaluronic Acid", "💧", "Humectant that holds 1000× its weight in water. Suitable for ALL skin types. Apply to damp skin and seal with moisturiser.", "Hydration, Plumping"),
        ("Niacinamide (B3)", "🌟", "Reduces pores, controls oil, fades dark spots, strengthens the skin barrier. Great for oily, acne-prone, and sensitive skin.", "Oil Control, Pores, Brightening"),
        ("Retinol / Retinoids", "🔬", "The gold-standard anti-ageing ingredient. Increases cell turnover, smooths fine lines, clears acne. Start at 0.1%, build slowly. PM only — always use SPF.", "Anti-Ageing, Acne, Texture"),
        ("Vitamin C", "🍊", "Antioxidant powerhouse. Brightens, evens skin tone, boosts collagen. Use in the AM. L-ascorbic acid (pure Vit C) is most potent but unstable.", "Brightening, Antioxidant"),
        ("AHA (Glycolic / Lactic Acid)", "🫧", "Chemical exfoliant that dissolves the glue between dead skin cells. Glycolic = strongest. Lactic = gentler, more hydrating. Use 1–2× a week PM.", "Exfoliation, Texture, Glow"),
        ("BHA (Salicylic Acid)", "🧴", "Oil-soluble exfoliant — penetrates INTO the pore to unclog from inside. Best for oily, acne-prone and blackhead-prone skin.", "Acne, Pores, Oily Skin"),
        ("Ceramides", "🛡️", "Lipids that form the skin barrier. Essential for dry and sensitive skin. Restore the barrier after active ingredients.", "Barrier Repair, Dry Skin"),
        ("Peptides", "💪", "Short chains of amino acids that signal skin to produce more collagen. Great for anti-ageing and skin firmness.", "Anti-Ageing, Firmness"),
        ("Zinc", "⚡", "Anti-inflammatory mineral. Controls oil production, kills acne bacteria, soothes sensitive skin. Often in SPF and acne treatments.", "Acne, Oil Control, Soothing"),
        ("Centella Asiatica (Cica)", "🌿", "Calming, healing botanical. Reduces redness, repairs the skin barrier, soothes sensitised skin. Great for post-procedure care.", "Soothing, Sensitive, Barrier"),
        ("SPF (Sunscreen)", "☀️", "Not an ingredient — a measure of UV protection. SPF 30 blocks ~97% UVB; SPF 50 blocks ~98%. Chemical vs mineral filters. Use every single day.", "Protection, Anti-Ageing"),
        ("Caffeine", "☕", "Constricts blood vessels — reduces puffiness and dark circles under the eyes temporarily.", "Eye Area, Puffiness"),
    ]
    cols = st.columns(2)
    for i, (name, icon, desc, tags) in enumerate(ingredients):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="ingredient-card">
                <b style="font-size:1rem;">{icon} {name}</b>
                <span style="font-size:0.75rem;background:#fce4e8;color:#7c3c50;border-radius:20px;padding:2px 8px;margin-left:8px;">{tags}</span><br>
                <span style="font-size:0.87rem;color:#444;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — TIPS & MYTHS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("💡 Expert Tips & Common Skincare Myths Debunked")

    st.markdown("#### ✅ Top Tips")
    tips_general = [
        "Always apply products from thinnest to thickest consistency.",
        "Wait 20–30 minutes after retinol before moisturising (the 'sandwich method' can reduce irritation).",
        "Don't mix Vitamin C with niacinamide at the same time — use one AM and one PM.",
        "Never skip SPF, even indoors — UVA penetrates glass and ages skin.",
        "Patch test new actives on the inner arm for 24h before applying to your face.",
        "Change your pillowcase weekly — or use a silk one to reduce friction and bacteria.",
        "Don't pick pimples — it spreads bacteria and causes post-inflammatory hyperpigmentation.",
        "Less is more: a simple 3-step routine done consistently beats a 12-step routine done sporadically.",
    ]
    for t in tips_general:
        st.markdown(f"""
        <div class="tip-card">✅ {t}</div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🔍 Myths vs Facts")
    myths = [
        ("MYTH: Oily skin doesn't need moisturiser.", "FALSE", "Dehydrated oily skin produces MORE oil to compensate. A lightweight gel moisturiser is essential."),
        ("MYTH: Natural / organic = safe.", "FALSE", "Poison ivy is natural. Many allergens are plant-derived. 'Natural' is a marketing term, not a safety standard."),
        ("MYTH: You don't need SPF on a cloudy day.", "FALSE", "80% of UV radiation penetrates clouds. UVA (ageing) penetrates all year, all weather."),
        ("MYTH: Expensive = better.", "FALSE", "Many drugstore products (CeraVe, The Ordinary) outperform luxury brands. Ingredients matter, not price."),
        ("MYTH: You should feel a 'tingle' for it to work.", "FALSE", "Tingling from actives usually means irritation or a compromised skin barrier. Less is more."),
        ("MYTH: Drinking water alone gives you glowing skin.", "FALSE", "Hydration helps but topical moisturisers and a healthy diet have far more impact on skin appearance."),
        ("MYTH: Men don't need skincare.", "FALSE", "Male skin is ~20% thicker, produces more sebum, and is shaved regularly — it needs care just as much."),
    ]
    for myth, verdict, fact in myths:
        color = "#00b894" if verdict == "TRUE" else "#d63031"
        label = "✅ TRUE" if verdict == "TRUE" else "❌ FALSE"
        st.markdown(f"""
        <div class="{'myth-true' if verdict == 'TRUE' else 'myth-false'}">
            <b>{myth}</b><br>
            <span style="font-weight:700;color:{color};">{label}</span>: {fact}
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — DIET & LIFESTYLE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("🍎 Diet, Sleep & Lifestyle for Healthy Skin")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🥗 Skin-Boosting Foods")
        foods = [
            ("🥑 Avocado", "Rich in healthy fats and Vitamin E — deeply moisturises from within."),
            ("🫐 Blueberries", "Packed with antioxidants that protect against free radical damage."),
            ("🐟 Salmon / Oily Fish", "Omega-3 fatty acids reduce inflammation and keep the skin barrier strong."),
            ("🌿 Green Tea", "EGCG compound fights UV damage and has anti-inflammatory properties."),
            ("🥕 Carrots / Sweet Potato", "Beta-carotene converts to Vitamin A (precursor to retinol) in the body."),
            ("🥦 Broccoli / Leafy Greens", "High in Vitamin C (collagen synthesis), Vitamin K and antioxidants."),
            ("🥚 Eggs", "Biotin supports skin barrier function and keratin production."),
            ("🍫 Dark Chocolate (70%+)", "Flavanols improve skin hydration and circulation."),
        ]
        for icon_food, desc in foods:
            st.markdown(f"**{icon_food}** — {desc}")

        st.markdown("#### 💧 Hydration")
        st.markdown("""
        - Aim for **2–3 litres of water** per day (more if active or in hot weather).
        - Herbal teas and water-rich foods (cucumber, watermelon) count.
        - Alcohol and caffeine are dehydrating — balance with extra water.
        - Signs of dehydration in skin: dullness, tightness, exaggerated fine lines.
        """)

    with c2:
        st.markdown("#### 😴 Sleep & Stress")
        st.markdown("""
        - **7–9 hours** of sleep is when skin does the bulk of its repair.
        - Growth hormone peaks during deep sleep — essential for cell renewal.
        - Cortisol (stress hormone) breaks down collagen and triggers acne flares.
        - Try a short meditation or breathing exercise before bed to lower cortisol.
        - Sleep on a **silk or satin pillowcase** to reduce friction and moisture loss.
        """)

        st.markdown("#### 🏃 Exercise")
        st.markdown("""
        - Cardio improves circulation, delivering nutrients and oxygen to skin cells.
        - Sweating helps clear pores (if you cleanse immediately after).
        - Yoga and stretching reduce cortisol levels.
        - Always cleanse before exercise to prevent sweat mixing with SPF/makeup.
        """)

        st.markdown("#### 🚫 What to Avoid")
        st.markdown("""
        - **Sugar** — causes glycation, which stiffens collagen and accelerates ageing.
        - **Dairy** (for some people) — can trigger acne in those sensitive to hormones in milk.
        - **Smoking** — reduces blood flow, depletes Vitamin C, causes wrinkles and dullness.
        - **Alcohol** — dehydrates, dilates blood vessels (redness), depletes antioxidants.
        - **Processed / fried foods** — pro-inflammatory and can worsen acne and redness.
        """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — SEASONAL GUIDE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader(f"📅 {season} Skincare Adjustments")
    seasonal_tips = {
        "Spring": {
            "icon": "🌸",
            "overview": "Transition out of heavy winter products. Focus on renewal and lighter formulas.",
            "tips": [
                "Swap heavy winter creams for lighter gel or lotion moisturisers.",
                "Add a Vitamin C serum as daylight increases.",
                "Begin exfoliating more regularly to remove winter dullness.",
                "Reintroduce SPF 50 as UV index rises.",
                "Stay alert to pollen — it can trigger reactive skin and rosacea flares.",
            ],
            "products": ["Gel moisturiser", "Vitamin C serum", "SPF 50", "Gentle AHA exfoliant"],
        },
        "Summer": {
            "icon": "☀️",
            "overview": "Sun protection is the absolute priority. Keep it light and control oil.",
            "tips": [
                "SPF 50 minimum, reapply every 2 hours if outdoors.",
                "Switch to oil-free or mattifying moisturisers.",
                "Use a micellar water or cleansing oil to remove sunscreen properly.",
                "Keep retinol to 1× a week if spending a lot of time in the sun.",
                "Carry a facial mist for refreshing and setting makeup outdoors.",
                "Antioxidant serum (Vitamin C / E) boosts SPF and fights UV damage.",
            ],
            "products": ["SPF 50", "Oil-free moisturiser", "Micellar water", "Antioxidant serum", "Facial mist"],
        },
        "Autumn / Fall": {
            "icon": "🍂",
            "overview": "Repair summer damage. Start rebuilding the skin barrier ahead of winter.",
            "tips": [
                "Reintroduce retinol (less sun = safer to ramp up usage).",
                "Add a peptide or hyaluronic acid serum for repair.",
                "Switch back to slightly richer moisturisers as humidity drops.",
                "Exfoliate to address any summer hyperpigmentation.",
                "Don't drop your SPF — UVA rays are year-round.",
            ],
            "products": ["Retinol serum", "Peptide serum", "Medium-weight moisturiser", "SPF 30+"],
        },
        "Winter": {
            "icon": "❄️",
            "overview": "Barrier repair is everything. Fight dryness, wind, and central heating.",
            "tips": [
                "Use a richer cream or balm — especially at night.",
                "Apply moisturiser on slightly damp skin to lock in hydration.",
                "A humidifier in your bedroom combats central heating dryness.",
                "Take shorter, lukewarm showers — hot water strips the skin barrier.",
                "Apply a barrier-repairing hand cream after every wash.",
                "Keep retinol but reduce frequency if skin becomes very dry.",
            ],
            "products": ["Rich night cream", "Ceramide moisturiser", "Hyaluronic acid serum", "Humidifier", "Hand cream"],
        },
    }

    s_data = seasonal_tips[season]
    st.markdown(f"### {s_data['icon']} {season} — {s_data['overview']}")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Seasonal Tips:**")
        for t in s_data["tips"]:
            st.markdown(f"- {t}")
    with c2:
        st.markdown("**Recommended Products:**")
        for p in s_data["products"]:
            st.markdown(f"- {p}")

    st.markdown("---")
    st.info("💡 Your skin takes about 4 weeks to visibly respond to seasonal adjustments. Introduce changes gradually.")

st.markdown("---")
st.caption("© 2025 BeautyBuzzi | Evidence-based skincare education for everyone")
