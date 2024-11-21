import streamlit as st
from PIL import Image
import numpy as np
from static.constants import DEFAULT_IMAGE_PATH, HAIR_COLOR_DEFAULT, MAIN_COLOR

# Function to include custom CSS
def add_custom_css(css_path="./static/styles.css"):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_home_page():
    # Load custom CSS for styling
    add_custom_css()

    # Title and Description
    st.markdown("## Transform your look with AI-powered makeup. with Beauty Buzz")
    st.markdown("""
        **Beauty Buzz** uses advanced AI technology to apply virtual makeup, giving you the power to experiment with different shades and looks in real time.
        Upload your image, choose your makeup parameters, and let the AI work its magic.
    """)

    # Layout with two columns (Image in the center, Parameters on the right)
    col1, col2 = st.columns([3, 1])

    # Column 1 - Center the image upload and display
    with col1:
        # Image uploader and display
        img_file_buffer = st.file_uploader("Upload your image", type=["png", "jpg", "jpeg"])

        if img_file_buffer is not None:
            image = np.array(Image.open(img_file_buffer))
            demo_img = img_file_buffer
        else:
            demo_img = DEFAULT_IMAGE_PATH
            image = np.array(Image.open(demo_img))

        st.subheader("Original Image")
        st.image(image, use_column_width=True)

    # Column 2 - Parameters and makeup options on the right
    with col2:
        st.header("Parameters")

        # Hair and lip color pickers
        hair_color = st.color_picker("Pick the Hair Color", HAIR_COLOR_DEFAULT)
        lip_color = st.color_picker("Pick the Lip Color", MAIN_COLOR)

        # Combine the selected colors (can be extended as needed)
        colors = [hair_color, lip_color, lip_color]

        # Button to apply makeup
        if st.button("Apply Makeup"):
            # Simulate applying makeup (you can replace this with your AI logic)
            st.success("Makeup applied successfully!")

    # Footer with copyright information
    st.markdown("<footer>© 2024 BeautyBuzz. All rights reserved.</footer>", unsafe_allow_html=True)

# Run the homepage rendering function
render_home_page()
