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

    st.markdown('<h1>Book a Consultation</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:1.1rem;color:#7c3c50;font-family:'Poppins',sans-serif;">
        Connect with a certified expert — skincare, grooming, makeup or hair. Tailored advice just for you. ✨
    </p>
    """, unsafe_allow_html=True)
    st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

    # ── Expert cards ────────────────────────────────────────────────────────────
    st.markdown("### 👩‍⚕️ Meet Our Experts")
    experts = [
        {"name": "Dr. Sophia Chen", "role": "Dermatologist", "icon": "🏥",
         "specialties": ["Acne & Breakouts", "Anti-Ageing", "Rosacea & Eczema", "Prescription Skincare"],
         "exp": "12 years", "lang": "English, Mandarin", "rating": "⭐ 4.9"},
        {"name": "James Rivera", "role": "Men's Grooming Specialist & Barber", "icon": "✂️",
         "specialties": ["Beard Care & Styling", "Men's Skincare Routines", "Hair Loss & Thinning", "Scalp Health"],
         "exp": "9 years", "lang": "English, Spanish", "rating": "⭐ 4.8"},
        {"name": "Aisha Johnson", "role": "Certified Makeup Artist & Colour Expert", "icon": "💄",
         "specialties": ["Makeup for All Skin Tones", "Bridal & Event Looks", "Colour Theory", "Clean Beauty"],
         "exp": "11 years", "lang": "English, French", "rating": "⭐ 4.9"},
        {"name": "Priya Mehta", "role": "Trichologist & Hair Specialist", "icon": "💇",
         "specialties": ["Hair Loss Diagnosis", "Scalp Treatments", "Natural Hair Care", "Hair Colour Safety"],
         "exp": "8 years", "lang": "English, Hindi", "rating": "⭐ 4.7"},
    ]

    expert_cols = st.columns(4)
    for i, exp in enumerate(experts):
        with expert_cols[i]:
            st.markdown(f"""
            <div style="background:white;border-radius:16px;padding:18px 14px;text-align:center;
                        box-shadow:0 4px 16px rgba(183,110,121,0.10);margin-bottom:8px;min-height:260px;">
                <div style="font-size:2.2rem;">{exp['icon']}</div>
                <b style="font-size:0.97rem;color:#403b3e;">{exp['name']}</b><br>
                <span style="font-size:0.78rem;color:#7c3c50;font-weight:600;">{exp['role']}</span><br>
                <span style="font-size:0.75rem;color:#888;">{exp['rating']} · {exp['exp']} exp</span><br>
                <hr style="margin:8px 0;">
                {''.join(f'<span style="display:inline-block;background:#fce4e8;color:#7c3c50;border-radius:20px;padding:2px 8px;font-size:0.7rem;margin:2px;">{s}</span>' for s in exp['specialties'])}
                <br><span style="font-size:0.73rem;color:#aaa;">🌐 {exp['lang']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Booking form ────────────────────────────────────────────────────────────
    st.markdown("### 📅 Schedule Your Consultation")
    with st.form(key="consultation_form"):
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### 👤 About You")
            name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number (optional)")
            gender = st.selectbox("I identify as", ["Woman", "Man", "Non-binary", "Prefer not to say"])
            age_group = st.selectbox("Age Group", ["Under 18", "18–25", "26–35", "36–45", "46–55", "55+"])

            st.markdown("#### 🧴 Your Skin & Hair Profile")
            skin_type = st.selectbox("Skin Type", ["Select…", "Normal", "Oily", "Dry", "Combination", "Sensitive"])
            skin_concerns = st.multiselect("Primary Concerns",
                ["Acne / Breakouts", "Fine Lines & Wrinkles", "Hyperpigmentation / Dark Spots",
                 "Rosacea / Redness", "Dryness / Flakiness", "Oiliness", "Sensitivity / Eczema",
                 "Uneven Texture", "Dark Circles", "Hair Loss / Thinning", "Beard Care",
                 "Scalp Issues", "Makeup Advice", "Bridal / Event Prep"])
            current_routine = st.text_area("Describe your current skincare or grooming routine (optional)", height=90)

        with c2:
            st.markdown("#### 📋 Consultation Details")
            expert_choice = st.selectbox("Preferred Expert", ["No Preference"] + [e["name"] for e in experts])
            consult_type = st.radio("Consultation Format", ["🎥 Video Call (Virtual)", "🏢 In-Person Visit"])
            consult_goal = st.selectbox("Primary Goal",
                ["Build a personalised routine", "Solve a specific skin concern",
                 "Pre-event / bridal prep", "Men's grooming plan", "Hair & scalp care",
                 "Makeup coaching", "General advice"])
            budget = st.select_slider("Budget for Products / Services", options=["Under $50", "$50–$100", "$100–$200", "$200+"])

            min_date = datetime.date.today() + datetime.timedelta(days=1)
            consult_date = st.date_input("Preferred Date", min_value=min_date,
                                          max_value=min_date + datetime.timedelta(days=60),
                                          value=min_date + datetime.timedelta(days=3))
            time_slots = ["9:00 AM", "10:30 AM", "12:00 PM", "1:30 PM", "3:00 PM", "4:30 PM", "6:00 PM"]
            consult_time = st.selectbox("Preferred Time Slot", time_slots)
            notes = st.text_area("Additional questions or information (optional)", height=90)

        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            submitted = st.form_submit_button("✨ Request Consultation")

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Full Name is required.")
        if not email.strip() or "@" not in email:
            errors.append("A valid Email Address is required.")
        if skin_type == "Select…":
            errors.append("Please select your Skin Type.")
        if not skin_concerns:
            errors.append("Please select at least one Primary Concern.")

        if errors:
            for e in errors:
                st.error(e)
        else:
            st.success(f"🎉 Thank you, **{name}**! Your consultation request has been received.")
            st.markdown(f"""
            <div style="background:#fff8f9;border-radius:14px;padding:18px 22px;border:1px solid #f0d0d5;margin-top:10px;">
                <b>📋 Booking Summary</b><br><br>
                <b>Expert:</b> {expert_choice}<br>
                <b>Format:</b> {consult_type}<br>
                <b>Date & Time:</b> {consult_date.strftime('%A, %d %B %Y')} at {consult_time}<br>
                <b>Goal:</b> {consult_goal}<br><br>
                <b>Next Steps:</b><br>
                • Confirmation email will arrive within 24 hours at <b>{email}</b><br>
                • You'll receive a short pre-consultation questionnaire to help your expert prepare<br>
                • {"A secure video link will be shared 1 hour before your session." if "Video" in consult_type else "Your in-person location and directions will be provided."}<br><br>
                <span style="color:#7c3c50;">Need to reschedule? Contact us at <b>support@beautybuzzi.com</b></span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── FAQ Section ─────────────────────────────────────────────────────────────
    st.markdown("### ❓ Frequently Asked Questions")
    faqs = [
        ("How long is a consultation?", "Standard consultations are 45–60 minutes. Follow-up sessions are 20–30 minutes."),
        ("Do you offer consultations for men?", "Absolutely. James Rivera specialises in men's grooming, skincare and beard care. All our experts are trained to advise everyone regardless of gender."),
        ("What should I prepare before my session?", "Take note of the products you currently use, any skin reactions you've had, and bring photos of your skin (no makeup) in natural light if possible."),
        ("Are the video calls secure?", "Yes. We use end-to-end encrypted video platforms. No session recordings are stored without explicit consent."),
        ("Can I get product recommendations after?", "Yes. Your expert will send a personalised product list within 48 hours of your session via email."),
        ("Is there a cancellation policy?", "You can reschedule or cancel up to 24 hours before your session with no charge. Within 24 hours, a 50% fee applies."),
        ("Do you accept health insurance?", "Dermatology consultations with Dr. Sophia Chen may be partially covered depending on your provider. We provide receipts for reimbursement claims."),
    ]
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.write(a)

    st.markdown("---")
    st.caption("© 2025 BeautyBuzzi | All consultations are confidential and conducted by certified professionals.")


# Call the function to render the page
if __name__ == "__main__":
    render_consultations_page()

