import streamlit as st
from PIL import Image
import numpy as np
import time

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
    # Placeholder function for skin analysis
    # In a real application, you would replace this with actual AI model predictions
    # For demonstration, we'll use random results but with some consistency
    
    # Convert to NumPy array to simulate analysis
    np.random.seed(sum(np.array(image).flatten()[:100]))
    
    results = {
        "acne": np.random.randint(15, 85),
        "dryness": np.random.randint(15, 85),
        "oiliness": np.random.randint(15, 85),
        "sensitivity": np.random.randint(15, 85),
        "skin_type": np.random.choice(["Combination", "Oily", "Dry", "Normal", "Sensitive"])
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

    # Set the title of the page
    st.markdown('<h1>AI Skin Analysis</h1>', unsafe_allow_html=True)
    st.markdown(
        """
            <div style="text-align: left; margin-bottom: 25px; font-family: 'Poppins', sans-serif;">
                <p style="font-size: 1.2rem; color: #7c3c50; font-weight: 300;">
                    Discover your perfect skincare routine powered by AI ✨
                </p>
            </div>
        """,
        unsafe_allow_html=True
    )
        
    # Decorative element
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
    
    # Introduction card
    st.markdown("""
    <div class="css-card">
        <h3 style="margin-top: 0;">How it works</h3>
        <p>Upload a clear, well-lit selfie showing your skin without makeup. Our AI will analyze your skin condition and provide personalized recommendations for your skincare routine.</p>
        <p><strong>For best results:</strong> Use natural lighting, face the camera directly, and avoid filters or editing.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create columns for upload section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Image upload with custom styling
        uploaded_file = st.file_uploader("Upload a clear selfie", type=["jpg", "jpeg", "png"])
    
    with col2:
        st.markdown("""
        <div style="background-color: #f9f0f2; padding: 15px; border-radius: 10px; height: 90%; display: flex; align-items: center; justify-content: center;">
            <div style="text-align: center;">
                <span style="font-size: 3rem;">📸</span>
                <p style="margin-top: 10px;">Your image will appear here</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Process uploaded image
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Your uploaded image', use_column_width=True)
        
        # Create a button to trigger analysis
        if st.button("Analyze My Skin"):
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate analysis progress
            for i in range(101):
                status_text.text(f"Analysis in progress: {i}%")
                progress_bar.progress(i)
                time.sleep(0.01)  # Faster progress for better UX
            
            status_text.text("Analysis complete!")
            st.success("Your skin has been successfully analyzed!")
            
            # Analyze the skin
            results = analyze_skin(image)
            
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📊 Analysis Results", "💧 Product Recommendations", "📝 Skincare Routine"])
            
            with tab1:
                st.subheader("Your Skin Profile")
                st.markdown(f"<div style='background-color: #f9f0f2; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'><h3 style='margin-top: 0; color: #7c3c50;'>Detected Skin Type: {results['skin_type']}</h3></div>", unsafe_allow_html=True)
                
                # Display metrics in a grid
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Acne Level</div>
                        <div class="metric-value">{results['acne']}%</div>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                        <div>{get_level_description(results['acne'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-container" style="margin-top: 20px;">
                        <div class="metric-title">Dryness Level</div>
                        <div class="metric-value">{results['dryness']}%</div>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                        <div>{get_level_description(results['dryness'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-container">
                        <div class="metric-title">Oiliness Level</div>
                        <div class="metric-value">{results['oiliness']}%</div>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                        <div>{get_level_description(results['oiliness'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-container" style="margin-top: 20px;">
                        <div class="metric-title">Sensitivity Level</div>
                        <div class="metric-value">{results['sensitivity']}%</div>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                        <div>{get_level_description(results['sensitivity'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with tab2:
                st.subheader("Personalized Product Recommendations")
                
                # Get product recommendations
                products = get_product_recommendations(results)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div style="background-color: #fff; border-radius: 10px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 10px;">🧼</div>
                        <h3 style="margin-top: 0; font-size: 1.2rem !important;">Cleanser</h3>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.write(products["cleanser"])
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color: #fff; border-radius: 10px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 10px;">💧</div>
                        <h3 style="margin-top: 0; font-size: 1.2rem !important;">Treatment</h3>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.write(products["treatment"])
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div style="background-color: #fff; border-radius: 10px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); height: 100%; text-align: center;">
                        <div style="font-size: 2.5rem; margin-bottom: 10px;">🧴</div>
                        <h3 style="margin-top: 0; font-size: 1.2rem !important;">Moisturizer</h3>
                        <div class="decorative-line" style="margin: 10px 0;"></div>
                    """, unsafe_allow_html=True)
                    
                    st.write(products["moisturizer"])
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class="css-card" style="background-color: #f9f0f2;">
                    <h3 style="margin-top: 0;">Key Ingredients to Look For</h3>
                    <ul>
                """, unsafe_allow_html=True)
                
                if results['acne'] > 50:
                    st.markdown("<li><strong>Salicylic Acid:</strong> Helps clear pores and reduce inflammation</li>", unsafe_allow_html=True)
                    st.markdown("<li><strong>Benzoyl Peroxide:</strong> Fights acne-causing bacteria</li>", unsafe_allow_html=True)
                
                if results['dryness'] > 50:
                    st.markdown("<li><strong>Hyaluronic Acid:</strong> Attracts and retains moisture</li>", unsafe_allow_html=True)
                    st.markdown("<li><strong>Ceramides:</strong> Strengthen skin barrier and prevent moisture loss</li>", unsafe_allow_html=True)
                
                if results['oiliness'] > 50:
                    st.markdown("<li><strong>Niacinamide:</strong> Regulates sebum production</li>", unsafe_allow_html=True)
                    st.markdown("<li><strong>Clay:</strong> Absorbs excess oil</li>", unsafe_allow_html=True)
                
                if results['sensitivity'] > 50:
                    st.markdown("<li><strong>Centella Asiatica:</strong> Soothes and calms irritation</li>", unsafe_allow_html=True)
                    st.markdown("<li><strong>Allantoin:</strong> Relieves skin discomfort</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with tab3:
                st.subheader("Your Customized Skincare Routine")
                
                # Morning routine
                st.markdown("""
                <div class="css-card">
                    <h3 style="margin-top: 0;">☀️ Morning Routine</h3>
                    <ol>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<li><strong>Cleanse:</strong> {products['cleanser']}</li>", unsafe_allow_html=True)
                
                if results['acne'] > 60 or results['oiliness'] > 60:
                    st.markdown(f"<li><strong>Treatment:</strong> {products['treatment']}</li>", unsafe_allow_html=True)
                
                st.markdown(f"<li><strong>Moisturize:</strong> {products['moisturizer']}</li>", unsafe_allow_html=True)
                st.markdown("<li><strong>Protect:</strong> Broad-spectrum SPF 30+ sunscreen</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
                # Evening routine
                st.markdown("""
                <div class="css-card">
                    <h3 style="margin-top: 0;">🌙 Evening Routine</h3>
                    <ol>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<li><strong>Cleanse:</strong> {products['cleanser']}</li>", unsafe_allow_html=True)
                
                # Add double cleanse for oily skin
                if results['oiliness'] > 60:
                    st.markdown("<li><strong>Double Cleanse:</strong> Start with an oil cleanser before your regular cleanser</li>", unsafe_allow_html=True)
                
                st.markdown(f"<li><strong>Treatment:</strong> {products['treatment']}</li>", unsafe_allow_html=True)
                
                # Add extra hydration for dry skin
                if results['dryness'] > 60:
                    st.markdown("<li><strong>Extra Hydration:</strong> Layer a hydrating toner or essence</li>", unsafe_allow_html=True)
                
                st.markdown(f"<li><strong>Moisturize:</strong> {products['moisturizer']}</li>", unsafe_allow_html=True)
                
                # Add occlusive for very dry skin
                if results['dryness'] > 70:
                    st.markdown("<li><strong>Seal:</strong> Apply a thin layer of occlusive balm to lock in moisture</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
                # Weekly treatments
                st.markdown("""
                <div class="css-card">
                    <h3 style="margin-top: 0;">📅 Weekly Treatments</h3>
                    <ul>
                """, unsafe_allow_html=True)
                
                if results['acne'] > 50:
                    st.markdown("<li><strong>1-2x Weekly:</strong> Clay mask to deep clean pores</li>", unsafe_allow_html=True)
                
                if results['dryness'] > 50:
                    st.markdown("<li><strong>2-3x Weekly:</strong> Hydrating sheet mask</li>", unsafe_allow_html=True)
                
                if results['oiliness'] > 50:
                    st.markdown("<li><strong>1x Weekly:</strong> Chemical exfoliation with BHA</li>", unsafe_allow_html=True)
                
                if results['sensitivity'] > 50:
                    st.markdown("<li><strong>2x Weekly:</strong> Soothing mask with oat or aloe</li>", unsafe_allow_html=True)
                else:
                    st.markdown("<li><strong>1x Weekly:</strong> Gentle exfoliation (AHA for dry skin, BHA for oily skin)</li>", unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Call to action
                st.markdown("""
                <div style="background-color: #f9f0f2; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;">
                    <h3 style="margin-top: 0;">Want a Professional Consultation?</h3>
                    <p>Book a virtual appointment with one of our skincare specialists for a more in-depth analysis and personalized recommendations.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Book appointment button
                if st.button("Book a Consultation"):
                    st.success("Thank you for your interest! Our team will contact you to schedule your consultation.")

def get_level_description(value):
    if value < 30:
        return "Low"
    elif value < 70:
        return "Moderate"
    else:
        return "High"

# Call the function to render the page
if __name__ == "__main__":
    render_ai_skin_analysis_page()
