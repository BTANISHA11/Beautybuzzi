import streamlit as st
from PIL import Image
import numpy as np

def analyze_face(image):
    # Placeholder function for face analysis
    # In a real application, you would replace this with actual AI model predictions
    # For demonstration, we'll use random results
    results = {
        "face_shape": np.random.choice(["Oval", "Round", "Square", "Heart"]),
        "hair_type": np.random.choice(["Straight", "Wavy", "Curly"]),
        "preferences": np.random.choice(["Short", "Medium", "Long"])
    }
    return results

def get_hairstyle_recommendations(face_shape, hair_type, preferences):
    recommendations = []

    # General recommendations based on face shape
    if face_shape == "Oval":
        recommendations.append("Most hairstyles suit an oval face. Consider long layers or a bob.")
    elif face_shape == "Round":
        recommendations.append("Longer hairstyles can elongate your face. Try long layers or a side part.")
    elif face_shape == "Square":
        recommendations.append("Soft, layered hairstyles can soften the jawline. Consider waves or curls.")
    elif face_shape == "Heart":
        recommendations.append("Chin-length bobs or side-swept bangs can balance a heart-shaped face.")

    # Recommendations based on hair type
    if hair_type == "Straight":
        recommendations.append("Consider sleek bobs or long, straight styles.")
    elif hair_type == "Wavy":
        recommendations.append("Loose waves or layered cuts can enhance your natural texture.")
    elif hair_type == "Curly":
        recommendations.append("Layered cuts can help manage volume and shape your curls.")

    # Preferences
    if preferences == "Short":
        recommendations.append("Try a chic pixie cut or a textured bob.")
    elif preferences == "Medium":
        recommendations.append("Consider a shoulder-length cut with layers.")
    elif preferences == "Long":
        recommendations.append("Long layers or a classic straight look can be stunning.")

    return recommendations

def render_hairstyle_recommendation_page():
    # Set the title of the page
    st.title("AI Hairstyle Recommendation")

    # Add introductory text
    st.write("Upload an image of your face for hairstyle recommendations. Our AI will provide insights into suitable hairstyles.")

    # Image upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption='Uploaded Image', use_column_width=True)

        with col2:
            # Analyze the face
            st.write("Analyzing your face...")
            results = analyze_face(image)

            # Display the results
            st.write("### Analysis Results")
            st.write(f"- **Face Shape:** {results['face_shape']}")
            st.write(f"- **Hair Type:** {results['hair_type']}")
            st.write(f"- **Preferences:** {results['preferences']}")

            # Provide hairstyle recommendations based on analysis
            st.write("### Hairstyle Recommendations")
            recommendations = get_hairstyle_recommendations(results['face_shape'], results['hair_type'], results['preferences'])
            for recommendation in recommendations:
                st.write(f"- {recommendation}")

# Call the function to render the page
if __name__ == "__main__":
    render_hairstyle_recommendation_page()
