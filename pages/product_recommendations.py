import streamlit as st

def render_product_recommendations_page():
    # Set the title of the page
    st.title("Product Recommendations")

    # Add introductory text with an emoji
st.write("Find the best skincare products tailored to your skin type and concerns. 💆‍♀️💫")

# Skin type selection
skin_type = st.selectbox(
    "Select Your Skin Type",
    ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
)

# Skin concerns selection
skin_concerns = st.multiselect(
    "Select Your Skin Concerns",
    ["Acne", "Wrinkles", "Dark Spots", "Dryness", "Sensitivity", "Oiliness", "Uneven Skin Tone"]
)

# Recommendations based on skin type and concerns
recommendations = {
    "Oily": {
        "products": [
            "Oil-free Cleanser 🧼",
            "Salicylic Acid Serum 💧",
            "Lightweight Gel Moisturizer 🌿",
            "Clay Mask 🧖‍♀️",
            "Non-comedogenic Sunscreen ☀️"
        ]
    },
    "Dry": {
        "products": [
            "Hydrating Cleanser 🧼",
            "Hyaluronic Acid Serum 💧",
            "Rich Cream Moisturizer 🥥",
            "Nourishing Face Oil 🌸",
            "Hydrating Sunscreen ☀️"
        ]
    },
    "Combination": {
        "products": [
            "Gentle Cleanser 🧼",
            "Balancing Toner 💦",
            "Lightweight Moisturizer for T-zone and Cream for Dry Areas 🌿",
            "Exfoliating Serum 🌟",
            "Broad-Spectrum Sunscreen ☀️"
        ]
    },
    "Sensitive": {
        "products": [
            "Fragrance-free Cleanser 🧼",
            "Soothing Serum with Aloe Vera 🍃",
            "Hypoallergenic Moisturizer 💖",
            "Gentle Exfoliant 🌼",
            "Mineral Sunscreen ☀️"
        ]
    },
    "Normal": {
        "products": [
            "Gentle Cleanser 🧼",
            "Hydrating Toner 💦",
            "Lightweight Moisturizer 🌿",
            "Occasional Exfoliant 🌟",
            "Broad-Spectrum Sunscreen ☀️"
        ]
    }
}

# Display recommendations based on user input
if st.button("Get Recommendations 🚀"):
    st.write("### Recommended Products:")
    st.write(f"**Skin Type:** {skin_type}")
    st.write("**Products:**")
    for product in recommendations[skin_type]["products"]:
        st.write(f"- {product}")
    
    # Additional recommendations based on concerns
    if skin_concerns:
        st.write("### Additional Recommendations for Your Concerns:")
        for concern in skin_concerns:
            if concern == "Acne":
                st.write("- Consider products with salicylic acid or benzoyl peroxide. 🛡️")
            elif concern == "Wrinkles":
                st.write("- Look for retinol or peptides in your products. 🔬")
            elif concern == "Dark Spots":
                st.write("- Use Vitamin C serums or products with niacinamide. 🍊")
            elif concern == "Dryness":
                st.write("- Incorporate hydrating serums and rich moisturizers. 💧")
            elif concern == "Sensitivity":
                st.write("- Choose fragrance-free and hypoallergenic products. 💖")
            elif concern == "Oiliness":
                st.write("- Use oil-free and mattifying products. 🌿")
            elif concern == "Uneven Skin Tone":
                st.write("- Try exfoliating acids or brightening serums. ✨")

   

# Call the function to render the page
if __name__ == "__main__":
    render_product_recommendations_page()