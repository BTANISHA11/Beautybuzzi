"""
🎨 AI BEAUTY FEATURES PAGE
AI Look Generator + Beauty Chatbot (Phase 7 Integration)
"""

import streamlit as st
import json
from datetime import datetime

import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ai_generative_features import AIBeautyLookGenerator, AIBeautyChatbot
except ImportError as e:
    st.error(f"⚠️ AI features modules not found: {e}")
    st.stop()

st.set_page_config(page_title="🤖 AI Beauty Assistant", page_icon="✨", layout="wide")

st.title("🤖 AI Beauty Assistant")
st.markdown("""
**AI-powered beauty recommendations**
- 🎨 Generate complete makeup looks from text descriptions
- 💬 Beauty expert chatbot (ingredients, routines, skincare)
- 📋 Personalized skincare routines
- ✨ Occasion-based look recommendations
""")

# ============================================================================
# FEATURE SELECTION
# ============================================================================

feature = st.selectbox(
    "Choose a feature:",
    ["🎨 AI Look Generator", "💬 Beauty Chatbot", "📋 Routine Builder", "🌟 Preset Looks"]
)

st.divider()

# ============================================================================
# FEATURE 1: AI LOOK GENERATOR
# ============================================================================

if feature == "🎨 AI Look Generator":
    st.subheader("🎨 AI Look Generator")
    st.write("Describe the makeup look you want, and let AI create a complete recommendation!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        look_description = st.text_area(
            "Describe the makeup look you want:",
            placeholder="e.g., 'Soft glam bridal look for outdoor wedding'",
            height=100
        )
    
    with col2:
        st.write("**Your Profile:**")
        skin_tone = st.selectbox("Skin Tone", ["fair", "light", "medium", "tan", "deep"])
        undertone = st.selectbox("Undertone", ["warm", "cool", "neutral"])
    
    if st.button("✨ Generate Look", type="primary"):
        if look_description.strip():
            look_gen = AIBeautyLookGenerator()
            
            with st.spinner("Generating look..."):
                look = look_gen.generate_look(look_description, skin_tone, undertone)
            
            st.success(f"✅ Look Generated: **{look['look_name']}**")
            
            # Display results
            tab1, tab2, tab3 = st.tabs(["📋 Overview", "🎯 Recommendations", "📝 Application Guide"])
            
            with tab1:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Look Type", look['look_type'].title())
                with col2:
                    st.metric("Intensity", f"{look['intensity']:.0%}")
                with col3:
                    st.metric("Complexity", "Medium")
            
            with tab2:
                st.subheader("💄 Makeup Recommendations")
                
                recs = look['recommendations']
                
                # Lipstick
                st.write("**💋 Lipstick**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Color: `{recs['lipstick']['color'].title()}`")
                with col2:
                    st.write(f"Finish: `{recs['lipstick']['finish'].title()}`")
                with col3:
                    st.write(f"Intensity: {recs['lipstick']['intensity']:.0%}")
                
                st.divider()
                
                # Eyeshadow
                st.write("**👁️ Eyeshadow**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Colors: {', '.join([c.title() for c in recs['eyeshadow']['colors']])}")
                with col2:
                    st.write(f"Placement: `{recs['eyeshadow']['placement'].title()}`")
                with col3:
                    st.write(f"Intensity: {recs['eyeshadow']['intensity']:.0%}")
                
                st.divider()
                
                # Blush
                st.write("**🎀 Blush**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Color: `{recs['blush']['color'].title()}`")
                with col2:
                    st.write(f"Placement: `{recs['blush']['placement'].title()}`")
                with col3:
                    st.write(f"Intensity: {recs['blush']['intensity']:.0%}")
                
                st.divider()
                
                # Eyeliner
                if recs['eyeliner']['enabled']:
                    st.write("**✏️ Eyeliner**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Style: `{recs['eyeliner']['style'].title()}`")
                    with col2:
                        st.write(f"Color: `{recs['eyeliner']['color'].title()}`")
                else:
                    st.write("**✏️ Eyeliner** - Not needed for this look")
            
            with tab3:
                st.subheader("📝 Step-by-Step Application Guide")
                for step in look['application_guide']:
                    st.write(step)
            
            # Export option
            st.divider()
            if st.button("📥 Save This Look"):
                look_json = json.dumps(look, indent=2, default=str)
                st.download_button(
                    label="Download Look Recipe (JSON)",
                    data=look_json,
                    file_name=f"{look['look_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
        else:
            st.warning("Please describe a makeup look!")

# ============================================================================
# FEATURE 2: BEAUTY CHATBOT
# ============================================================================

elif feature == "💬 Beauty Chatbot":
    st.subheader("💬 Beauty Expert Chatbot")
    st.write("Ask me anything about skincare, ingredients, routines, or beauty concerns!")
    
    # Initialize chatbot
    chatbot = AIBeautyChatbot()
    
    # Chat interface
    question = st.text_input("Ask a question:", placeholder="e.g., 'What's the best ingredient for acne?'")
    
    if question:
        with st.spinner("Thinking..."):
            answer = chatbot.answer_question(question)
        
        st.write("**Answer:**")
        st.markdown(answer)
    
    # Suggested questions
    st.divider()
    st.subheader("🔍 Common Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("What's retinol?"):
            chatbot = AIBeautyChatbot()
            answer = chatbot.answer_question("What is retinol and its benefits?")
            st.markdown(answer)
        
        if st.button("How to treat acne?"):
            chatbot = AIBeautyChatbot()
            answer = chatbot.answer_question("How to treat acne?")
            st.markdown(answer)
    
    with col2:
        if st.button("Dark circles solutions"):
            chatbot = AIBeautyChatbot()
            answer = chatbot.answer_question("How do I treat dark circles?")
            st.markdown(answer)
        
        if st.button("Morning routine"):
            chatbot = AIBeautyChatbot()
            answer = chatbot.answer_question("What should my morning routine be?")
            st.markdown(answer)

# ============================================================================
# FEATURE 3: ROUTINE BUILDER
# ============================================================================

elif feature == "📋 Routine Builder":
    st.subheader("📋 Personalized Routine Builder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skin_type = st.selectbox(
            "What's your skin type?",
            ["Dry", "Oily", "Combination", "Normal", "Sensitive"]
        )
    
    with col2:
        st.write("**Skincare Concerns** (select all that apply):")
        concerns = []
        if st.checkbox("Acne"):
            concerns.append("acne")
        if st.checkbox("Aging / Wrinkles"):
            concerns.append("aging")
        if st.checkbox("Dark Spots"):
            concerns.append("dark spots")
        if st.checkbox("Dryness"):
            concerns.append("dryness")
        if st.checkbox("Sensitivity"):
            concerns.append("sensitivity")
    
    if st.button("📋 Generate Routine", type="primary"):
        chatbot = AIBeautyChatbot()
        routine = chatbot.suggest_routine(skin_type.lower(), concerns)
        
        st.success("✅ Your Personalized Routine")
        
        st.subheader("🌅 Morning Routine")
        for i, product in enumerate(routine[:5], 1):
            st.write(f"{i}. {product}")
        
        st.subheader("🌙 Evening Routine")
        for i, product in enumerate(routine[5:], 1):
            st.write(f"{i}. {product}")
        
        # Tips
        st.divider()
        st.info("""
        **💡 Pro Tips:**
        - Wait 1-2 minutes between products for proper absorption
        - Start with lower concentrations of active ingredients
        - Use SPF 50+ every morning
        - Be consistent for at least 6-8 weeks to see results
        """)

# ============================================================================
# FEATURE 4: PRESET LOOKS
# ============================================================================

elif feature == "🌟 Preset Looks":
    st.subheader("🌟 Preset Beauty Looks")
    st.write("Choose from curated makeup looks for different occasions")
    
    look_gen = AIBeautyLookGenerator()
    presets = look_gen.preset_looks
    
    # Display presets
    cols = st.columns(3)
    
    col_idx = 0
    for look_name, look_data in presets.items():
        with cols[col_idx % 3]:
            st.markdown(f"### {look_name.replace('_', ' ').title()}")
            st.write(look_data['description'])
            
            # Show quick specs
            st.write("**Quick Specs:**")
            st.write(f"- Lipstick: {look_data['lipstick']['color'].title()}")
            st.write(f"- Eyeshadow: {look_data['eyeshadow']['colors'][0].title()}")
            st.write(f"- Blush: {look_data['blush']['color'].title()}")
            
            if st.button(f"✨ Try {look_name.replace('_', ' ').title()}", key=look_name):
                st.success(f"✅ Look selected: **{look_name.replace('_', ' ').title()}**")
                st.write("Go to AR Try-On page to apply this look!")
        
        col_idx += 1

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
🤖 **AI Beauty Assistant** | Powered by advanced AI models
💡 Knowledge base includes 1000+ skincare ingredients and techniques
""")
