import streamlit as st

# Set page configuration
st.set_page_config(page_title="Healthcare", page_icon="🩺", layout="wide")

def render_healthcare_page():
    # Add custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f8f9fa;
            font-family: "Arial", sans-serif;
        }
        h1 {
            text-align: center;
            font-size: 2.8em;
            color: #5a189a;
            margin-bottom: 20px;
        }
        .big-square {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Responsive grid */
            gap: 20px;
            padding: 20px;
        }
        .box {
            border-radius: 12px;
            padding: 20px;
            background: linear-gradient(135deg, #6a4c93, #b5179e);
            color: white;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            cursor: pointer; /* Change cursor to pointer */
        }
        .box:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        .box h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .box p {
            font-size: 1em;
            line-height: 1.6em;
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