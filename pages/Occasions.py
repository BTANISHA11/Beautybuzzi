import streamlit as st
import os
from PIL import Image
import requests

# Set page config
st.set_page_config(page_title="Beauty Buzz - Occasions", page_icon="💄", layout="wide")

# Embed custom CSS
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
}

.occasion-title {
    font-size: 1.5em;
    color: #495057;
    margin-bottom: 10px;
}

footer {
    text-align: center;
    font-size: 1em;
    color: #adb5bd;
    margin-top: 50px;
    border-top: 1px solid #dee2e6;
    padding-top: 10px;
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
st.markdown("<h1 class='header'>💄 Beauty Buzz: Makeup for Every Occasion 💄</h1>", unsafe_allow_html=True)
st.write("")

# Occasion Options
st.markdown("<h3 class='subheader'>Choose your Occasion</h3>", unsafe_allow_html=True)
occasion = st.selectbox(
    "Select an Occasion",
    ["Office Day", "Cocktail Party", "Wedding", "Birthday Party", "Night Out", "Casual Day"]
)

# Display Occasion Image and Details
image_mapping = {
    "Office Day": "office_day.jpg",
    "Cocktail Party": "cocktail_party.jpg",
    "Wedding": "wedding.jpg",
    "Birthday Party": "birthday_party.jpg",
    "Night Out": "night_out.jpg",
    "Casual Day": "casual_day.jpg",
}

if occasion:
    col1, col2 = st.columns([1, 2])

    with col1:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder = os.path.join(script_dir, "images")
        
        # Display occasion image
        image = Image.open(os.path.join(image_folder, image_mapping[occasion]))
        st.image(image, caption=f"{occasion} Look")

    with col2:
        st.markdown(f"<h4 class='occasion-title'>{occasion} Makeup Suggestions:</h4>", unsafe_allow_html=True)
        if occasion == "Office Day":
            st.write("Light and subtle makeup suitable for professional settings:")
            st.write("- **Foundation**: Matte, lightweight\n"
                     "- **Lipstick**: Nude shades\n"
                     "- **Eyeliner**: Minimalistic\n"
                     "- **Blush**: Soft pink or peach")
        elif occasion == "Cocktail Party":
            st.write("Glamorous makeup with bold choices:")
            st.write("- **Foundation**: High-coverage\n"
                     "- **Lipstick**: Bold red or berry tones\n"
                     "- **Eyeliner**: Winged or cat-eye\n"
                     "- **Blush**: Rosy tones")
        elif occasion == "Wedding":
            st.write("Traditional and vibrant look for celebrations:")
            st.write("- **Foundation**: Dewy finish\n"
                     "- **Lipstick**: Deep red or maroon\n"
                     "- **Eyeliner**: Heavy, bridal\n"
                     "- **Blush**: Rich rose")
        elif occasion == "Birthday Party":
            st.write("Fun and vibrant colors for a joyful vibe:")
            st.write("- **Foundation**: Luminous\n"
                     "- **Lipstick**: Coral or pink\n"
                     "- **Eyeliner**: Glitter or metallic\n"
                     "- **Blush**: Bright pink")
        elif occasion == "Night Out":
            st.write("Bold and dramatic look for the night:")
            st.write("- **Foundation**: High-definition\n"
                     "- **Lipstick**: Dark plum or wine shades\n"
                     "- **Eyeliner**: Smokey eyes\n"
                     "- **Blush**: Darker peach")
        elif occasion == "Casual Day":
            st.write("Natural, no-makeup look for a relaxed day:")
            st.write("- **Foundation**: Tinted moisturizer\n"
                     "- **Lipstick**: Lip balm or nude gloss\n"
                     "- **Eyeliner**: None or light pencil\n"
                     "- **Blush**: Subtle pink")

# Drag-and-Drop for Makeup Application
st.markdown("<h3 class='subheader'>Upload Your Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    # Send image to backend for makeup application
    st.markdown("<h4 class='occasion-title'>Applied Makeup Preview:</h4>", unsafe_allow_html=True)
    
    # Simulate backend processing (Replace with actual API call)
    url = "http://backend-api-url/apply-makeup"  # Replace with your backend API endpoint
    files = {"file": uploaded_file}
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        processed_image = Image.open(response.content)
        st.image(processed_image, caption="Makeup Applied")
    else:
        st.error("Failed to apply makeup. Please try again.")

# Footer
st.markdown("<div class='footer'>Powered by Beauty Buzz AI 💄</div>", unsafe_allow_html=True)
