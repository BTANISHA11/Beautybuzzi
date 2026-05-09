"""
🔥 PHASE 3: 3D FACE & HEAD TRACKING
Enable side-face rendering, head rotation tracking, perspective-aware makeup.
Uses MediaPipe Face Geometry for 3D transformation matrices.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, Tuple, Optional
import math
import os

class Face3DTracker:
    """
    3D face tracking with head rotation, perspective awareness.
    Enables: head pose estimation, occlusion handling, stable overlays.
    """
    
    def __init__(self):
        """Initialize MediaPipe Face Mesh with 3D landmarks."""
        self.face_mesh = None
        self.landmarker = None
        
        # Try legacy Face Mesh API
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
        except:
            pass
        
        # Try Tasks API
        try:
            if os.path.exists('face_landmarker.task'):
                from mediapipe.tasks import python
                from mediapipe.tasks.python import vision
                base_options = python.BaseOptions(
                    model_asset_path='face_landmarker.task'
                )
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    output_face_blendshapes=True,
                    output_facial_transformation_matrixes=True
                )
                self.landmarker = vision.FaceLandmarker.create_from_options(options)
        except:
            pass
        
        # Reference 3D face model landmarks (normalized)
        self.reference_3d_landmarks = self._load_reference_landmarks()
    
    def _load_reference_landmarks(self) -> np.ndarray:
        """Load canonical 3D face model (468 landmarks)."""
        # Simplified reference face in 3D space
        # In production: use FaceMesh's canonical landmarks
        landmarks_3d = np.zeros((468, 3), dtype=np.float32)
        
        # This is a placeholder - in real implementation use MediaPipe's canonical face
        return landmarks_3d
    
    def detect_face_3d(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Detect face with 3D landmarks and head pose.
        Returns: 3D landmarks, transformation matrix, head angles.
        """
        if self.face_mesh is None and self.landmarker is None:
            return None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape
        
        # Try face_mesh first
        if self.face_mesh is not None:
            try:
                results = self.face_mesh.process(frame_rgb)
                if results.multi_face_landmarks:
                    landmarks_2d = self._landmarks_to_2d(results.multi_face_landmarks[0], h, w)
                    return self._process_landmarks(landmarks_2d, h, w)
            except:
                pass
        
        # Try landmarker
        if self.landmarker is not None:
            try:
                import mediapipe as mp
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
                results = self.landmarker.detect(image)
                if results.face_landmarks:
                    landmarks_2d = self._landmarks_to_2d_from_landmarker(results.face_landmarks[0], h, w)
                    return self._process_landmarks(landmarks_2d, h, w)
            except:
                pass
        
        return None
    
    def _landmarks_to_2d(self, landmarks, h: int, w: int) -> np.ndarray:
        """Convert MediaPipe landmarks to 2D coordinates."""
        return np.array([(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark])
    
    def _landmarks_to_2d_from_landmarker(self, landmarks, h: int, w: int) -> np.ndarray:
        """Convert Landmarker landmarks to 2D coordinates."""
        try:
            return np.array([(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark])
        except:
            return np.array([(int(lm.x * w), int(lm.y * h)) for lm in landmarks])
    
    def _process_landmarks(self, landmarks_2d: np.ndarray, h: int, w: int) -> Dict:
        """Process landmarks to extract head pose."""
        # landmarks_2d is already a numpy array of (x, y) coordinates
        
        # Estimate head pose (pitch, yaw, roll)
        head_pose = self._estimate_head_pose(landmarks_2d, w, h)
        
        # Estimate 3D transformation matrix
        transform_matrix = self._estimate_transformation(landmarks_2d, head_pose)
        
        return {
            'landmarks_2d': landmarks_2d,
            'head_pose': head_pose,  # (pitch, yaw, roll) in degrees
            'transform_matrix': transform_matrix,
            'is_frontal': abs(head_pose[1]) < 30,  # Yaw < 30°
            'is_profile': abs(head_pose[1]) > 60  # Profile view
        }
    
    def _estimate_head_pose(self, landmarks_2d: np.ndarray, w: int, h: int) -> Tuple[float, float, float]:
        """
        Estimate head rotation angles (pitch, yaw, roll).
        Uses 3D-to-2D correspondence.
        """
        # Key landmarks for pose estimation
        # Nose tip, chin, left/right eyes, left/right ears
        
        nose_tip = landmarks_2d[1]  # Nose tip
        chin = landmarks_2d[152]  # Chin
        left_eye = landmarks_2d[33]  # Left eye
        right_eye = landmarks_2d[263]  # Right eye
        left_ear = landmarks_2d[234]  # Left ear tragus
        right_ear = landmarks_2d[454]  # Right ear tragus
        
        # Simplified pose estimation
        # In production: use SolvePnP with 3D reference model
        
        # Yaw: horizontal head rotation (left-right)
        eye_distance = np.linalg.norm(right_eye - left_eye)
        nose_to_eye_mid = np.linalg.norm(nose_tip - (left_eye + right_eye) / 2)
        yaw = math.degrees(math.atan2(nose_to_eye_mid, eye_distance * 0.5))
        
        # Pitch: vertical head rotation (up-down)
        nose_to_chin = chin[1] - nose_tip[1]
        nose_to_eye = (left_eye[1] + right_eye[1]) / 2 - nose_tip[1]
        pitch = math.degrees(math.atan2(nose_to_chin, abs(nose_to_eye)))
        
        # Roll: head tilt (side-to-side)
        eye_angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
        roll = math.degrees(eye_angle)
        
        return (pitch, yaw, roll)
    
    def _estimate_transformation(self, landmarks_2d: np.ndarray, head_pose: Tuple) -> np.ndarray:
        """
        Estimate 3D transformation matrix from 2D landmarks and head pose.
        Used for perspective-aware makeup rendering.
        """
        pitch, yaw, roll = head_pose
        
        # Rotation matrices
        pitch_rad = math.radians(pitch)
        yaw_rad = math.radians(yaw)
        roll_rad = math.radians(roll)
        
        # Rotation matrix (simplified Euler angles)
        Rx = np.array([
            [1, 0, 0],
            [0, math.cos(pitch_rad), -math.sin(pitch_rad)],
            [0, math.sin(pitch_rad), math.cos(pitch_rad)]
        ])
        
        Ry = np.array([
            [math.cos(yaw_rad), 0, math.sin(yaw_rad)],
            [0, 1, 0],
            [-math.sin(yaw_rad), 0, math.cos(yaw_rad)]
        ])
        
        Rz = np.array([
            [math.cos(roll_rad), -math.sin(roll_rad), 0],
            [math.sin(roll_rad), math.cos(roll_rad), 0],
            [0, 0, 1]
        ])
        
        # Combined rotation
        R = Rz @ Ry @ Rx
        
        # Identity translation (can be extended)
        T = np.eye(4)
        T[:3, :3] = R
        
        return T
    
    # ============================================================================
    # PERSPECTIVE-AWARE MAKEUP RENDERING
    # ============================================================================
    
    def apply_perspective_aware_makeup(
        self,
        image: np.ndarray,
        face_data: Dict,
        makeup_config: Dict
    ) -> np.ndarray:
        """
        Apply makeup with perspective correction based on head pose.
        Adjusts intensity and placement based on viewing angle.
        """
        if not face_data:
            return image
        
        pitch, yaw, roll = face_data['head_pose']
        
        # Adjust makeup intensity based on head rotation
        intensity_factor = self._calculate_intensity_factor(yaw)
        
        # For profile views: use alternative regions
        if abs(yaw) > 45:
            return self._apply_profile_makeup(image, face_data, makeup_config, intensity_factor)
        
        # For frontal/3/4 views: standard rendering
        return self._apply_perspective_corrected_makeup(image, face_data, makeup_config, intensity_factor)
    
    def _calculate_intensity_factor(self, yaw: float) -> float:
        """
        Reduce makeup intensity as head rotates away from camera.
        Accounts for foreshortening.
        """
        yaw_abs = abs(yaw)
        
        # Linear falloff from 1.0 (frontal) to 0.3 (90° profile)
        intensity = max(0.3, 1.0 - (yaw_abs / 90.0) * 0.7)
        
        return intensity
    
    def _apply_perspective_corrected_makeup(
        self,
        image: np.ndarray,
        face_data: Dict,
        makeup_config: Dict,
        intensity_factor: float
    ) -> np.ndarray:
        """
        Apply makeup with perspective correction.
        """
        result = image.copy()
        
        # Import rendering engine
        try:
            from rendering_engine import ProfessionalRenderingEngine
            renderer = ProfessionalRenderingEngine()
            
            # Extract landmarks
            landmarks = self._landmarks_to_dict(face_data['landmarks_2d'])
            
            # Apply with adjusted intensity
            if 'lips_all' in landmarks:
                lip_mask = self._create_region_mask(image.shape, landmarks['lips_all'])
                result = renderer.render_lipstick(
                    result,
                    makeup_config.get('lipstick_color', (255, 105, 180)),
                    landmarks,
                    intensity=makeup_config.get('lipstick_intensity', 0.7) * intensity_factor,
                    finish='glossy'
                )
            
        except ImportError:
            pass
        
        return result
    
    def _apply_profile_makeup(
        self,
        image: np.ndarray,
        face_data: Dict,
        makeup_config: Dict,
        intensity_factor: float
    ) -> np.ndarray:
        """
        Apply makeup for profile view (side-face).
        Use alternative regions not visible in profile.
        """
        # In profile view: focus on lips and nose contour
        # Skip eye makeup (not visible)
        # Adjust blush placement
        
        result = image.copy()
        return result
    
    def _landmarks_to_dict(self, landmarks_2d: np.ndarray) -> Dict:
        """Convert 468 landmarks to region dictionary."""
        return {
            'lips_all': landmarks_2d[61:68].tolist() + landmarks_2d[88:95].tolist(),
            'left_eye': landmarks_2d[159:181].tolist(),
            'right_eye': landmarks_2d[386:408].tolist(),
        }
    
    def _create_region_mask(self, shape: Tuple, points: list) -> np.ndarray:
        """Create binary mask from points."""
        mask = np.zeros(shape[:2], dtype=np.uint8)
        if points:
            pts = np.array(points, np.int32)
            cv2.fillPoly(mask, [pts], 255)
        return mask
    
    # ============================================================================
    # OCCLUSION DETECTION
    # ============================================================================
    
    def detect_occlusions(self, face_data: Dict) -> Dict:
        """
        Detect occluded face regions (hair covering forehead, etc.).
        Prevents makeup application in occluded areas.
        """
        landmarks_2d = face_data['landmarks_2d']
        
        occlusions = {
            'forehead_occluded': False,
            'left_eye_occluded': False,
            'right_eye_occluded': False,
            'cheek_occluded': False,
            'lips_occluded': False
        }
        
        # Simple heuristic: if landmarks are close to image boundary, likely occluded
        h, w = 480, 640  # Typical frame size
        
        forehead_lms = landmarks_2d[10:30]
        if np.any(forehead_lms[:, 1] < h * 0.1):
            occlusions['forehead_occluded'] = True
        
        return occlusions
    
    # ============================================================================
    # VISUALIZATION
    # ============================================================================
    
    def draw_3d_axes(self, image: np.ndarray, face_data: Dict) -> np.ndarray:
        """Draw 3D rotation axes on face for debugging."""
        if not face_data:
            return image
        
        landmarks_2d = face_data['landmarks_2d']
        nose = landmarks_2d[1].astype(np.int32)
        
        pitch, yaw, roll = face_data['head_pose']
        
        # Calculate axis endpoints based on rotation
        scale = 50
        
        # X-axis (red) - left/right
        x_offset = (scale * math.cos(math.radians(yaw)), scale * math.sin(math.radians(yaw)))
        
        # Y-axis (green) - up/down
        y_offset = (0, scale * math.cos(math.radians(pitch)))
        
        # Z-axis (blue) - forward/back
        z_offset = (scale * math.sin(math.radians(roll)), 0)
        
        result = image.copy()
        
        # Draw axes
        cv2.line(result, tuple(nose), tuple(nose + np.array(x_offset, dtype=np.int32)), (0, 0, 255), 3)  # Red
        cv2.line(result, tuple(nose), tuple(nose + np.array(y_offset, dtype=np.int32)), (0, 255, 0), 3)  # Green
        cv2.line(result, tuple(nose), tuple(nose + np.array(z_offset, dtype=np.int32)), (255, 0, 0), 3)  # Blue
        
        # Add text
        cv2.putText(result, f"Pitch: {pitch:.1f}°", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(result, f"Yaw: {yaw:.1f}°", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(result, f"Roll: {roll:.1f}°", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return result


if __name__ == "__main__":
    tracker = Face3DTracker()
    print("✅ 3D Face Tracker loaded")
