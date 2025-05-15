import streamlit as st
import datetime

def local_css():
    # Apply the same custom CSS as in the About page
    st.markdown("""
    <style>
        /* Global Styles & Color Scheme */
        :root {
            --primary-color: #FF6B9B;
            --primary-light: #FFD2E6;
            --primary-dark: #D94073;
            --accent-color: #A771FF;
            --accent-light: #E5D4FF;
            --neutral-dark: #2A2A3A;
            --neutral-light: #F8F6FF;
            --text-light: #FFFFFF;
            --text-dark: #2A2A3A;
        }
        
        /* Base Styles */
        body {
            font-family: 'DM Sans', sans-serif;
            color: var(--text-dark);
            background-color: var(--neutral-light);
        }
        
        /* Header styling */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #403b3e;
    }
    
    h1 {
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        text-align: left;
        background: linear-gradient(90deg, #b76e79, #7c3c50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: var(--gradient-bg);
            
            color: white;
        }
        
        .sidebar .sidebar-content .block-container {
            padding-top: 2rem;
        }
        
        /* App header/title */
        .app-header {
            background-color: white;
            padding: 1.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .logo {
            font-family: 'Italiana', serif;
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-dark);
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin: 0;
        }
        
        /* Custom styling for sidebar navigation */
        section[data-testid="stSidebar"] {
            background-image: var(--gradient-bg);
            border-radius: 0 20px 20px 0;
        }
        
        section[data-testid="stSidebar"] > div {
            padding-top: 3rem;
            background: transparent;
        }
        
        /* Style for nav items in sidebar */
        .nav-item {
            padding: 0.75rem 1rem;
            border-radius: 10px;
            margin-bottom: 0.5rem;
            transition: all 0.2s ease;
            cursor: pointer;
            color: white;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .nav-item:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        .nav-item.active {
            background-color: white;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Page content styling */
        .content-section {
            background-color: white;
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        }
        
        .section-heading {
            color: var(--neutral-dark);
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            position: relative;
            display: inline-block;
        }
        
        .section-heading:after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--gradient-bg);
            border-radius: 3px;
        }
        
        /* How It Works Section */
        .step-container {
            display: flex;
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .step-card {
            flex: 1;
            background-color: var(--neutral-light);
            border-radius: 15px;
            padding: 1.5rem;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }
        
        .step-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }
        
        .step-number {
            position: absolute;
            top: -15px;
            left: 20px;
            width: 32px;
            height: 32px;
            background: var(--gradient-bg);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
        }
        
        .step-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .step-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--primary-dark);
        }
        
        /* Expert profiles section */
        .experts-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .expert-card {
            background-color: var(--neutral-light);
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .expert-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }
        
        .expert-image {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin: 0 auto 1rem auto;
            background-color: #ddd;
            overflow: hidden;
            position: relative;
        }
        
        .expert-name {
            font-weight: 600;
            color: var(--neutral-dark);
            margin-bottom: 0.3rem;
        }
        
        .expert-title {
            color: var(--primary-color);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
        
        .expert-bio {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 1rem;
        }
        
        /* Form styling */
        .form-container {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        }
        
        /* Style Streamlit form elements */
        div.stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem 1rem;
        }
        
        div.stTextInput > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 1px var(--primary-light);
        }
        
        div.stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem 1rem;
        }
        
        div.stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 1px var(--primary-light);
        }
        
        div.stSelectbox > div > div > div {
            border-radius: 10px;
            border: 1px solid #e0e0e0;
        }
        
        /* Form section styling */
        .form-section {
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="%23FFD2E6" opacity="0.3"/></svg>');
            background-repeat: no-repeat;
            background-position: bottom right;
            background-size: 300px;
            background-color: white;
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        }
        
        /* Success message styling */
        div.stAlert > div {
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg, rgba(255, 107, 155, 0.1) 0%, rgba(167, 113, 255, 0.1) 100%);
        }
        
        div.stAlert[data-baseweb="notification"] {
            border-radius: 10px;
            border-left: 4px solid var(--primary-color);
        }
        
        /* Button styling */
    
    
    /* Button styling */
    .stButton > button {
        border-radius: 30px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        color: white !important;
        background: linear-gradient(90deg, #b76e79, #7c3c50) !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(123, 60, 80, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 7px 15px rgba(123, 60, 80, 0.4) !important;
    }
        
        /* Beautify date and time inputs */
        div.stDateInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem 1rem;
        }
        
        /* Callout box */
        .callout {
            background-color: var(--primary-light);
            border-left: 4px solid var(--primary-color);
            border-radius: 10px;
            padding: 1rem;
            margin: 1.5rem 0;
        }
        
    /* Decorative elements */
    .decorative-line {
        height: 3px;
        background: linear-gradient(90deg, transparent, #b76e79, transparent);
        margin: 20px 0;
        border-radius: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

    
   

    
def render_consultations_page():
    local_css()
    
    # Consultation form
    st.markdown('<h1>Consultation</h1>', unsafe_allow_html=True)
    st.markdown(
            """
            <div style="text-align: left; margin-bottom: 25px; font-family: 'Poppins', sans-serif;">
                <p style="font-size: 1.2rem; color: #7c3c50; font-weight: 300;">
                    Discover your perfect skincare routine ✨
                </p>
            </div>
            """,
            unsafe_allow_html=True
    )
    # Decorative element
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)
        
    # Create columns for a two-column form layout
    col1, col2 = st.columns([1, 1])
    
    with st.form(key='consultation_form'):
        # First column - Personal Information
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            
            st.subheader("Your Skin Profile")
            skin_type = st.selectbox(
                "Skin Type",
                ["Select your skin type", "Dry", "Oily", "Combination", "Normal", "Sensitive"]
            )
            
            skin_concerns = st.multiselect(
                "Skin Concerns (select all that apply)",
                ["Acne", "Fine Lines & Wrinkles", "Hyperpigmentation", "Rosacea", 
                 "Dryness", "Oiliness", "Sensitivity", "Uneven Texture", "Dark Circles"]
            )
            
            current_routine = st.text_area("Briefly describe your current skincare routine")
        
        # Second column - Consultation Details
        with col2:
            st.subheader("Consultation Details")
            
            expert = st.selectbox(
                "Preferred Expert (Optional)",
                ["No preference", "Dr. Sophia Chen", "James Rivera", "Aisha Johnson"]
            )
            
            consultation_type = st.radio(
                "Consultation Type",
                ["Virtual (Video Call)", "In-Person"]
            )
            
            # Date picker with some constraints
            min_date = datetime.date.today() + datetime.timedelta(days=1)
            max_date = min_date + datetime.timedelta(days=30)
            consultation_date = st.date_input(
                "Preferred Date", 
                min_value=min_date,
                max_value=max_date,
                value=min_date + datetime.timedelta(days=3)
            )
            
            time_slots = [
                "9:00 AM - 10:00 AM", 
                "10:30 AM - 11:30 AM",
                "1:00 PM - 2:00 PM", 
                "2:30 PM - 3:30 PM",
                "4:00 PM - 5:00 PM"
            ]
            consultation_time = st.selectbox("Preferred Time Slot", time_slots)
            
            additional_notes = st.text_area("Any additional information or questions")
        
        # Submit button centered at bottom
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Schedule Consultation")
            
    # Handle form submission
    if submit_button:
        if name and email and skin_type != "Select your skin type" and len(skin_concerns) > 0:
            st.success("Thank you for your request! We've received your consultation details and will send a confirmation email shortly.")
            st.markdown("""
            <div style="background-color: var(--neutral-light); border-radius: 10px; padding: 1rem; margin-top: 1rem;">
                <p><strong>Next Steps:</strong></p>
                <ul>
                    <li>You'll receive a confirmation email within 24 hours</li>
                    <li>Our team will send you a short pre-consultation questionnaire</li>
                    <li>We'll provide instructions for your virtual session or in-person visit</li>
                </ul>
                <p style="margin-top: 1rem;">If you need to reschedule, please contact us at <span style="color: var(--primary-color);">support@beautybuzz.com</span></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Please fill out all required fields to schedule your consultation.")

    

# Call the function to render the page
if __name__ == "__main__":
    render_consultations_page()
