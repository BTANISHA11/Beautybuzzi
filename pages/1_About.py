import streamlit as st
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Beauty Buzz - Skin-Smart Makeup AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a luxury beauty app experience
st.markdown("""
<style>
    /* Global Styles & Color Scheme */
    :root {
        --primary-color: #FF6B9B;
        --primary-light: #FFD2E6;
        --primary-dark: #D94073;
        --accent-color: #A771FF;
        --accent-light: #E5D4FF;
        --neutral-dark: #2A2A3A;
        --neutral-light: #F8F6FF;
        --text-light: #FFFFFF;
        --text-dark: #2A2A3A;
        --gradient-bg: linear-gradient(135deg, #FF6B9B 0%, #A771FF 100%);
    }
    
    /* Base Styles */
    body {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-dark);
        background-color: var(--neutral-light);
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
    
    h2, h3, h4, h5, h6 {
        font-family: 'Italiana', serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #b76e79, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    
    /* Container styles */
    .main > div {
        padding: 0 !important;
    }
    
    .main {
        background-color: var(--neutral-light);
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        color: white;
    }
    
    .sidebar .sidebar-content .block-container {
        padding-top: 2rem;
    }
    
    /* App header/title */
    .app-header {
        background-color: white;
        padding: 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo {
        font-family: 'Italiana', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-dark);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 0;
    }
    
    /* Custom styling for sidebar navigation */
    section[data-testid="stSidebar"] {
        border-radius: 0 20px 20px 0;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 3rem;
        background: transparent;
    }
    
    /* Style for nav items in sidebar */
    .nav-item {
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        cursor: pointer;
        color: white;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    .nav-item.active {
        background-color: white;
        color: var(--primary-color);
        font-weight: 600;
    }
    
    /* Hero Section */
    .hero-section {
        border-radius: 30px;
        padding: 4rem 3rem;
        margin: 0 3rem 3rem 3rem;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        color: white;
    }
    
    .hero-content {
        width: 55%;
        position: relative;
        z-index: 2;
    }
    
    .hero-image {
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        width: 50%;
        z-index: 1;
        background-size: cover;
        background-position: center;
        border-radius: 0 30px 30px 0;
    }
    
    .hero-overlay {
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        width: 50%;
        z-index: 1;
        mix-blend-mode: multiply;
    }
    
    .tagline {
        font-size: 3.5rem;
        line-height: 1.2;
        margin-bottom: 1.5rem;
    }
    
    .highlight {
        color: var(--accent-light);
        position: relative;
        z-index: 1;
    }
    
    .highlight:after {
        content: '';
        position: absolute;
        bottom: 5px;
        left: 0;
        width: 100%;
        height: 8px;
        background-color: rgba(167, 113, 255, 0.4);
        z-index: -1;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        line-height: 1.6;
        margin-bottom: 2rem;
        opacity: 0.9;
        max-width: 600px;
    }
    
    /* Features Section */
    .section-title {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
        color: var(--neutral-dark);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin: 0 0rem;
    }
    
    .feature-card {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        display: inline-block;
        position: relative;
        z-index: 1;
    }
    
    .feature-icon:before {
        content: '';
        position: absolute;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: var(--primary-light);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: -1;
    }
    
    .feature-card h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: var(--neutral-dark);
    }
    
    .feature-card p {
        color: #666;
        line-height: 1.6;
    }
    
    /* Occasions Section */
    .occasions-section {
        padding: 4rem 3rem;
        text-align: center;
        background-color: white;
        border-radius: 30px;
        margin: 0rem;
        margin-top: 3rem;
    }
    
    .occasions-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .occasion-card {
        padding: 2rem;
        border-radius: 20px;
        background-color: var(--neutral-light);
        transition: all 0.3s ease;
    }
    
    .occasion-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    }
    
    .occasion-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .occasion-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--neutral-dark);
    }
    
    .occasion-text {
        color: #666;
    }
    
    /* Testimonial Section */
    .testimonial-section {
        margin: 0rem;
        margin-top: 3rem;
        text-align: center;
    }
    
    .testimonial-card {
        background: white;
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        position: relative;
    }
    
    .testimonial-quote {
        font-size: 1.4rem;
        line-height: 1.6;
        color: var(--neutral-dark);
        margin-bottom: 1.5rem;
        font-style: italic;
    }
    
    .testimonial-quote:before {
        content: '"';
        font-size: 4rem;
        color: var(--primary-light);
        position: absolute;
        top: 1.5rem;
        left: 2rem;
        font-family: Georgia, serif;
    }
    
    .testimonial-author {
        font-weight: 600;
        color: var(--primary-dark);
    }
    
    .testimonial-detail {
        color: #666;
    }
    
    /* CTA Section */
    .cta-section {
        text-align: center;
        margin: 5rem 3rem 3rem 3rem;
    }
    
    .cta-title {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: var(--neutral-dark);
    }
    
    .cta-button {
        display: inline-block;
        background: var(--gradient-bg);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        margin: 1.5rem 0;
        cursor: pointer;
        box-shadow: 0 8px 20px rgba(255, 107, 155, 0.3);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(255, 107, 155, 0.4);
    }
    
    .cta-text {
        color: #666;
        margin-top: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #7c3c50;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    
    .copyright {
        margin-top: 3rem;
        text-align: center;
        opacity: 0.7;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to encode images for background
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background_from_url(url):
    return f"""
    <style>
    .hero-image {{
        background-image: url("{url}");
    }}
    </style>
    """

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0.5rem; text-align: center;">
        <h1 class="logo" style="color: white; justify-content: center;">💄 Beauty Buzz</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some space
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation items with icons
    st.markdown("""
    <div class="nav-item active">
        <span>ℹ️</span> About
    </div>
    <div class="nav-item">
        <span>🔍</span> Skin Analysis
    </div>
    <div class="nav-item">
        <span>💄</span> Virtual Try-On
    </div>
    <div class="nav-item">
        <span>🛍️</span> Product Finder
    </div>
    <div class="nav-item">
        <span>👥</span> Community
    </div>
    <div class="nav-item">
        <span>⚙️</span> Settings
    </div>
    """, unsafe_allow_html=True)
    
    # Add space before the sign-in button
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Sign-in button styled to match the theme
    st.markdown("""
    <div style="padding: 0 1rem;">
        <button class="cta-button" style="width: 100%; padding: 0.75rem; font-size: 1rem; background: white; color: var(--primary-color);">
            Sign In
        </button>
    </div>
    <div style="text-align: center; margin-top: 0.5rem; color: rgba(255,255,255,0.8); font-size: 0.8rem;">
        New user? <a href="#" style="color: white; text-decoration: underline;">Create account</a>
    </div>
    """, unsafe_allow_html=True)

# App header on main content area
st.markdown('<h1>About BeautyBuzz</h1>', unsafe_allow_html=True)
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
        
# Use a placeholder image URL for the hero section
hero_image_url = "/api/placeholder/600/800"
st.markdown(set_background_from_url(hero_image_url), unsafe_allow_html=True)

# Hero Section
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
        

# Features Section
st.markdown('<h2 class="section-title">Your Skin-Smart Beauty Assistant</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Advanced Skin Analysis</h3>
        <p>Our AI scans your selfie to detect skin concerns including acne, dryness, sensitivity, aging signs, and hyperpigmentation with dermatologist-level accuracy.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <h3>Smart Recommendations</h3>
        <p>Get personalized skincare and makeup suggestions based on your unique skin profile, concerns, and beauty goals for a routine that truly works.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💄</div>
        <h3>Virtual Try-On Studio</h3>
        <p>See how products actually look on your face using our high-fidelity AR technology before purchasing, saving time and money on products that don't match.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Special Occasions Section
st.markdown("""
<div class="occasions-section">
    <h2 class="section-title">Instant Glam for Every Occasion</h2>
    <div class="occasions-grid">
        <div class="occasion-card">
            <div class="occasion-icon">👰</div>
            <h3 class="occasion-title">Weddings & Events</h3>
            <p class="occasion-text">Flawless, long-wear looks that photograph beautifully and last through celebrations.</p>
        </div>
        <div class="occasion-card">
            <div class="occasion-icon">🎓</div>
            <div class="occasion-title">Interviews & Presentations</div>
            <p class="occasion-text">Professional, confidence-boosting makeup that makes the right impression.</p>
        </div>
        <div class="occasion-card">
            <div class="occasion-icon">✨</div>
            <div class="occasion-title">Everyday Glow</div>
            <p class="occasion-text">Quick, effortless routines that enhance your natural beauty in minutes.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Testimonial Section
st.markdown("""
<div class="testimonial-section">
    <div class="testimonial-card">
        <p class="testimonial-quote">Beauty Buzz completely transformed my relationship with makeup. The AI actually understood my rosacea and recommended products that don't trigger flare-ups. For the first time, I can wear makeup without worrying about my skin!</p>
        <p class="testimonial-author">- Cynthia Williams</p>
        <p class="testimonial-detail">28, Sensitive Skin with Rosacea</p>
    </div>
</div>
""", unsafe_allow_html=True)

# CTA Section
st.markdown("""
<div class="cta-section">
    <h2 class="cta-title">Ready for Healthier Beauty?</h2>
    <p>Discover makeup and skincare that's actually good for your unique skin type.</p>
    <button class="cta-button">Start Free Analysis</button>
    <p class="cta-text">No credit card needed • 2-minute setup • AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 Glow Guide | Your Personal Skincare Assistant</p>
        <p style="font-size: 0.75rem; margin-top: 5px;">
            Results are personalized recommendations and not medical advice.
            Consult with a dermatologist for specific skin concerns.
        </p>
    </div>
""", unsafe_allow_html=True)
