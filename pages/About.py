import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Beauty Buzz - About Us", page_icon="💄", layout="wide")

# Custom CSS
custom_css = """
<style>
/* General Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f9f9f9;
    padding: 20px;
}

/* About Section */
.about-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
    gap: 20px;
}

.left-content, .right-content {
    flex: 1; /* Equal width for both sides */
}

.left-content {
    padding: 20px;
}

.left-content h1 {
    font-size: 2.9rem;
    color: #000;
    line-height: 1.2;
}

.right-content {
    padding: 20px;
}

.signature {
    font-family: 'Brush Script MT', cursive;
    font-size: 1.9rem;
    margin-top: 20px;
    color: #000;
}

.right-content img {
    width: 100%; /* Full width to maintain responsiveness */
    height: auto;
    border-radius: 10px;
}

/* Text Content */
.text-content {
    max-width: 800px;
    margin: 0 auto 40px;
    text-align: center; /* Center text */
}

.text-content blockquote {
    font-size: 1.6rem;
    font-style: italic;
    margin: 20px 0;
    border-left: 4px solid #aaa;
    padding-left: 15px;
    color: #555;
}

.text-content .testimonial {
    text-align: right;
    font-size: 0.9rem;
    color: #777;
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

image = Image.open("./pages/images/image2.png")

# Render the image in Streamlit
st.image(image, caption="Try on MAKEUP")

# Text Content Section
st.markdown("<div class='text-content'>"
            "<p>"
            "Beauty Buzz is revolutionizing the beauty industry with cutting-edge technology, offering a seamless virtual makeup experience. "
            "Our platform allows users to experiment with various makeup styles and shades in real-time using their own face, providing the perfect makeup solution for every occasion. "
            "From virtual try-ons to personalized recommendations, Beauty Buzz is designed to empower individuals to express their unique beauty with confidence."
            "</p>"
            "<p>"
            "At Beauty Buzz, our mission is to bridge the gap between technology and beauty. By leveraging artificial intelligence, computer vision, and machine learning, "
            "we aim to provide a more personalized and accessible beauty experience. Our goal is to help individuals discover the best makeup products and styles that align with their unique "
            "preferences and personalities, making beauty fun, easy, and inclusive."
            "</p>"
            "<blockquote>"
            "“ We are a diverse group of tech enthusiasts, beauty aficionados, and AI innovators, working together to bring Beauty Buzz to life. "
            "Our team is passionate about creating products that enhance the beauty experience and make it accessible to everyone. Here's a glimpse of the amazing people behind Beauty Buzz: ”"
            "</blockquote>"
            "<p class='testimonial'>"
            "TESTIMONIAL BY<br><strong>Cynthia Summer</strong>"
            "</p>"
            "</div>", unsafe_allow_html=True)

# Footer
st.markdown("<footer>Powered by Beauty Buzz AI 💄 | All Rights Reserved</footer>", unsafe_allow_html=True)
