import streamlit as st

def render_consultations_page():
    # Set the title of the page
    st.title("Consultations with Skincare Experts")

    # Add introductory text
    st.write("Book a consultation with our certified skincare experts for personalized advice and treatment plans tailored to your skin type and concerns.")

    # Provide information about the consultation process
    st.write("### How It Works")
    st.write(
        """
        1. **Fill Out the Consultation Form:** Provide us with your details and any specific skincare concerns you may have.
        2. **Schedule a Session:** Choose a date and time that works for you.
        3. **Meet with an Expert:** Join a video call or in-person consultation to discuss your skincare needs and get personalized recommendations.
        """
    )

    # Consultation form
    st.write("### Consultation Request Form")
    
    with st.form(key='consultation_form'):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        phone = st.text_input("Your Phone Number")
        skin_concerns = st.text_area("What are your main skincare concerns? (e.g., acne, dryness, aging)")
        
        # Dropdown for selecting preferred consultation type
        consultation_type = st.selectbox(
            "Select Consultation Type",
            ["In-Person", "Video Call"]
        )

        # Date and time selection
        consultation_date = st.date_input("Preferred Date")
        consultation_time = st.time_input("Preferred Time")

        # Submit button
        submit_button = st.form_submit_button("Request Consultation")

        if submit_button:
            # Here you would typically handle the form submission (e.g., send an email or save to a database)
            st.success("Thank you for your request! We will get back to you shortly to confirm your consultation.")

# Call the function to render the page
if __name__ == "__main__":
    render_consultations_page()