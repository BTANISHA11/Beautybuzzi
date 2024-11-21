import streamlit as st

def render_healthy_diet_page():
    # Set the title of the page
    st.title("Healthy Diet Tips")

    # Add some introductory text
    st.write("Eating a balanced diet is essential for maintaining good health and well-being. Here are some tips to help you achieve a healthy diet:")

    # List of healthy diet tips
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

    # Display the tips
    for tip in diet_tips:
        st.write(tip)

    # Optional: Add a section for recipes or meal ideas
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

    # Optional: Add links to resources for further reading
    st.write("For more information on healthy eating, consider visiting:")
    st.markdown("- [ChooseMyPlate.gov](https://www.choosemyplate.gov/)")
    st.markdown("- [Nutrition.gov](https://www.nutrition.gov/)")

# Call the function to render the page
if __name__ == "__main__":
    render_healthy_diet_page()