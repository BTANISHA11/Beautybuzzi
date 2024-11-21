import os
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Beauty Buzz - Features", page_icon="✨", layout="wide")

# Custom CSS
custom_css = """
<style>
body {
    background-color: #f8f9fa;
    font-family: "Arial", sans-serif;
}

.header {
    text-align: center;
    font-size: 3em;
    color: #d63384;
    margin-top: 20px;
}

.subheader {
    font-size: 1.5em;
    color: #6f42c1;
    margin-bottom: 30px;
    text-align: center;
}

.feature-box {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
}

.feature-title {
    font-size: 1.5em;
    color: #495057;
    margin-bottom: 10px;
}

.feature-description {
    font-size: 1em;
    color: #6c757d;
    line-height: 1.5em;
}

.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 1.2em;
    color: #868e96;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='header'>✨ Beauty Buzz: App Features ✨</h1>", unsafe_allow_html=True)
st.write("")

# Subheader
st.markdown("<h3 class='subheader'>Discover the cutting-edge features that make Beauty Buzz your ultimate virtual makeup companion!</h3>", unsafe_allow_html=True)

# Features List
features = [
    {
        "title": "Real-Time Makeup Try-On",
        "description": "Experiment with different makeup styles instantly using your live camera feed. Explore lipstick, blush, eyeliner, foundation, and hair colors applied virtually.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "Occasion-Specific Suggestions",
        "description": "Receive personalized makeup recommendations for office days, weddings, cocktail parties, and more. Choose the perfect look for every occasion.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "Advanced Makeup Filters",
        "description": "Filter products by price, brand, and occasion to find the ideal beauty products that suit your style and budget.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "AI-Powered Realism",
        "description": "Leverages CNNs and OpenCV to apply makeup styles with precision, ensuring natural-looking results while preserving your facial features.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "Multi-Brand Product Integration",
        "description": "Browse and select makeup products from top beauty brands, with links to purchase them directly from e-commerce platforms.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "Customizable Shades",
        "description": "Customize shades of lipstick, blush, and more to match your preferences and experiment with bold or subtle looks.",
        "image": "skincare.jpg.jpg"
    },
    {
        "title": "Virtual Camera Feature",
        "description": "Use the built-in camera feature to capture your look and compare styles before making a purchase decision.",
        "image": "skincare.jpg.jpg"
    }
]

# Display Features
for feature in features:
    st.markdown(f"<div class='feature-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])  # Adjust column widths
    with col1:
        if os.path.exists(feature["image"]):
            st.image(feature["image"], use_column_width=True, caption=feature["title"])
        else:
            st.image("https://via.placeholder.com/150", use_column_width=True, caption="Image not available")
    with col2:
        st.markdown(f"<h2 class='feature-title'>{feature['title']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='feature-description'>{feature['description']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Powered by Beauty Buzz AI 💄</div>", unsafe_allow_html=True)
