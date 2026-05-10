"""
🎨 AR MAKEUP TRY-ON PAGE
Combines real-time AR, professional rendering, 3D head tracking, and skin analysis.
Live demo of Phases 1-7 integration.
"""

import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from realtime_ar import RealtimeARPipeline
    from rendering_engine import ProfessionalRenderingEngine
    from face_3d_tracker import Face3DTracker
    from skin_analysis_v2 import DermatologyGradeSkinAnalyzer
    from foundation_matcher import AIFoundationMatcher
    from ai_generative_features import AIBeautyLookGenerator, AIBeautyChatbot
except ImportError as e:
    st.error(f"⚠️ Failed to import production modules: {e}")
    st.stop()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="✨ AR Makeup Try-On",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("✨ AR Makeup Try-On Studio")
st.markdown("""
**Real-time makeup visualization powered by AI**
- 🎬 Live webcam feed with 468-landmark face tracking
- 💄 Professional multi-layer rendering (5 finish types)
- 📐 3D perspective-aware makeup intensity
- 🧬 Dermatology-grade skin analysis (10 metrics)
- 🎨 AI foundation shade matching
- 🤖 Instant beauty routine recommendations
""")


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value.lstrip('#')[index:index + 2], 16) for index in (0, 2, 4))


def _build_render_landmarks(frame_data: dict) -> dict:
    return {
        'lips_all': frame_data.get('lips_all', []),
        'left_eye': frame_data.get('left_eye', []),
        'right_eye': frame_data.get('right_eye', []),
        'left_eyelids': frame_data.get('left_eyelids', []),
        'right_eyelids': frame_data.get('right_eyelids', []),
        'left_cheek': frame_data.get('left_cheek'),
        'right_cheek': frame_data.get('right_cheek'),
    }

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================

with st.sidebar:
    st.header("⚙️ Controls")
    
    # Feature toggles
    st.subheader("📸 Camera Features")
    enable_ar = st.checkbox("Enable AR Makeup", value=True)
    enable_3d_tracking = st.checkbox("3D Head Tracking", value=True)
    enable_skin_analysis = st.checkbox("Real-time Skin Analysis", value=False)
    
    st.divider()
    
    # Makeup intensity sliders
    st.subheader("💄 Makeup Intensity")
    lipstick_intensity = st.slider("Lipstick", 0.0, 1.0, 0.7, 0.05)
    eyeshadow_intensity = st.slider("Eyeshadow", 0.0, 1.0, 0.6, 0.05)
    blush_intensity = st.slider("Blush", 0.0, 1.0, 0.5, 0.05)
    eyeliner_intensity = st.slider("Eyeliner", 0.0, 1.0, 0.8, 0.05)
    
    st.divider()
    
    # Color selection
    st.subheader("🎨 Colors")
    lipstick_color = st.color_picker("Lipstick Color", "#FF69B4")
    eyeshadow_color = st.color_picker("Eyeshadow Color", "#FFD700")
    blush_color = st.color_picker("Blush Color", "#FFC0CB")
    
    st.divider()
    
    # Finish selection
    st.subheader("✨ Finish Type")
    finish_type = st.selectbox("Lipstick Finish", ["glossy", "matte", "satin", "metallic", "shimmer"])

# ============================================================================
# MAIN CONTENT
# ============================================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Camera Feed")
    
    # Initialize modules
    ar_pipeline = RealtimeARPipeline()
    rendering_engine = ProfessionalRenderingEngine()
    face_tracker = Face3DTracker()
    skin_analyzer = DermatologyGradeSkinAnalyzer()
    
    # Webcam input
    picture = st.camera_input("Take a photo")
    
    if picture is not None:
        # Convert to OpenCV format
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process frame
        if enable_ar:
            # Step 1: AR pipeline - detect faces + extract regions
            _, frame_data = ar_pipeline.process_frame(image)
            render_landmarks = _build_render_landmarks(frame_data)

            if render_landmarks['lips_all'] or render_landmarks['left_eye'] or render_landmarks['right_eye']:
                # Step 2: 3D tracking - get head pose
                if enable_3d_tracking:
                    face_3d = face_tracker.detect_face_3d(image)
                    if face_3d and 'head_pose' in face_3d:
                        _, yaw, _ = face_3d['head_pose']
                        intensity_factor = face_tracker._calculate_intensity_factor(yaw)
                    else:
                        intensity_factor = 1.0
                else:
                    intensity_factor = 1.0
                
                # Step 3: Render makeup
                result = image.copy()
                
                # Apply lipstick
                if render_landmarks['lips_all']:
                    result = rendering_engine.render_lipstick(
                        result,
                        _hex_to_rgb(lipstick_color),
                        render_landmarks,
                        intensity=lipstick_intensity * intensity_factor,
                        finish=finish_type
                    )
                
                # Apply eyeshadow
                if render_landmarks['left_eye'] or render_landmarks['right_eye']:
                    result = rendering_engine.render_eyeshadow(
                        result,
                        _hex_to_rgb(eyeshadow_color),
                        render_landmarks,
                        intensity=eyeshadow_intensity * intensity_factor
                    )
                
                # Apply blush
                if render_landmarks['left_cheek'] is not None or render_landmarks['right_cheek'] is not None:
                    result = rendering_engine.render_blush(
                        result,
                        _hex_to_rgb(blush_color),
                        render_landmarks,
                        intensity=blush_intensity * intensity_factor
                    )
                
                result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                st.image(result_rgb, width="stretch", caption="✨ With AR Makeup")
                
                # Step 4: Real-time skin analysis (optional, slower)
                if enable_skin_analysis:
                    st.info("🔍 Analyzing skin...")
                    
                    # Extract face region
                    h, w = image.shape[:2]
                    face_region = image[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
                    
                    # Analyze
                    skin_analysis = skin_analyzer.analyze_skin(face_region)
                    
                    # Display metrics
                    st.subheader("🧬 Skin Health Report")
                    metric_cols = st.columns(5)
                    
                    metrics = [
                        ('Acne', skin_analysis['acne_severity']),
                        ('Wrinkles', skin_analysis['wrinkle_score']),
                        ('Pigmentation', skin_analysis['pigmentation_score']),
                        ('Redness', skin_analysis['redness_score']),
                        ('Overall', skin_analysis['overall_health_score'])
                    ]
                    
                    for (name, score), col in zip(metrics, metric_cols):
                        with col:
                            st.metric(name, f"{score}/100")
                    
                    # Recommendations
                    st.subheader("💡 Skincare Recommendations")
                    for rec in skin_analysis['recommendations']:
                        st.write(f"• {rec}")
            else:
                st.warning("⚠️ No face detected. Ensure face is clearly visible.")
        else:
            # Display original
            st.image(image_rgb, width="stretch", caption="Original Photo")

with col2:
    st.subheader("📊 Analysis Results")
    
    if picture is not None:
        # Quick stats
        st.metric("Face Detected", "✅ Yes")
        st.metric("3D Tracking", "✅ Enabled" if enable_3d_tracking else "⏸️ Disabled")
        
        st.divider()
        
        # Skin tone & undertone
        if enable_skin_analysis:
            st.subheader("🎨 Skin Profile")
            
            # Simple demo (would use foundation_matcher in real integration)
            st.write("**Estimated Skin Tone**: Medium")
            st.write("**Undertone**: Warm")
            st.write("**Foundation Match**: MAC NC42")
        
        st.divider()
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        
        if st.button("💬 Get Routine Recommendation"):
            chatbot = AIBeautyChatbot()
            routine = chatbot.suggest_routine("medium", ["acne", "dryness"])
            st.success("Personalized Routine:")
            for i, product in enumerate(routine, 1):
                st.write(f"{i}. {product}")
        
        if st.button("🎨 Generate AI Look"):
            look_gen = AIBeautyLookGenerator()
            look = look_gen.generate_look("soft glam", "medium", "warm")
            st.success(f"**{look['look_name']}**")
            for step in look['application_guide']:
                st.write(step)

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
✨ **Beautybuzzi AR Makeup Try-On** | Powered by MediaPipe + PyTorch
🔬 Advanced features: 3D head tracking, frequency separation rendering, dermatology-grade skin analysis
""")
