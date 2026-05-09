"""
🎨 FOUNDATION SHADE MATCHER PAGE
AI-powered foundation selection (Phase 5 Integration)
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image

import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from foundation_matcher import AIFoundationMatcher
except ImportError as e:
    st.error(f"⚠️ Foundation matcher module not found: {e}")
    st.stop()

st.set_page_config(page_title="🎨 Foundation Matcher", page_icon="💄", layout="wide")

st.title("🎨 AI Foundation Shade Matcher")
st.markdown("""
**Find your perfect foundation shade in seconds**
- 🧬 Advanced skin tone detection
- 🔬 White balance correction for accurate analysis
- 🎨 Undertone analysis (warm, cool, neutral)
- 💄 Top 3 shade recommendations
- 📊 Delta-E color matching precision
""")

# ============================================================================
# INITIALIZATION
# ============================================================================

matcher = AIFoundationMatcher()

# ============================================================================
# MAIN INTERFACE
# ============================================================================

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📸 Upload or Take a Photo")
    
    input_method = st.radio("Choose input method:", ["📤 Upload", "📷 Webcam"])
    
    if input_method == "📤 Upload":
        uploaded_file = st.file_uploader("Choose a clear face photo", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Photo", use_column_width=True)
            
            # Convert to OpenCV format
            image_np = np.array(image)
            if len(image_np.shape) == 3 and image_np.shape[2] == 4:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    else:
        picture = st.camera_input("Take a photo with your webcam")
        if picture:
            image = Image.open(picture)
            image_np = np.array(image)
            if len(image_np.shape) == 3 and image_np.shape[2] == 4:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

with col2:
    st.subheader("⚙️ Analysis Tips")
    st.info("""
    **For Best Results:**
    ✓ Use natural daylight
    ✓ Face clearly visible
    ✓ No heavy makeup
    ✓ No extreme shadows
    ✓ Neutral expression
    """)

# ============================================================================
# ANALYSIS
# ============================================================================

st.divider()

if 'image_bgr' in locals():
    if st.button("🔬 Analyze & Find Shades", type="primary"):
        with st.spinner("Analyzing your skin tone..."):
            # Run foundation matching
            match_result = matcher.match_foundation(image_bgr)
        
        st.success("✅ Analysis Complete!")
        
        # ============================================================================
        # RESULTS DISPLAY
        # ============================================================================
        
        tab1, tab2, tab3 = st.tabs(["🎨 Skin Profile", "💄 Top Matches", "📊 Details"])
        
        # ============================================================================
        # TAB 1: SKIN PROFILE
        # ============================================================================
        
        with tab1:
            st.subheader("Your Skin Profile")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Skin Tone", match_result['skin_tone'].title())
            
            with col2:
                st.metric("Undertone", match_result['undertone'].title())
            
            with col3:
                st.metric("Confidence", f"{match_result['confidence']:.0%}")
            
            with col4:
                st.metric("Analysis", "✅ Complete")
            
            st.divider()
            
            # Skin tone description
            tone_descriptions = {
                'fair': 'Very light skin with subtle undertones',
                'light': 'Light to medium-light skin with delicate features',
                'medium': 'Medium depth skin with varied undertones',
                'tan': 'Deeper tan skin with warm or cool undertones',
                'deep': 'Deep skin tone with rich, vibrant undertones'
            }
            
            undertone_descriptions = {
                'warm': 'Yellow, peachy, or golden undertones - pair with warm neutrals and earthy tones',
                'cool': 'Pink, red, or blue undertones - pair with cool tones and jewel colors',
                'neutral': 'Balanced mix of warm and cool - wear any color confidently'
            }
            
            st.write(f"**Skin Tone:** {tone_descriptions.get(match_result['skin_tone'], 'Unknown')}")
            st.write(f"**Undertone:** {undertone_descriptions.get(match_result['undertone'], 'Unknown')}")
            
            # Color preview
            st.write("**Your Skin Color (Extracted):**")
            r, g, b = match_result['skin_color_rgb']
            col1, col2 = st.columns([1, 4])
            with col1:
                st.color_picker("", f"#{int(r):02x}{int(g):02x}{int(b):02x}", disabled=True, label_visibility="collapsed")
            with col2:
                st.write(f"RGB: ({int(r)}, {int(g)}, {int(b)})")
        
        # ============================================================================
        # TAB 2: TOP MATCHES
        # ============================================================================
        
        with tab2:
            st.subheader("💄 Top 3 Foundation Matches")
            st.write("These shades are your closest matches. Try them in-store!")
            
            for i, match in enumerate(match_result['top_matches'], 1):
                st.divider()
                
                col1, col2, col3 = st.columns([1.5, 2, 1.5])
                
                # Color preview
                with col1:
                    r, g, b = match['rgb']
                    st.color_picker(
                        f"Match #{i}",
                        f"#{int(b):02x}{int(g):02x}{int(r):02x}",  # BGR to RGB
                        disabled=True
                    )
                
                # Details
                with col2:
                    st.write(f"**#{i} {match['brand']} {match['name']}**")
                    st.write(f"Undertone: {match['undertone'].title()}")
                    st.write(f"Tone: {match['tone'].title()}")
                
                # Match score
                with col3:
                    match_score = max(0, 100 - match['delta_e'])
                    st.metric("Match Score", f"{match_score:.0f}/100")
                
                # Buy button (placeholder)
                col_button = st.columns([1, 1, 1])
                with col_button[1]:
                    if st.button(f"🛍️ Find on Sephora", key=f"sephora_{i}"):
                        st.info(f"Search '{match['brand']} {match['name']}' on Sephora.com")
        
        # ============================================================================
        # TAB 3: TECHNICAL DETAILS
        # ============================================================================
        
        with tab3:
            st.subheader("📊 Analysis Details")
            
            st.write("**LAB Color Space Analysis:**")
            l, a, b = match_result['skin_color_lab']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("L* (Lightness)", f"{l}")
                st.caption("0=Black, 100=White")
            with col2:
                st.metric("a* (Green-Magenta)", f"{a}")
                st.caption("-=Green, +=Magenta")
            with col3:
                st.metric("b* (Blue-Yellow)", f"{b}")
                st.caption("-=Blue, +=Yellow")
            
            st.divider()
            
            st.write("**All Matches (by score):**")
            
            # Show all matches with Delta-E values
            all_matches_data = []
            for match in match_result['top_matches']:
                all_matches_data.append({
                    'Brand': match['brand'],
                    'Shade': match['name'],
                    'Undertone': match['undertone'].title(),
                    'Tone': match['tone'].title(),
                    'Match Score': f"{max(0, 100 - match['delta_e']):.0f}/100",
                    'Delta-E': f"{match['delta_e']:.2f}"
                })
            
            import pandas as pd
            df = pd.DataFrame(all_matches_data)
            st.dataframe(df, use_container_width=True)
            
            st.divider()
            
            st.write("**What is Delta-E?**")
            st.info("""
            Delta-E measures color difference on a scale where:
            - **0** = Identical match
            - **1-2** = Imperceptible difference (best matches)
            - **3-10** = Noticeable but acceptable
            - **11+** = Significant difference
            
            Our algorithm uses CIE76 Delta-E for perceptual accuracy.
            """)

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

st.divider()

st.subheader("💡 Foundation Tips")

col1, col2 = st.columns(2)

with col1:
    st.write("**How to Apply:**")
    st.write("""
    1. Apply primer for smoother texture
    2. Use small dots across face
    3. Blend with damp beauty sponge
    4. Set with translucent powder
    5. Use setting spray for longevity
    """)

with col2:
    st.write("**Pro Tips:**")
    st.write("""
    - Test in natural light (not store lighting)
    - Match to jawline, not just cheek
    - Consider undertone, not just depth
    - Blend 2 shades if in-between
    - Retest after seasonal changes
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
🎨 **AI Foundation Matcher** | Advanced undertone & tone detection
Using LAB color space analysis and Delta-E color matching precision
""")
