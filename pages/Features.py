import streamlit as st
import os

# Set page configuration
st.set_page_config(page_title="Beauty Buzz - Features", page_icon="✨", layout="wide")

# Custom CSS
custom_css = """
<style>
body {
    background-color: #f9ccd3; /* Light pinkish background */
    font-family: "Arial", sans-serif;
}

.features-container {
    text-align: center;
    padding: 50px 20px;
    color: #333;
    position: relative;
    overflow: hidden;
}

.features-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 30px;
    color: #aa1945; /* Rose Red color */
}

/* Center Images Layout */
.features-images {
    position: relative;
    width: 100%;
    max-width: 1000px;
    height: 500px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
}

.image-item {
    position: relative;
    width: 100%;
    height: 100%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

.image-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Shapes and Sizes */
.circle, .large-rect, .small-rect, .small-circle, .medium-square {
    position: absolute;
    z-index: -1;
}

.circle {
    width: 250px;
    height: 250px;
    top: -20%;
    left: -10%;
}

.large-rect {
    width: 300px;
    height: 500px;
    top: 80px;
    left: 40%;
}

.small-rect {
    width: 220px;
    height: 250px;
    top: 200px;
    left: 98%;
}

.small-circle {
    width: 200px;
    height: 150px;
    top: 320px;
    left: 5%;
}

.medium-square {
    width: 250px;
    height: 180px;
    top: 0;
    left: 95%;
}

/* Feature Descriptions */
.features-text {
    margin-top: 40px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
}

.text-item {
    max-width: 250px;
    text-align: left;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    position: relative;
}

.text-item h2 {
    font-size: 1.5rem;
    color: #391306; /* Puce color */
    margin-bottom: 10px;
}

.text-item p {
    font-size: 1.2rem; /* Bigger font size */
    color: #555; /* Grey color */
    line-height: 1.8; /* Increased line spacing */
}

/* Styling Numbers */
.text-item::before {
    content: attr(data-number);
    font-size: 5rem; /* Bigger size for numbers */
    font-weight: bold;
    color: #aa1945; /* Rose Red */
    position: absolute;
    top: -40px;
    left: -20px;
    z-index: -1;
}

@media (max-width: 768px) {
    .features-images {
        width: 100%;
        height: auto;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        position: relative;
    }

    .image-item {
        position: relative;
        margin: auto;
    }

    .features-text {
        flex-direction: column;
        align-items: center;
    }

    .text-item {
        text-align: center;
        margin: 20px 0;
    }
}
</style>

"""
st.markdown(custom_css, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='features-title'>Our Features</h1>", unsafe_allow_html=True)

# Image Group
st.markdown("<div class='features-images'>", unsafe_allow_html=True)
images = [
    {"src": "https://via.placeholder.com/150", "class": "circle"},
    {"src": "https://via.placeholder.com/300x400", "class": "large-rect"},
    {"src": "https://via.placeholder.com/200x250", "class": "small-rect"},
    {"src": "https://via.placeholder.com/150", "class": "circle"},
    {"src": "https://via.placeholder.com/150", "class": "circle"}
]

for img in images:
    st.markdown(f"""
    <div class='image-item {img['class']}'>
        <img src="{img['src']}" alt="Feature Image">
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Feature Text
st.markdown("<div class='features-text'>", unsafe_allow_html=True)
features = [
    {
        "title": "1 Real-Time Makeup Try-On",
        "description": "Experiment with different makeup styles instantly using your live camera feed."
    },
    {
        "title": "2 Occasion-Specific Suggestions",
        "description": "Receive personalized makeup recommendations for every occasion."
    },
    {
        "title": "3 Advanced Makeup Filters",
        "description": "Filter products by price, brand, and occasion to find your ideal match."
    },
    {
        "title": "4 AI-Powered Realism",
        "description": "Leverage AI to apply makeup styles with precision and natural-looking results."
    }
]

for idx, feature in enumerate(features, 1):
    st.markdown(f"""
        <div class="features-text>
                <div class='text-item' data-number="{idx}">
                   <h2 class="darkcolor">{feature['title']}</h2>
                   <p>{feature['description']}</p>
                   <hr/>
                </div>
        </div>
    
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
