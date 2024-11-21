import streamlit as st

# Set page configuration
st.set_page_config(page_title="Healthcare", page_icon="🩺", layout="wide")

def render_healthcare_page():
    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f9f9f9;
            font-family: "Arial", sans-serif;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #4a4a4a;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .big-square {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* Responsive grid */
            gap: 20px;
            padding: 20px;
        }
        .box {
            border: 1px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            background-color: #ffffff;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .box:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .box h3 {
            font-size: 1.4em;
            color: #2a2a2a;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .box p {
            font-size: 1em;
            color: #6c757d;
            line-height: 1.6em;
        }
        a {
            text-decoration: none;
        }
        a:hover {
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown("<h1>Healthcare Features</h1>", unsafe_allow_html=True)

    # Features grid with links
    st.markdown(
        """
        <div class="big-square">
            <a href="/skincare_tips">
                <div class="box">
                    <h3>Skincare Tips</h3>
                    <p>Discover expert tips to maintain glowing, healthy skin through proper care and lifestyle changes.</p>
                </div>
            </a>
            <a href="/ai_skin_analysis">
                <div class="box">
                    <h3>AI Skin Analysis</h3>
                    <p>Get personalized skin insights with our AI-powered analysis tool, tailored to your unique needs.</p>
                </div>
            </a>
            <a href="/product_recommendations">
                <div class="box">
                    <h3>Product Recommendations</h3>
                    <p>Receive custom recommendations for skincare products that suit your skin type and goals.</p>
                </div>
            </a>
            <a href="/healthy_diet">
                <div class="box">
                    <h3>Healthy Diet</h3>
                    <p>Learn how balanced nutrition promotes radiant skin and overall well-being.</p>
                </div>
            </a>
            <a href="/skincare_routine">
                <div class="box">
                    <h3>Skincare Routine</h3>
                    <p>Develop an effective skincare routine with step-by-step guidance for optimal results.</p>
                </div>
            </a>
            <a href="/consultations">
                <div class="box">
                    <h3>Consultations</h3>
                    <p>Book a session with certified skincare experts for personalized advice and treatment plans.</p>
                </div>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Call the function to render the page
render_healthcare_page()
