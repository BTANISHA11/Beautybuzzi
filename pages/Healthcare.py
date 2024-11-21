import os
import base64
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Healthcare", page_icon="🩺", layout="wide")

def render_healthcare_page():
    # Set up the script directory and image folder
    script_dir = os.path.dirname(__file__)
    image_folder = os.path.join(script_dir, "images")

    # Add custom CSS for layout and styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f9fafc;
            font-family: "Arial", sans-serif;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(4, 1fr); /* Adjust column count for square layout */
            gap: 20px;
            padding: 20px;
        }
        .box {
            border-radius: 15px;
            background: linear-gradient(135deg, #ffafbd, #ffc3a0); /* Chic gradient */
            color: #3d3d3d;
            text-align: center;
            padding: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .box:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
        }
        .box img {
            width: 200px; /* Smaller image size */
            height: 200px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .box h3 {
            font-size: 1.6em; /* More clear and open font size */
            margin: 10px 0;
            font-weight: bold;
            color: #333;
        }
        .box p {
            font-size: 1.1em; /* Better readability */
            line-height: 1.6em;
            color: #555;
        }
        /* Custom box layout */
        .box2 {
            grid-column: span 1;
            grid-row: span 2;
        }
        .box3 {
            grid-column: span 2;
            grid-row: span 1;
        }
        .box4 {
            grid-column: span 1;
            grid-row: span 1;
            border-radius: 50%; /* Circle shape */
        }
        .box5 {
            grid-column: span 2;
            grid-row: span 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #5a189a;">Healthcare Features</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature details with images
    features = [
        {
            "title": "Skincare Tips",
            "description": "Discover expert tips to maintain glowing, healthy skin through proper care and lifestyle changes.",
            "image": "skincare.jpg",
            "css_class": "box2",
        },
        {
            "title": "AI Skin Analysis",
            "description": "Get personalized skin insights with our AI-powered analysis tool, tailored to your unique needs.",
            "image": "skin_analysis.jpg",
            "css_class": "box3",
        },
        {
            "title": "Product Recommendations",
            "description": "Receive custom recommendations for skincare products that suit your skin type and goals.",
            "image": "beauty_products.jpg",
            "css_class": "box4",
        },
        {
            "title": "Healthy Diet",
            "description": "Learn how balanced nutrition promotes radiant skin and overall well-being.",
            "image": "healthy_diet.jpg",
            "css_class": "box5",
        },
        {
            "title": "Skincare Routine",
            "description": "Develop an effective skincare routine with step-by-step guidance for optimal results.",
            "image": "skincare_night_routine.jpg",
            "css_class": "box",
        },
        {
            "title": "Consultations",
            "description": "Book a session with certified skincare experts for personalized advice and treatment plans.",
            "image": "office_day.jpg",
            "css_class": "box",
        },
        {
            "title": "Customer Testimonials",
            "description": "Read inspiring success stories from our satisfied users and join the thriving community.",
            "image": "wedding.jpg",
            "css_class": "box",
        },
    ]

    # Render features in grid
    st.markdown('<div class="container">', unsafe_allow_html=True)
    for feature in features:
        image_path = os.path.join(image_folder, feature["image"])
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
            st.markdown(
                f"""
                <div class="box {feature['css_class']}">
                    <img src="data:image/jpeg;base64,{encoded_image}" alt="{feature['title']}">
                    <h3>{feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Call the function to render the page
render_healthcare_page()
