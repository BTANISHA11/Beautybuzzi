import streamlit as st

def render_skincare_tips():
    st.title("Skincare Tips")
    st.write("Here are some expert tips to maintain glowing, healthy skin:")
    
    tips = [
        "1. **Keep Your Skin Clean:** Regularly cleanse your face to remove dirt, oil, and makeup.",
        "2. **Moisturize Daily:** Use a good moisturizer to keep your skin hydrated.",
        "3. **Use Sunscreen:** Protect your skin from harmful UV rays by applying sunscreen every day.",
        "4. **Stay Hydrated:** Drink plenty of water to keep your skin hydrated from the inside.",
        "5. **Eat a Balanced Diet:** Incorporate fruits, vegetables, and healthy fats into your diet for better skin health.",
        "6. **Get Enough Sleep:** Aim for 7-9 hours of quality sleep to allow your skin to repair itself.",
        "7. **Avoid Smoking:** Smoking can accelerate skin aging and cause wrinkles.",
        "8. **Manage Stress:** Practice relaxation techniques to reduce stress, which can affect your skin."
    ]
    
    for tip in tips:
        st.write(tip)

    st.write("For more detailed information, consider consulting a skincare professional or dermatologist.")

def render_skincare_routine():
    st.title("Skincare Routine")
    st.write("A consistent skincare routine is key to maintaining healthy and radiant skin. Here are the essential steps to follow:")
    
    routine_steps = [
        "1. **Cleansing:** Start with a gentle cleanser to remove dirt, oil, and makeup. Cleanse your face twice a day, morning and evening.",
        "2. **Toning:** Apply a toner to help balance your skin's pH levels and prepare it for the next steps.",
        "3. **Serum:** Use a serum that targets your specific skin concerns, such as hydration, brightening, or anti-aging.",
        "4. **Moisturizing:** Apply a moisturizer to keep your skin hydrated and lock in moisture. Choose a product suitable for your skin type.",
        "5. **Sunscreen:** In the morning, finish your routine with a broad-spectrum sunscreen to protect your skin from harmful UV rays.",
        "6. **Exfoliation:** Exfoliate your skin 1-2 times a week to remove dead skin cells and promote cell turnover. Use a chemical or physical exfoliant based on your preference.",
        "7. **Face Masks:** Treat your skin with face masks 1-2 times a week for additional nourishment and hydration."
    ]

    for step in routine_steps:
        st.write(step)

    st.write("### Recommended Products")
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

    st.write("### Tips for Customizing Your Skincare Routine")
    st.write("1. **Know Your Skin Type:** Identify whether your skin is oily, dry, combination, or sensitive to choose appropriate products.")
    st.write("2. **Patch Test New Products:** Always patch test new products to avoid adverse reactions.")
    st.write("3. **Be Consistent:** Stick to your routine for at least a few weeks to see results.")
    st.write("4. **Adjust Seasonally:** Modify your routine based on seasonal changes, such as using heavier moisturizers in winter.")

def render_healthy_diet_tips():
    st.title("Healthy Diet Tips")
    st.write("Eating a balanced diet is essential for maintaining good health and well-being. Here are some tips to help you achieve a healthy diet:")
    
    diet_tips = [
        "1. **Eat a Variety of Foods:** Include different fruits, vegetables, whole grains, proteins, and healthy fats in your diet.",
        "2. **Focus on Whole Foods:** Choose whole, minimally processed foods over highly processed options.",
        "3. **Control Portion Sizes:** Be mindful of portion sizes to avoid overeating.",
        "4. **Stay Hydrated:** Drink plenty of water throughout the day to stay hydrated. Limit sugary drinks.",
        "5. **Limit Added Sugars and Salt:** Reduce your intake of added sugars and salt by choosing fresh foods and reading labels.",
        "6. **Include Healthy Fats:** Incorporate sources of healthy fats like avocados, nuts, seeds, and olive oil.",
        "7. **Plan Your Meals:** Plan your meals in advance to ensure you have healthy options available.",
        "8. **Listen to Your Body:** Pay attention to your hunger and fullness cues, and eat when you're hungry."
    ]

    for tip in diet_tips:
        st.write(tip)

    st.write("### Healthy Meal Ideas")
    meal_ideas = [
        "- **Breakfast:** Oatmeal topped with fresh fruits and nuts.",
        "- **Lunch:** Quinoa salad with mixed vegetables and a lemon vinaigrette.",
        "- **Dinner:** Grilled salmon with steamed broccoli and sweet potatoes.",
        "- **Snacks:** Hummus with carrot and cucumber sticks."
    ]

    st.write("Here are some healthy meal ideas to get you started:")
    for meal in meal_ideas:
        st.write(meal)

    st.write("For more information on healthy eating, consider visiting:")
    st.markdown("- [ChooseMyPlate.gov](https://www.choosemyplate.gov/)")
    st.markdown("- [Nutrition.gov](https://www.nutrition.gov/)")

def main():
    st.sidebar.title("Navigation")
    options = ["Skincare Tips", "Skincare Routine", "Healthy Diet Tips"]
    choice = st.sidebar.selectbox("Select a section", options)

    if choice == "Skincare Tips":
        render_skincare_tips()
    elif choice == "Skincare Routine":
        render_skincare_routine()
    elif choice == "Healthy Diet Tips":
        render_healthy_diet_tips()

if __name__ == "__main__":
    main()