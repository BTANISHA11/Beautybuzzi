import streamlit as st

def render_skincare_routine_page():
    # Set the title of the page
    st.title("Skincare Routine")

    # Add some introductory text
    st.write("A consistent skincare routine is key to maintaining healthy and radiant skin. Here are the essential steps to follow:")

    # List of skincare routine steps
    routine_steps = [
        "1. **Cleansing:** Start with a gentle cleanser to remove dirt, oil, and makeup. Cleanse your face twice a day, morning and evening.",
        "2. **Toning:** Apply a toner to help balance your skin's pH levels and prepare it for the next steps.",
        "3. **Serum:** Use a serum that targets your specific skin concerns, such as hydration, brightening, or anti-aging.",
        "4. **Moisturizing:** Apply a moisturizer to keep your skin hydrated and lock in moisture. Choose a product suitable for your skin type.",
        "5. **Sunscreen:** In the morning, finish your routine with a broad-spectrum sunscreen to protect your skin from harmful UV rays.",
        "6. **Exfoliation:** Exfoliate your skin 1-2 times a week to remove dead skin cells and promote cell turnover. Use a chemical or physical exfoliant based on your preference.",
        "7. **Face Masks:** Treat your skin with face masks 1-2 times a week for additional nourishment and hydration."
    ]

    # Display the steps
    for step in routine_steps:
        st.write(step)

    # Optional: Add a section for product recommendations
    st.write("### Recommended Products")
    st.write("Here are some product types you might consider for each step of your routine:")
    product_recommendations = {
        "Cleansers": "Gel or cream-based cleansers that suit your skin type.",
        "Toners": "Alcohol-free toners with hydrating ingredients.",
        "Serums": "Vitamin C serums for brightening or hyaluronic acid serums for hydration.",
        "Moisturizers": "Lightweight gels for oily skin or rich creams for dry skin.",
        "Sunscreens": "Broad-spectrum SPF 30 or higher, suitable for daily use.",
        "Exfoliants": "Gentle chemical exfoliants like AHA or BHA.",
        "Face Masks": "Hydrating sheet masks or clay masks for deep cleansing."
    }

    for product_type, recommendation in product_recommendations.items():
        st.write(f"- **{product_type}:** {recommendation}")

    # Optional: Add tips for customizing your routine
    st.write("### Tips for Customizing Your Skincare Routine")
    st.write("1. **Know Your Skin Type:** Identify whether your skin is oily, dry, combination, or sensitive to choose appropriate products.")
    st.write("2. **Patch Test New Products:** Always patch test new products to avoid adverse reactions.")
    st.write("3. **Be Consistent:** Stick to your routine for at least a few weeks to see results.")
    st.write("4. **Adjust Seasonally:** Modify your routine based on seasonal changes, such as using heavier moisturizers in winter.")

# Call the function to render the page
if __name__ == "__main__":
    render_skincare_routine_page()