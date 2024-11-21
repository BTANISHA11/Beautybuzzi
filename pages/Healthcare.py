import streamlit as st

# Must be the first command in the script
st.set_page_config(layout="wide", page_title="Healthcare")

def render_healthcare_page():
    # Add CSS for custom styling with hover effect
    st.markdown(
        """
        <style>
        .big-square {
            display: grid;
            grid-template-columns: repeat(4, 1fr);  # 4 equal columns
            grid-template-rows: repeat(3, 1fr);     # 3 equal rows
            gap: 10px !important;
            
            width: 100%;
            height: 100vh;
        }
        .box {
            border-radius: 10px;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            text-align: center;
            color: white;
            transition: transform 0.3s, background 0.3s;
            background-size: cover;
            background-position: center;
            height: 100%;
      
        }
        .box1 {
        margin:10px;
            grid-column: 1 / 3;
            grid-row: 1 / 2;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box2 {
        margin:10px;
            grid-column: 3 / 4;
            grid-row: 1 / 2;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box3 {
        margin:10px;
            grid-column: 1 / 2;
            grid-row: 2 / 3;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box4 {
        margin:10px;
            grid-column: 2 / 3;
            grid-row: 2 / 3;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box5 {
        margin:10px;
            grid-column: 3 / 4;
            grid-row: 2 / 3;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box6 {
        margin:10px;
            grid-column: 1 / 3;
            grid-row: 3 / 4;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box7 {
        margin:10px;
            grid-column: 3 / 4;
            grid-row: 3 / 4;
            background: rgba(0, 0, 0, 0.5);  # Replace with your image URL
        }
        .box:hover {
            background: rgba(0, 0, 0, 0.5);  # Adding a dark overlay on hover
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Add the HTML structure for the grid layout
    st.markdown(
        """
        <div><h1>HEALTHCARE</h1></div>
        <div class="big-square">
            <div class="box box1">
                <h3>Skincare Tips</h3>
                <p>Explore tips for achieving better skin health and maintaining a glowing complexion.</p>
            </div>
            <div class="box box2">
                <h3>AI Skin Analysis</h3>
                <p>Leverage AI to understand your skin better and get tailored insights.</p>
            </div>
            <div class="box box3">
                <h3>Product Recommendations</h3>
                <p>Receive personalized product suggestions to match your unique skin needs.</p>
            </div>
            <div class="box box4">
                <h3>Healthy Diet</h3>
                <p>Learn about the foods that promote healthy skin and a healthy body.</p>
            </div>
            <div class="box box5">
                <h3>Skincare Routine</h3>
                <p>Understand the importance of a consistent skincare routine for lasting results.</p>
            </div>
            <div class="box box6">
                <h3>Consultations</h3>
                <p>Book a consultation with a skincare expert to receive personalized advice.</p>
            </div>
            <div class="box box7">
                <h3>Customer Testimonials</h3>
                <p>See how our products have worked wonders for others and join the community.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Call the function to render the page
render_healthcare_page()
