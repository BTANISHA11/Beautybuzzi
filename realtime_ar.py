import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import streamlit as st
from typing import Tuple, Dict, List
import time
import os

class RealtimeARPipeline:
    """
    Live webcam AR rendering with 468 MediaPipe landmarks.
    Enables: precise lipstick, eyeshadow, blush, beard simulation.
    """
    
    def __init__(self):
        """Initialize MediaPipe Face Mesh detector."""
        # Try new Tasks API first, fall back to legacy if needed
        self.face_mesh = None
        self.landmarker = None
        
        # Try loading face landmarker task (MediaPipe Tasks API)
        try:
            if os.path.exists('face_landmarker.task'):
                base_options = python.BaseOptions(
                    model_asset_path='face_landmarker.task'
                )
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    output_face_blendshapes=True,
                    output_facial_transformation_matrixes=True
                )
                self.landmarker = vision.FaceLandmarker.create_from_options(options)
        except Exception as e:
            pass
        
        # Fall back to legacy Face Mesh API
        try:
            if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'face_mesh'):
                mp_face_mesh = mp.solutions.face_mesh
                self.face_mesh = mp_face_mesh.FaceMesh(
                    static_image_mode=False,
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.7,
                    min_tracking_confidence=0.7
                )
        except Exception as e:
            # If legacy API not available, will use basic detection
            pass
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Process single video frame with face detection.
        Returns: frame, landmarks dict
        """
        if self.face_mesh is None and self.landmarker is None:
            return frame, {}
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape
        
        # Try using landmarker first
        if self.landmarker is not None:
            try:
                import mediapipe as mp
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                results = self.landmarker.detect(image)
                if results.face_landmarks:
                    landmarks_dict = self._extract_face_regions_from_landmarker(results.face_landmarks[0], h, w)
                    return frame, landmarks_dict
            except:
                pass
        
        # Fall back to face_mesh
        if self.face_mesh is not None:
            try:
                results = self.face_mesh.process(frame_rgb)
                if not results.multi_face_landmarks:
                    return frame, {}
                
                landmarks = results.multi_face_landmarks[0]
                landmarks_dict = self._extract_face_regions(landmarks, h, w)
                return frame, landmarks_dict
            except:
                pass
        
        return frame, {}
    
    def _extract_face_regions(self, landmarks, h: int, w: int) -> Dict:
        """
        Extract critical face regions from 468 landmarks.
        Returns: Dict with lip, eyeshadow, blush, beard regions.
        """
        lms = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]
        
        return {
            # Lip contours (indices 61-68, 88-95)
            'lips_upper': lms[61:68],
            'lips_lower': lms[88:95],
            'lips_all': lms[61:68] + lms[88:95],
            
            # Eyes & eyeshadow (left: 159-181, right: 386-408)
            'left_eye': lms[159:181],
            'right_eye': lms[386:408],
            'left_eyelids': lms[163:167],
            'right_eyelids': lms[390:394],
            
            # Cheeks & blush (cheekbone regions)
            'left_cheek': lms[50],  # Left cheekbone
            'right_cheek': lms[280],  # Right cheekbone
            
            # Nose & face contour
            'nose': lms[168:195],
            
            # Face outline (jawline, chin)
            'face_outline': lms[10],
            'jaw_left': lms[200],
            'jaw_right': lms[420],
            
            # Facial hair region (for beard simulation)
            'facial_hair_zone': lms[164:190],
            
            # Head pose estimation
            'all_landmarks': lms
        }
    
    def _extract_face_regions_from_landmarker(self, landmarks, h: int, w: int) -> Dict:
        """
        Extract critical face regions from MediaPipe Landmarker results.
        Returns: Dict with lip, eyeshadow, blush, beard regions.
        """
        # landmarks is a NormalizedLandmarkList
        lms = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark] if hasattr(landmarks, 'landmark') else []
        
        if not lms:
            return {}
        
        return {
            # Lip contours (indices 61-68, 88-95)
            'lips_upper': lms[61:68] if len(lms) > 68 else [],
            'lips_lower': lms[88:95] if len(lms) > 95 else [],
            'lips_all': (lms[61:68] if len(lms) > 68 else []) + (lms[88:95] if len(lms) > 95 else []),
            
            # Eyes & eyeshadow (left: 159-181, right: 386-408)
            'left_eye': lms[159:181] if len(lms) > 181 else [],
            'right_eye': lms[386:408] if len(lms) > 408 else [],
            'left_eyelids': lms[163:167] if len(lms) > 167 else [],
            'right_eyelids': lms[390:394] if len(lms) > 394 else [],
            
            # Cheeks & blush
            'left_cheek': lms[50] if len(lms) > 50 else None,
            'right_cheek': lms[280] if len(lms) > 280 else None,
            
            # Face outline
            'nose': lms[168:195] if len(lms) > 195 else [],
            'face_outline': lms[10] if len(lms) > 10 else None,
            'jaw_left': lms[200] if len(lms) > 200 else None,
            'jaw_right': lms[420] if len(lms) > 420 else None,
            
            # Facial hair region
            'facial_hair_zone': lms[164:190] if len(lms) > 190 else [],
            
            # All landmarks
            'all_landmarks': lms
        }
    
    def get_fps(self, frame_time: float) -> float:
        """Calculate frames per second."""
        return 1.0 / frame_time if frame_time > 0 else 0


class RealtimeWebcamApp:
    """Streamlit-based real-time webcam AR viewer."""
    
    def __init__(self):
        self.ar_pipeline = RealtimeARPipeline()
        self.makeup_state = {
            'lipstick_color': (255, 105, 180),  # Hot pink
            'lipstick_intensity': 0.7,
            'eyeshadow_color': (200, 100, 200),  # Purple
            'eyeshadow_intensity': 0.6,
            'blush_color': (255, 150, 150),  # Peach
            'blush_intensity': 0.5,
            'eyeliner_enabled': True,
            'beard_color': (60, 40, 20),
            'beard_density': 0.0
        }
    
    def run(self):
        """Main Streamlit app for real-time AR."""
        st.set_page_config(page_title="🪞 Real-Time Beauty AR", layout="wide")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.title("🪞 Real-Time Makeup AR")
            st.subheader("Live Webcam Try-On with 468 Face Landmarks")
            
            # Placeholder for video
            video_placeholder = st.empty()
            fps_placeholder = st.empty()
        
        with col2:
            st.subheader("🎨 Makeup Controls")
            
            self.makeup_state['lipstick_intensity'] = st.slider(
                "💄 Lipstick Intensity", 0.0, 1.0, 0.7
            )
            
            self.makeup_state['eyeshadow_intensity'] = st.slider(
                "✨ Eyeshadow Intensity", 0.0, 1.0, 0.6
            )
            
            self.makeup_state['blush_intensity'] = st.slider(
                "🎀 Blush Intensity", 0.0, 1.0, 0.5
            )
            
            self.makeup_state['eyeliner_enabled'] = st.checkbox(
                "✏️ Eyeliner", value=True
            )
            
            if st.checkbox("👨 Beard Mode (For Men)"):
                self.makeup_state['beard_density'] = st.slider(
                    "Beard Density", 0.0, 1.0, 0.5
                )
            
            start_webcam = st.button("▶️ Start Webcam", key="start_webcam")
        
        if start_webcam:
            self._run_webcam_stream(video_placeholder, fps_placeholder)
    
    def _run_webcam_stream(self, video_placeholder, fps_placeholder):
        """Run live webcam stream."""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not cap.isOpened():
            st.error("❌ Cannot access webcam")
            return
        
        stop_button = st.button("⏹️ Stop", key="stop_webcam")
        frame_count = 0
        fps_smoothed = 0
        
        while cap.isOpened() and not stop_button:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Mirror effect
            start_time = time.time()
            
            # Process frame
            frame_proc, landmarks = self.ar_pipeline.process_frame(frame)
            
            # TODO: Apply makeup rendering here (Phase 2)
            if landmarks:
                frame_proc = self._draw_landmarks(frame_proc, landmarks)
            
            # FPS calculation
            frame_time = time.time() - start_time
            fps = 1.0 / frame_time if frame_time > 0 else 0
            fps_smoothed = 0.7 * fps_smoothed + 0.3 * fps
            
            # Display
            frame_rgb = cv2.cvtColor(frame_proc, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame_rgb, use_column_width=True)
            fps_placeholder.metric("FPS", f"{fps_smoothed:.1f}")
            
            frame_count += 1
        
        cap.release()
        st.success(f"✅ Processed {frame_count} frames")
    
    def _draw_landmarks(self, frame, landmarks: Dict) -> np.ndarray:
        """Draw face landmarks on frame (debug visualization)."""
        h, w = frame.shape[:2]
        
        # Draw lips
        if 'lips_all' in landmarks:
            pts = np.array(landmarks['lips_all'], np.int32)
            cv2.polylines(frame, [pts], True, (255, 0, 255), 2)
        
        # Draw eye regions
        if 'left_eye' in landmarks:
            pts = np.array(landmarks['left_eye'], np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 255), 1)
        
        if 'right_eye' in landmarks:
            pts = np.array(landmarks['right_eye'], np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 255), 1)
        
        # Draw face outline
        if 'face_outline' in landmarks:
            pt = landmarks['face_outline']
            cv2.circle(frame, pt, 5, (0, 255, 0), -1)
        
        return frame


if __name__ == "__main__":
    app = RealtimeWebcamApp()
    app.run()
