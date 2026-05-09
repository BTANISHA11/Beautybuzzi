import streamlit as st
import base64
from PIL import Image
import io

from services.product_catalog import enrich_product_list, enrich_product_map
from services.product_offers import ProductOfferService


offer_service = ProductOfferService()


def render_offer_comparison(product, key_prefix, accent_color="#7c3c50"):
    snapshot = offer_service.get_snapshot(product)
    link_cols = st.columns([1.1, 1.2, 2.2])
    with link_cols[0]:
        st.link_button(
            "Buy best offer",
            snapshot.best_offer.url,
            use_container_width=True,
        )
    with link_cols[1]:
        if len(snapshot.offers) > 1:
            st.link_button(
                f"Buy from {snapshot.offers[1].retailer}",
                snapshot.offers[1].url,
                use_container_width=True,
            )
    with link_cols[2]:
        st.markdown(
            f"<div style='padding:10px 14px;border-radius:12px;background:#fff7f8;border:1px solid #f0d6dc;color:{accent_color};font-size:0.9rem;'>"
            f"<b>Best price:</b> ${snapshot.best_offer.price:.2f} at {snapshot.best_offer.retailer} · {snapshot.comparison_label} · <b>Source:</b> {snapshot.source}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with st.expander(f"Compare prices for {product['name']}"):
        comparison_rows = [
            {
                "Retailer": offer.retailer,
                "Price": f"${offer.price:.2f}",
                "Availability": "In stock" if offer.in_stock else "Out of stock",
                "Shipping": offer.shipping_note,
            }
            for offer in snapshot.offers
        ]
        st.table(comparison_rows)
        retailer_cols = st.columns(len(snapshot.offers))
        for idx, offer in enumerate(snapshot.offers):
            with retailer_cols[idx]:
                st.link_button(
                    f"Open {offer.retailer}",
                    offer.url,
                    key=f"{key_prefix}_offer_{idx}",
                    use_container_width=True,
                )


def render_product_card(product, key_prefix, accent_color="#b76e79", description_key=None, weekly_note=None):
    description_field = description_key or ("desc" if "desc" in product else "description")
    description = product.get(description_field, "")
    st.markdown(
        f"""
        <div class="product-card" style="border-left-color:{accent_color};">
            <b>{product['icon']} {product['name']}</b> — <span style="color:{accent_color};">{product['brand']}</span> · <b>${product['price']}</b><br>
            <span style="color:#555;font-size:0.9rem;">{description}</span>
            {f'<p style="margin:10px 0 0 0; color:{accent_color}; font-family: Poppins, sans-serif; font-weight: 500; font-size: 0.85rem;">{weekly_note}</p>' if weekly_note else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_offer_comparison(product, key_prefix, accent_color=accent_color)



def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
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
    
    /* Card styling */
    .css-1r6slb0 {
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        background-color: rgba(255, 255, 255, 0.85) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        backdrop-filter: blur(4px) !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 30px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        color: white !important;
        background: linear-gradient(90deg, #b76e79, #7c3c50) !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(123, 60, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 7px 15px rgba(123, 60, 80, 0.4) !important;
    }
    
    /* Selectbox & multiselect styling */
    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 30px !important;
        border: 1px solid #e6ccd2 !important;
        background-color: white !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        border-radius: 30px !important;
        border: 1px solid #e6ccd2 !important;
        background-color: white !important;
    }
    
    /* Product card styling */
    .product-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #b76e79;
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Concern tags styling */
    .concern-tag {
        display: inline-block;
        background-color: #f8e1e5;
        color: #7c3c50;
        border-radius: 20px;
        padding: 5px 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 20px;
        color: #7c3c50;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    
    /* Loading animation */
    .loading {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    /* Decorative elements */
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #b76e79, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    /* Responsive typography */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_product_recommendations_page():
    # Apply background and CSS
    local_css()
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Add Google Font
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )
    
    # Create page layout with columns for better design
    col1, col2, col3 = st.columns([1, 10, 1])
    
    with col2:
        # Header section
        st.markdown('<h1>Glow Guide</h1>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: left; margin-bottom: 25px; font-family: 'Poppins', sans-serif;">
                <p style="font-size: 1.2rem; color: #7c3c50; font-weight: 300;">
                    Discover your perfect skincare routine ✨
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Decorative element
        st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
        
        # Introduction card
        st.markdown(
            """
            <div style="background-color: rgba(255, 255, 255, 0.7); 
                        border-radius: 15px; 
                        padding: 20px; 
                        margin-bottom: 25px; 
                        text-align: left;
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                <h3 style="color: #7c3c50; font-family: 'Poppins', sans-serif; font-weight: 600; margin-bottom: 15px;">
                    Your Personal Skincare Assistant
                </h3>
                <p style="color: #5a5a5a; font-family: 'Poppins', sans-serif; font-size: 1rem;">
                    Tell us about your skin, and we'll recommend the perfect products for your unique needs. 
                    Our expert selections are tailored to your skin type and concerns for the most radiant results. 
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Input section with nicer styling
        st.markdown(
            """
            <h3 style="font-family: 'Poppins', sans-serif; color: #7c3c50; font-size: 1.5rem; margin-top: 10px;">
                Tell us about your skin
            </h3>
            """, 
            unsafe_allow_html=True
        )

        # ── Gender & Age selectors ────────────────────────────────────────────
        g_col, a_col = st.columns(2)
        with g_col:
            gender = st.selectbox("👤 I identify as", ["Woman", "Man", "Non-binary"])
        with a_col:
            age_group = st.selectbox("🎂 Age Group", ["Under 18", "18–25", "26–35", "36–45", "46–55", "55+"])

        # Men's grooming path
        if gender == "Man":
            st.markdown("---")
            st.markdown("### 💈 Men's Grooming Guide")
            men_skin_types = {"Normal": "✨", "Oily": "💦", "Dry": "🏜️", "Sensitive": "🌸"}
            sel_men_type = st.selectbox("Skin Type", [f"{v} {k}" for k, v in men_skin_types.items()])
            men_skin_type = sel_men_type.split(" ")[1]
            men_budget = st.slider("Budget ($)", 0, 150, (20, 80), step=5)
            has_beard = st.checkbox("🧔 I have / want to grow a beard")

            men_products = {
                "Normal": [
                    {"name": "Daily Face Wash", "brand": "Bulldog", "price": 10, "icon": "🧼", "desc": "Gentle, natural ingredients formula for everyday cleansing."},
                    {"name": "Invisible SPF 50 Moisturiser", "brand": "Kiehl's", "price": 35, "icon": "☀️", "desc": "Hydrates and protects in one step — perfect for minimal routines."},
                    {"name": "Niacinamide 10% Serum", "brand": "The Ordinary", "price": 9, "icon": "💧", "desc": "Controls oil, minimises pores, and evens skin tone."},
                    {"name": "Eye Gel", "brand": "Jack Black", "price": 30, "icon": "👁️", "desc": "Reduces puffiness and dark circles under the eyes."},
                ],
                "Oily": [
                    {"name": "Purifying Gel Cleanser", "brand": "Lab Series", "price": 22, "icon": "🧼", "desc": "Removes excess oil and unclogs pores."},
                    {"name": "BHA Exfoliant", "brand": "Paula's Choice", "price": 33, "icon": "💧", "desc": "2% salicylic acid — weekly use to keep pores clear."},
                    {"name": "Oil-Free Lightweight Moisturiser", "brand": "Baxter of California", "price": 28, "icon": "🌿", "desc": "Hydrates without shine or greasiness."},
                    {"name": "Matte SPF 50", "brand": "Supergoop", "price": 38, "icon": "☀️", "desc": "Invisible matte finish sunscreen."},
                    {"name": "Charcoal Clay Mask", "brand": "Clinique", "price": 29, "icon": "🧖", "desc": "Deep-cleans pores. Use 1–2× weekly."},
                ],
                "Dry": [
                    {"name": "Hydrating Cream Cleanser", "brand": "CeraVe", "price": 14, "icon": "🧼", "desc": "Cleanses without disrupting the moisture barrier."},
                    {"name": "Hyaluronic Acid Serum", "brand": "The Inkey List", "price": 10, "icon": "💧", "desc": "Draws moisture into the skin."},
                    {"name": "Rich Daily Moisturiser", "brand": "Kiehl's", "price": 42, "icon": "🧴", "desc": "Thick cream formula for lasting hydration."},
                    {"name": "Hydrating SPF 50", "brand": "Elta MD", "price": 37, "icon": "☀️", "desc": "Moisturises and protects in one."},
                ],
                "Sensitive": [
                    {"name": "Gentle Fragrance-Free Cleanser", "brand": "Vanicream", "price": 12, "icon": "🧼", "desc": "No dyes, fragrance or harsh surfactants."},
                    {"name": "Centella Serum", "brand": "COSRX", "price": 18, "icon": "🌿", "desc": "Calms redness and repairs the skin barrier."},
                    {"name": "Soothing Moisturiser", "brand": "Avène", "price": 25, "icon": "🧴", "desc": "Thermal spring water formula for reactive skin."},
                    {"name": "Mineral SPF 50", "brand": "EltaMD", "price": 40, "icon": "☀️", "desc": "Physical-only sunscreen — gentler than chemical filters."},
                ],
            }
            men_products = enrich_product_map(men_products, segment="men", category="skincare")

            beard_products = [
                {"name": "Beard Oil", "brand": "Beardbrand", "price": 25, "icon": "🛢️", "desc": "Conditions the beard and moisturises the skin underneath. Apply daily."},
                {"name": "Beard Balm", "brand": "Mountaineer Brand", "price": 18, "icon": "🪮", "desc": "Light hold and conditioning for medium-to-long beards."},
                {"name": "Beard Wash", "brand": "Scotch Porter", "price": 20, "icon": "🧼", "desc": "Gentle cleanser specifically for facial hair — use 2–3× a week."},
                {"name": "Beard Shaper / Brush", "brand": "Zeus", "price": 15, "icon": "🪥", "desc": "Natural bristle brush trains the beard direction and distributes product evenly."},
                {"name": "Beard Trimmer", "brand": "Philips Norelco", "price": 45, "icon": "✂️", "desc": "Precision trimming for all beard lengths and styles."},
            ]
            beard_products = enrich_product_list(beard_products, segment="men", collection="beard-care", category="grooming")

            filtered_men = [p for p in men_products.get(men_skin_type, []) if men_budget[0] <= p["price"] <= men_budget[1]]

            st.markdown(f"#### 🧴 {men_skin_type} Skin — Recommended Products (${men_budget[0]}–${men_budget[1]})")
            if filtered_men:
                for idx, p in enumerate(filtered_men):
                    render_product_card(p, key_prefix=f"men_core_{idx}", accent_color="#7c3c50", description_key="desc")
            else:
                st.info("No products in this budget range — try widening the slider.")

            if has_beard:
                st.markdown("#### 🧔 Beard Care Products")
                filtered_beard = [p for p in beard_products if men_budget[0] <= p["price"] <= men_budget[1]]
                if filtered_beard:
                    for idx, p in enumerate(filtered_beard):
                        render_product_card(p, key_prefix=f"beard_{idx}", accent_color="#6c5ce7", description_key="desc")
                else:
                    st.info("No beard products in this budget range.")

            # Men's routine guide
            st.markdown("---")
            st.markdown("#### 📋 Simple Men's Skincare Routine")
            am = ["Gentle face wash", "Serum (niacinamide or vitamin C)", "Moisturiser with SPF 50"]
            pm = ["Face wash", "Treatment serum (retinol 1–2× a week if 30+)", "Moisturiser"]
            if has_beard:
                am.insert(1, "Post-shave balm or beard oil on facial hair")
                pm.append("Beard oil (comb through beard)")
            if age_group in ["36–45", "46–55", "55+"]:
                pm.insert(2, "Retinol 0.1–0.3% (start slowly, build up)")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**☀️ Morning**")
                for s in am:
                    st.markdown(f"- {s}")
            with c2:
                st.markdown("**🌙 Evening**")
                for s in pm:
                    st.markdown(f"- {s}")

            st.markdown("---")
            st.info("💡 **Minimum viable routine:** cleanser + SPF in the AM, cleanser + moisturiser in the PM. That's it. Everything else is a bonus.")
            return   # Exit the function — men's section is complete

        # ── Women / Non-binary continue with the existing skin-type section ───
        
        # Skin type selection with icons
        skin_types = {
            "Oily": "💦",
            "Dry": "🏜️",
            "Combination": "⚖️",
            "Sensitive": "🌸",
            "Normal": "✨"
        }
        
        skin_type_options = [f"{icon} {skin_type}" for skin_type, icon in skin_types.items()]
        selected_skin_type = st.selectbox(
            "What's your skin type?",
            skin_type_options
        )
        # Extract actual skin type without the emoji
        skin_type = selected_skin_type.split(" ")[1]
        
        # Skin concerns selection with better UI
        concern_icons = {
            "Acne": "🔴",
            "Wrinkles": "🔬",
            "Dark Spots": "🟤",
            "Dryness": "🏜️",
            "Sensitivity": "❗",
            "Oiliness": "💧",
            "Uneven Skin Tone": "🌓",
            "Pores": "🔍",
            "Redness": "🟥"
        }
        
        concern_options = [f"{icon} {concern}" for concern, icon in concern_icons.items()]
        selected_concerns = st.multiselect(
            "What are your skin concerns?",
            concern_options
        )
        # Extract actual concerns without the emojis
        skin_concerns = [concern.split(" ", 1)[1] for concern in selected_concerns]
        
        # Budget slider
        budget = st.slider(
            "Your budget range ($)",
            0, 200, (30, 100),
            step=10
        )
        
        # Age-based additions
        if age_group in ["36–45", "46–55", "55+"]:
            st.info("💡 Based on your age group, we've added anti-ageing and collagen-supporting products to your recommendations.")
        
        # Product preferences
        st.markdown(
            """
            <h4 style="font-family: 'Poppins', sans-serif; color: #7c3c50; font-size: 1.2rem; margin-top: 15px;">
                Product Preferences
            </h4>
            """, 
            unsafe_allow_html=True
        )
        
        cols = st.columns(3)
        with cols[0]:
            cruelty_free = st.checkbox("Cruelty-Free 🐰")
        with cols[1]:
            vegan = st.checkbox("Vegan 🌱")
        with cols[2]:
            fragrance_free = st.checkbox("Fragrance-Free 🚫")
        
        # Recommendations database based on skin type
        recommendations = {
            "Oily": {
                "products": [
                    {"name": "Gentle Foaming Cleanser", "brand": "CeraVe", "price": 15, "description": "Removes excess oil without stripping the skin", "icon": "🧼"},
                    {"name": "Oil Control Toner", "brand": "Paula's Choice", "price": 29, "description": "Minimizes pores and controls sebum production", "icon": "💦"},
                    {"name": "Salicylic Acid Serum", "brand": "The Ordinary", "price": 12, "description": "Unclogs pores and fights acne", "icon": "💧"},
                    {"name": "Oil-Free Gel Moisturizer", "brand": "Neutrogena", "price": 18, "description": "Hydrates without adding oil", "icon": "🌿"},
                    {"name": "Clay Purifying Mask", "brand": "Kiehl's", "price": 39, "description": "Weekly treatment to absorb excess oil and impurities", "icon": "🧖‍♀️"},
                    {"name": "Matte Finish Sunscreen", "brand": "Supergoop", "price": 38, "description": "SPF 40 with oil-controlling properties", "icon": "☀️"}
                ]
            },
            "Dry": {
                "products": [
                    {"name": "Hydrating Cream Cleanser", "brand": "La Roche-Posay", "price": 16, "description": "Cleans without stripping natural oils", "icon": "🧼"},
                    {"name": "Hyaluronic Acid Serum", "brand": "The Inkey List", "price": 10, "description": "Attracts and retains moisture", "icon": "💧"},
                    {"name": "Rich Moisturizing Cream", "brand": "First Aid Beauty", "price": 34, "description": "Deeply nourishes dry skin", "icon": "🥥"},
                    {"name": "Squalane Facial Oil", "brand": "Biossance", "price": 32, "description": "Locks in moisture and restores skin barrier", "icon": "🌸"},
                    {"name": "Overnight Hydrating Mask", "brand": "Laneige", "price": 28, "description": "Replenishes moisture while you sleep", "icon": "😴"},
                    {"name": "Hydrating Sunscreen", "brand": "Elta MD", "price": 37, "description": "SPF 46 with hydrating properties", "icon": "☀️"}
                ]
            },
            "Combination": {
                "products": [
                    {"name": "Balanced Gel Cleanser", "brand": "Youth To The People", "price": 36, "description": "Balances oily and dry areas", "icon": "🧼"},
                    {"name": "PHA Toning Solution", "brand": "COSRX", "price": 22, "description": "Gentle exfoliation for balanced skin", "icon": "💦"},
                    {"name": "Niacinamide Serum", "brand": "Good Molecules", "price": 14, "description": "Regulates oil production and improves texture", "icon": "⚖️"},
                    {"name": "Balancing Moisturizer", "brand": "Origins", "price": 33, "description": "Hydrates dry areas while controlling oily zones", "icon": "🌿"},
                    {"name": "Multi-Masking Kit", "brand": "Fresh", "price": 58, "description": "Different masks for different facial areas", "icon": "🧖‍♀️"},
                    {"name": "Lightweight Sunscreen", "brand": "Innisfree", "price": 27, "description": "SPF 50 that works well for mixed skin types", "icon": "☀️"}
                ]
            },
            "Sensitive": {
                "products": [
                    {"name": "Ultra Gentle Cleanser", "brand": "Vanicream", "price": 11, "description": "Free from common irritants", "icon": "🧼"},
                    {"name": "Cica Repair Serum", "brand": "Dr. Jart+", "price": 48, "description": "Calms and soothes irritated skin", "icon": "🍃"},
                    {"name": "Barrier Repair Moisturizer", "brand": "Avène", "price": 35, "description": "Strengthens skin's natural defenses", "icon": "💖"},
                    {"name": "Centella Calming Toner", "brand": "Purito", "price": 19, "description": "Reduces redness and inflammation", "icon": "🌼"},
                    {"name": "Oat Repairing Mask", "brand": "Aveeno", "price": 24, "description": "Soothes skin with colloidal oatmeal", "icon": "🌾"},
                    {"name": "Mineral Sunscreen", "brand": "Coola", "price": 42, "description": "SPF 50 with zinc oxide for sensitive skin", "icon": "☀️"}
                ]
            },
            "Normal": {
                "products": [
                    {"name": "Amino Acid Cleanser", "brand": "Kiehl's", "price": 30, "description": "Maintains skin's natural balance", "icon": "🧼"},
                    {"name": "Vitamin C Serum", "brand": "Timeless", "price": 25, "description": "Brightens and protects", "icon": "🍊"},
                    {"name": "Peptide Moisturizer", "brand": "Drunk Elephant", "price": 68, "description": "Supports healthy skin function", "icon": "🌿"},
                    {"name": "Exfoliating Toner", "brand": "Pixi", "price": 29, "description": "Keeps skin smooth and radiant", "icon": "✨"},
                    {"name": "Radiance Boosting Mask", "brand": "Tatcha", "price": 68, "description": "Promotes glowing complexion", "icon": "🌟"},
                    {"name": "Antioxidant Sunscreen", "brand": "La Roche-Posay", "price": 36, "description": "SPF 50 with additional skin benefits", "icon": "☀️"}
                ]
            }
        }
        recommendations = {
            key: {
                **value,
                "products": enrich_product_list(
                    value["products"],
                    segment="women-non-binary",
                    collection=f"{key.lower()}-core",
                    category="skincare",
                ),
            }
            for key, value in recommendations.items()
        }
        
        # Additional product recommendations based on concerns
        concern_products = {
            "Acne": [
                {"name": "Benzoyl Peroxide Treatment", "brand": "Paula's Choice", "price": 19, "description": "Targets acne-causing bacteria", "icon": "🛡️"},
                {"name": "Spot Treatment Gel", "brand": "Kate Somerville", "price": 26, "description": "Reduces inflammation and size of blemishes", "icon": "🔴"}
            ],
            "Wrinkles": [
                {"name": "Retinol Serum", "brand": "Sunday Riley", "price": 85, "description": "Reduces fine lines and promotes collagen", "icon": "🔬"},
                {"name": "Peptide Eye Cream", "brand": "The Inkey List", "price": 15, "description": "Targets crow's feet and under-eye lines", "icon": "👁️"}
            ],
            "Dark Spots": [
                {"name": "Tranexamic Acid Serum", "brand": "Good Molecules", "price": 12, "description": "Fades hyperpigmentation", "icon": "🟤"},
                {"name": "Alpha Arbutin Solution", "brand": "The Ordinary", "price": 9, "description": "Reduces appearance of dark spots", "icon": "🍊"}
            ],
            "Dryness": [
                {"name": "Ceramide Cream", "brand": "Dr. Jart+", "price": 48, "description": "Restores skin barrier and locks in moisture", "icon": "💧"},
                {"name": "Hydrating Face Mist", "brand": "Tatcha", "price": 48, "description": "Instant hydration throughout the day", "icon": "💦"}
            ],
            "Sensitivity": [
                {"name": "Centella Serum", "brand": "COSRX", "price": 26, "description": "Calms irritation and redness", "icon": "💖"},
                {"name": "Oat Barrier Cream", "brand": "La Roche-Posay", "price": 32, "description": "Strengthens sensitive skin", "icon": "🌾"}
            ],
            "Oiliness": [
                {"name": "Oil-Control Primer", "brand": "Fenty Skin", "price": 32, "description": "Mattifies and controls shine", "icon": "🌿"},
                {"name": "Charcoal Deep Cleanse", "brand": "Origins", "price": 25, "description": "Detoxifies and absorbs excess oil", "icon": "⚫"}
            ],
            "Uneven Skin Tone": [
                {"name": "Glycolic Acid Toner", "brand": "Pixi", "price": 29, "description": "Exfoliates for even complexion", "icon": "✨"},
                {"name": "Brightening Mask", "brand": "Summer Fridays", "price": 46, "description": "Illuminates dull skin", "icon": "🌟"}
            ],
            "Pores": [
                {"name": "Pore-Minimizing Serum", "brand": "Tatcha", "price": 88, "description": "Refines and tightens pores", "icon": "🔍"},
                {"name": "BHA Liquid Exfoliant", "brand": "Paula's Choice", "price": 32, "description": "Clears and minimizes pores", "icon": "💦"}
            ],
            "Redness": [
                {"name": "Green Color Corrector", "brand": "Dr. Jart+", "price": 52, "description": "Neutralizes redness instantly", "icon": "🟩"},
                {"name": "Cica Recovery Balm", "brand": "Etude House", "price": 24, "description": "Calms and reduces redness", "icon": "🌱"}
            ]
        }
        concern_products = {
            concern: enrich_product_list(
                products,
                segment="women-non-binary",
                collection=f"concern-{concern.lower()}",
                category="treatment",
            )
            for concern, products in concern_products.items()
        }
        
        # Button to get recommendations
        if st.button("✨ Get Your Personalized Routine ✨"):
            # Show loading animation
            with st.spinner('Analyzing your skin profile...'):
                import time
                time.sleep(1.5)  # Simulate processing time
            
            # Display results in a beautiful format
            st.markdown(
                f"""
                <div style="text-align: center; margin: 30px 0 20px 0;">
                    <h2 style="color: #7c3c50; font-family: 'Playfair Display', serif; font-weight: 700;">
                        Your Perfect Skincare Routine
                    </h2>
                    <p style="color: #5a5a5a; font-family: 'Poppins', sans-serif;">
                        Curated for your {skin_type.lower()} skin within ${budget[0]}-${budget[1]} range
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Display concern tags
            if skin_concerns:
                st.markdown('<div style="text-align: center; margin-bottom: 25px;">', unsafe_allow_html=True)
                for concern in skin_concerns:
                    st.markdown(f'<span class="concern-tag">{concern_icons.get(concern, "✨")} {concern}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Morning and evening routine sections
            routine_tabs = st.tabs(["🌞 Morning Routine", "🌙 Evening Routine", "💫 Weekly Treatments"])
            
            # Filter products by budget
            filtered_products = [p for p in recommendations[skin_type]["products"] if budget[0] <= p["price"] <= budget[1]]
            
            # Apply preferences filters if selected
            if cruelty_free or vegan or fragrance_free:
                # In a real app, you'd have these attributes in your product data
                # This is just a simulation for the UI
                filtered_products = filtered_products[:max(3, len(filtered_products)-1)]
            
            # If no products in budget range, show message
            if not filtered_products:
                st.warning("No products match your budget range. Please adjust your budget.")
            else:
                # Morning routine
                with routine_tabs[0]:
                    st.markdown(
                        """
                        <p style="text-align: center; color: #7c3c50; font-family: 'Poppins', sans-serif; margin-bottom: 20px;">
                            Start your day with these products for healthy, protected skin
                        </p>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Morning products (usually cleanser, serum, moisturizer, sunscreen)
                    morning_products = [p for p in filtered_products if p["name"].lower().find("cleanser") >= 0 or 
                                                                        p["name"].lower().find("serum") >= 0 or 
                                                                        p["name"].lower().find("moisturizer") >= 0 or
                                                                        p["name"].lower().find("sunscreen") >= 0]
                    
                    # Ensure we have at least some products
                    if len(morning_products) < 3:
                        morning_products = filtered_products[:3]
                    
                    # Create order of routine
                    routine_order = ["cleanser", "toner", "serum", "moisturizer", "sunscreen"]
                    ordered_products = []
                    
                    # Try to order products logically for routine
                    for step in routine_order:
                        for product in morning_products:
                            if step in product["name"].lower() and product not in ordered_products:
                                ordered_products.append(product)
                    
                    # Add any remaining products
                    for product in morning_products:
                        if product not in ordered_products:
                            ordered_products.append(product)
                    
                    # Display morning products as cards
                    for i, product in enumerate(ordered_products[:4]):  # Limit to 4 products for morning
                        render_product_card(product, key_prefix=f"morning_{i}", accent_color="#7c3c50")
                
                # Evening routine
                with routine_tabs[1]:
                    st.markdown(
                        """
                        <p style="text-align: center; color: #7c3c50; font-family: 'Poppins', sans-serif; margin-bottom: 20px;">
                            Wind down with these products to repair and restore your skin while you sleep
                        </p>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Evening products (usually double cleanse, treatment, night cream, oil)
                    evening_products = [p for p in filtered_products if p["name"].lower().find("cleanser") >= 0 or 
                                                                       p["name"].lower().find("oil") >= 0 or 
                                                                       p["name"].lower().find("cream") >= 0 or
                                                                       p["name"].lower().find("serum") >= 0]
                    
                    # Ensure we have at least some products
                    if len(evening_products) < 3:
                        evening_products = filtered_products[:3]
                    
                    # Display evening products as cards
                    for i, product in enumerate(evening_products[:4]):  # Limit to 4 products for evening
                        render_product_card(product, key_prefix=f"evening_{i}", accent_color="#7c3c50")
                
                # Weekly treatments
                with routine_tabs[2]:
                    st.markdown(
                        """
                        <p style="text-align: center; color: #7c3c50; font-family: 'Poppins', sans-serif; margin-bottom: 20px;">
                            Boost your skincare routine with these special treatments 1-2 times per week
                        </p>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Weekly treatments (usually masks, exfoliants)
                    weekly_products = [p for p in filtered_products if p["name"].lower().find("mask") >= 0 or 
                                                                      p["name"].lower().find("exfoliat") >= 0]
                    
                    # If no specific treatments found, select a couple products that might work
                    if not weekly_products and filtered_products:
                        weekly_products = filtered_products[-2:]
                    
                    # Display weekly treatment products as cards
                    for i, product in enumerate(weekly_products[:2]):  # Limit to 2 products for treatments
                        render_product_card(
                            product,
                            key_prefix=f"weekly_{i}",
                            accent_color="#7c3c50",
                            weekly_note="Use 1-2 times per week for best results",
                        )
                    
                    # If no weekly products found
                    if not weekly_products:
                        st.info("No specific weekly treatments found in your budget range. Consider increasing your budget for special treatments.")
                
                # Concern-specific products
                if skin_concerns:
                    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
                    st.markdown(
                        """
                        <h3 style="text-align: center; color: #7c3c50; font-family: 'Playfair Display', serif; margin: 30px 0 20px 0;">
                            Products for Your Specific Concerns
                        </h3>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # Create columns layout for concerns
                    col_count = min(len(skin_concerns), 2)  # Max 2 columns
                    if col_count > 0:
                        concern_cols = st.columns(col_count)
                        
                        for idx, concern in enumerate(skin_concerns[:2]):  # Limit to first 2 concerns
                            with concern_cols[idx % col_count]:
                                st.markdown(
                                    f"""
                                    <div style="background-color: rgba(255, 255, 255, 0.7); 
                                                border-radius: 15px; 
                                                padding: 15px; 
                                                margin-bottom: 15px;
                                                border: 1px solid rgba(255, 255, 255, 0.3);
                                                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);">
                                        <h4 style="text-align: center; color: #7c3c50; font-family: 'Poppins', sans-serif; margin-bottom: 15px;">
                                            {concern_icons.get(concern, "✨")} For {concern}
                                        </h4>
                                    """, 
                                    unsafe_allow_html=True
                                )
                                
                                # Get concern-specific products
                                if concern in concern_products:
                                    filtered_concern_products = [p for p in concern_products[concern] if budget[0] <= p["price"] <= budget[1]]
                                    
                                    if filtered_concern_products:
                                        for product_idx, product in enumerate(filtered_concern_products):
                                            render_product_card(
                                                product,
                                                key_prefix=f"concern_{concern}_{product_idx}",
                                                accent_color="#7c3c50",
                                            )
                                    else:
                                        st.markdown(
                                            """
                                            <p style="color: #7c3c50; font-family: 'Poppins', sans-serif; font-size: 0.9rem; text-align: center;">
                                                No products in your budget range. Consider adjusting your budget.
                                            </p>
                                            """, 
                                            unsafe_allow_html=True
                                        )
                                else:
                                    st.markdown(
                                        """
                                        <p style="color: #7c3c50; font-family: 'Poppins', sans-serif; font-size: 0.9rem; text-align: center;">
                                            No specific products found for this concern.
                                        </p>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                # Routine tips
                st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <h3 style="text-align: center; color: #7c3c50; font-family: 'Playfair Display', serif; margin: 30px 0 20px 0;">
                        Skincare Tips
                    </h3>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Tips based on skin type
                tips = {
                    "Oily": [
                        "Don't over-wash your face - it can stimulate more oil production",
                        "Use blotting papers during the day to absorb excess oil",
                        "Look for products labeled 'non-comedogenic' to prevent clogged pores",
                        "Don't skip moisturizer - dehydrated skin can produce more oil"
                    ],
                    "Dry": [
                        "Take shorter, lukewarm showers to prevent stripping natural oils",
                        "Apply moisturizer on damp skin to lock in hydration",
                        "Consider using a humidifier in your bedroom",
                        "Drink plenty of water throughout the day"
                    ],
                    "Combination": [
                        "Multi-mask by applying different products to different areas",
                        "Focus oil-controlling products on T-zone only",
                        "Layer lightweight hydrating products on dry areas",
                        "Consider using different cleansers morning and night"
                    ],
                    "Sensitive": [
                        "Always patch test new products before full application",
                        "Avoid products with alcohol, fragrance, and essential oils",
                        "Introduce new products one at a time with at least a week in between",
                        "Keep your routine simple with fewer products"
                    ],
                    "Normal": [
                        "Maintain your skin balance with consistent skincare",
                        "Focus on protection during the day and repair at night",
                        "Don't forget your neck and décolletage in your routine",
                        "Regular exfoliation (1-2 times per week) helps maintain radiance"
                    ]
                }
                
                # Display tips in a nice format
                tip_cols = st.columns(2)
                for i, tip in enumerate(tips[skin_type]):
                    with tip_cols[i % 2]:
                        st.markdown(
                            f"""
                            <div style="background-color: rgba(255, 255, 255, 0.7); 
                                        border-radius: 15px; 
                                        padding: 15px; 
                                        margin-bottom: 15px;
                                        border: 1px solid rgba(255, 255, 255, 0.3);
                                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                                        display: flex;
                                        align-items: flex-start;">
                                <div style="background: linear-gradient(90deg, #fce1e4, #fcf4dd); 
                                            border-radius: 50%; 
                                            min-width: 30px; 
                                            height: 30px; 
                                            display: flex; 
                                            align-items: center; 
                                            justify-content: center;
                                            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                                            margin-right: 10px;
                                            margin-top: 2px;">
                                    <span style="font-size: 0.9rem; font-weight: bold; color: #7c3c50;">✓</span>
                                </div>
                                <p style="margin: 0; color: #5a5a5a; font-family: 'Poppins', sans-serif; font-size: 0.95rem;">
                                    {tip}
                                </p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                
                # Save as PDF option (not functional in Streamlit but looks good)
                st.markdown(
                    """
                    <div style="text-align: center; margin: 30px 0;">
                        <button style="background: linear-gradient(90deg, #b76e79, #7c3c50);
                                       color: white;
                                       border: none;
                                       padding: 10px 20px;
                                       border-radius: 30px;
                                       font-family: 'Poppins', sans-serif;
                                       font-weight: 600;
                                       box-shadow: 0 4px 10px rgba(123, 60, 80, 0.3);
                                       cursor: pointer;">
                            <span style="margin-right: 5px;">📋</span> Save Your Routine
                        </button>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Footer
                st.markdown(
                    """
                    <div class="footer">
                        <p>© 2025 Glow Guide | Your Personal Skincare Assistant</p>
                        <p style="font-size: 0.75rem; margin-top: 5px;">
                            Results are personalized recommendations and not medical advice.
                            Consult with a dermatologist for specific skin concerns.
                        </p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        # Show app features when no results are displayed yet
        else:
            st.markdown(
                """
                
                """, 
                unsafe_allow_html=True
            )
            
            

# Call the function to render the page
if __name__ == "__main__":
    render_product_recommendations_page()
