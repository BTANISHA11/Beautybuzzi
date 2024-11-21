import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Beauty Buzz - About Us", page_icon="💄", layout="wide")

# Custom CSS
custom_css = """
<style>
body {
    background-color: #f8f9fa;
    font-family: "Arial", sans-serif;
}

.header {
    text-align: center;
    font-size: 3.5em;
    color: #d63384;
    margin-top: 30px;
}

.subheader {
    font-size: 1.8em;
    color: #6f42c1;
    margin-bottom: 30px;
    text-align: center;
}

.about-content {
    font-size: 1.2em;
    color: #495057;
    line-height: 1.8em;
    margin-bottom: 30px;
}

.mission-section, .team-section {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 30px;
}

.mission-title, .team-title {
    font-size: 2em;
    color: #495057;
    margin-bottom: 15px;
}

.team-members {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}

.team-member {
    text-align: center;
    margin: 10px;
}

.team-member img {
    border-radius: 50%;
    width: 120px;
    height: 120px;
    margin-bottom: 10px;
}

footer {
    text-align: center;
    font-size: 1.2em;
    color: #868e96;
    margin-top: 50px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='header'>💄 Welcome to Beauty Buzz</h1>", unsafe_allow_html=True)
st.write("")

# Subheader
st.markdown("<h3 class='subheader'>Empowering You to Explore the World of Beauty with AI-Powered Virtual Makeup Try-On</h3>", unsafe_allow_html=True)

# About Us Section
st.markdown("<p class='about-content'>Beauty Buzz is revolutionizing the beauty industry with cutting-edge technology, offering a seamless virtual makeup experience. Our platform allows users to experiment with various makeup styles and shades in real-time using their own face, providing the perfect makeup solution for every occasion. From virtual try-ons to personalized recommendations, Beauty Buzz is designed to empower individuals to express their unique beauty with confidence.</p>", unsafe_allow_html=True)

# Mission Section
st.markdown("<div class='mission-section'><h2 class='mission-title'>Our Mission</h2><p class='about-content'>At Beauty Buzz, our mission is to bridge the gap between technology and beauty. By leveraging artificial intelligence, computer vision, and machine learning, we aim to provide a more personalized and accessible beauty experience. Our goal is to help individuals discover the best makeup products and styles that align with their unique preferences and personalities, making beauty fun, easy, and inclusive.</p></div>", unsafe_allow_html=True)

# Team Section
st.markdown("<div class='team-section'><h2 class='team-title'>Meet the Team</h2><p class='about-content'>We are a diverse group of tech enthusiasts, beauty aficionados, and AI innovators, working together to bring Beauty Buzz to life. Our team is passionate about creating products that enhance the beauty experience and make it accessible to everyone. Here's a glimpse of the amazing people behind Beauty Buzz:</p></div>", unsafe_allow_html=True)



# Footer
st.markdown("<footer>Powered by Beauty Buzz AI 💄 | All Rights Reserved</footer>", unsafe_allow_html=True)
