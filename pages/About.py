import streamlit as st

# Set page configuration
st.set_page_config(layout="wide", page_title="About Us")

def render_about_page():
   # Adding CSS styles for the containers
    st.markdown(
        """
        <style>
        .feature-box {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }
        .feature-line {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .feature-line img {
            width: 60px;
            height: 60px;
            border-radius: 10px;
        }
        /* Alternate the layout for each feature */
        .feature-line:nth-child(even) {
            flex-direction: row-reverse; /* Reverse the order for even elements */
        }
        .feature-line h4 {
            margin: 0;
            font-size: 18px;
            font-weight: bold;
        }
        .feature-line p {
            margin: 5px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-box">
            <h4>FEATURES</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Adding container-like boxes for each feature
    with st.container():
        # First Feature - Image on the left, Text on the right
        st.markdown(
            """
            <div class="feature-line">
            """,
            unsafe_allow_html=True,
        )
        st.image("./imgs/hero4.png", use_column_width=False)
        st.markdown(
            """
            <div>
                <h4>AI-powered Makeup Application</h4>
                <p>Leverage advanced AI technology to apply virtual makeup effortlessly.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr/>", unsafe_allow_html=True)

        # Second Feature - Image on the right, Text on the left (alternate order)
        st.markdown(
            """
            <div class="feature-line">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div>
                <h4>Virtual Try-On for Lips, Hair, and Foundation</h4>
                <p>Experiment with different shades and styles virtually before committing to a look.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.image("./imgs/img3.png", width=60, height=60)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        # Third Feature - Image on the left, Text on the right
        st.markdown(
            """
            <div class="feature-line">
            """,
            unsafe_allow_html=True,
        )
        st.image("./imgs/hero4.png", use_column_width=False)
        st.markdown(
            """
            <div>
                <h4>Customizable Parameters for Shades</h4>
                <p>Fine-tune your makeup shades to match your unique preferences.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr/>", unsafe_allow_html=True)

        # Fourth Feature - Image on the right, Text on the left (alternate order)
        st.markdown(
            """
            <div class="feature-line">
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div>
                <h4>Save and Share Your Favorite Looks</h4>
                <p>Keep a record of your favorite styles and share them with friends.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.image("./imgs/hero6.jpg", width=60, height=60)
        st.markdown("</div>", unsafe_allow_html=True)

# Call the function to render the page
render_about_page()
