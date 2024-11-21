import streamlit as st

def render_features_page():
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
        }
        .feature-line img {
            width: 60px;
            height: 60px;
            border-radius: 10px;
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
        st.markdown(
            """
            <div class="feature-box">
                <div class="feature-line">
                    <img src="./imgs/img3.png" alt="AI-powered Makeup">
                    <div>
                        <h4>AI-powered Makeup Application</h4>
                        <p>Leverage advanced AI technology to apply virtual makeup effortlessly.</p>
                    </div>
                </div>
                <hr/>
                <div class="feature-line">
                    <img src="../imgs/img3.png" alt="Virtual Try-On">
                    <div>
                        <h4>Virtual Try-On for Lips, Hair, and Foundation</h4>
                        <p>Experiment with different shades and styles virtually before committing to a look.</p>
                    </div>
                </div>
                <hr/>
                <div class="feature-line">
                    <img src="../imgs/img (1).png" alt="Customizable Parameters">
                    <div>
                        <h4>Customizable Parameters for Shades</h4>
                        <p>Fine-tune your makeup shades to match your unique preferences.</p>
                    </div>
                </div>
                <hr/>
                <div class="feature-line">
                    <img src="https://via.placeholder.com/60" alt="Save and Share">
                    <div>
                        <h4>Save and Share Your Favorite Looks</h4>
                        <p>Keep a record of your favorite styles and share them with friends.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
