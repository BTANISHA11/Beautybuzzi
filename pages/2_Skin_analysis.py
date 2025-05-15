import streamlit as st
from PIL import Image
import numpy as np

def analyze_skin(image):
    # Placeholder function for skin analysis
    # In a real application, you would replace this with actual AI model predictions
    # For demonstration, we'll use random results
    results = {
        "acne": np.random.randint(0, 100),
        "dryness": np.random.randint(0, 100),
        "oiliness": np.random.randint(0, 100),
        "sensitivity": np.random.randint(0, 100)
    }
    return results

def render_ai_skin_analysis_page():
    # Set the title of the page
    st.title("AI Skin Analysis")

    # Add introductory text
    st.write("Upload an image of your skin for analysis. Our AI will provide insights into your skin condition.")

    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Analyze the skin
        st.write("Analyzing your skin...")
        results = analyze_skin(image)

        # Display the results
        st.write("### Analysis Results")
        st.write(f"- **Acne Level:** {results['acne']}%")
        st.write(f"- **Dryness Level:** {results['dryness']}%")
        st.write(f"- **Oiliness Level:** {results['oiliness']}%")
        st.write(f"- **Sensitivity Level:** {results['sensitivity']}%")

        # Provide skincare recommendations based on analysis
        st.write("### Recommendations")
        if results['acne'] > 50:
            st.write("Consider using products with salicylic acid or benzoyl peroxide.")
        if results['dryness'] > 50:
            st.write("Incorporate a hydrating serum and a rich moisturizer into your routine.")
        if results['oiliness'] > 50:
            st.write("Look for oil-free and non-comedogenic products.")
        if results['sensitivity'] > 50:
            st.write("Use gentle, fragrance-free products to avoid irritation.")

# Call the function to render the page
if __name__ == "__main__":
    render_ai_skin_analysis_page()
