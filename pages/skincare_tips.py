import streamlit as st

def render_skincare_tips():
    # Set the title of the page
    st.title("Skincare Tips")
    
    # Add some introductory text
    st.write("Here are some expert tips to maintain glowing, healthy skin:")
    
    # List of skincare tips
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
    
    # Display the tips
    for tip in tips:
        st.write(tip)

    # Optionally, you could add images or links for further reading
    st.write("For more detailed information, consider consulting a skincare professional or dermatologist.")

# Call the function to render the page
if __name__ == "__main__":
    render_skincare_tips()