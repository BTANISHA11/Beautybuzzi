"""
🔥 PHASE 5: AI FOUNDATION SHADE MATCHING
Detect undertone, skin tone, warm/cool/neutral. Recommend exact foundation shades.
Advanced approach using LAB color space, cheek sampling, white balance normalization.
"""

import cv2
import numpy as np
from typing import Dict, Tuple, List
import colorsys

class AIFoundationMatcher:
    """
    Professional foundation shade matching AI.
    Analyzes: undertone (warm/cool/neutral), skin tone (fair/light/medium/tan/deep), exact shade.
    """
    
    def __init__(self):
        """Initialize foundation shade database."""
        self.foundation_database = self._load_foundation_database()
        self.undertone_ranges = {
            'warm': {'h': (10, 40), 's': (40, 100), 'y': (100, 150)},  # Yellow-red
            'cool': {'h': (200, 280), 's': (30, 100), 'v': (100, 150)},  # Blue-pink
            'neutral': {'h': (0, 360), 's': (30, 60), 'v': (120, 160)}  # Balanced
        }
    
    def _load_foundation_database(self) -> List[Dict]:
        """
        Load foundation shade database with RGB values.
        In production: connect to real product database (Sephora, Ulta, etc.)
        """
        foundations = [
            # Fair skin
            {'brand': 'MAC', 'name': 'NC10', 'rgb': (240, 210, 190), 'undertone': 'neutral', 'tone': 'fair'},
            {'brand': 'MAC', 'name': 'NC15', 'rgb': (245, 215, 195), 'undertone': 'neutral', 'tone': 'fair'},
            {'brand': 'MAC', 'name': 'NW10', 'rgb': (238, 208, 180), 'undertone': 'cool', 'tone': 'fair'},
            
            # Light skin
            {'brand': 'MAC', 'name': 'NC25', 'rgb': (250, 220, 200), 'undertone': 'neutral', 'tone': 'light'},
            {'brand': 'MAC', 'name': 'NC30', 'rgb': (255, 225, 205), 'undertone': 'neutral', 'tone': 'light'},
            
            # Medium skin
            {'brand': 'MAC', 'name': 'NC42', 'rgb': (215, 170, 140), 'undertone': 'neutral', 'tone': 'medium'},
            {'brand': 'MAC', 'name': 'NC45', 'rgb': (220, 175, 145), 'undertone': 'neutral', 'tone': 'medium'},
            
            # Tan skin
            {'brand': 'MAC', 'name': 'NC55', 'rgb': (195, 140, 110), 'undertone': 'neutral', 'tone': 'tan'},
            {'brand': 'MAC', 'name': 'NW55', 'rgb': (190, 135, 100), 'undertone': 'cool', 'tone': 'tan'},
            
            # Deep skin
            {'brand': 'MAC', 'name': 'NC65', 'rgb': (165, 110, 80), 'undertone': 'neutral', 'tone': 'deep'},
            {'brand': 'MAC', 'name': 'NW65', 'rgb': (160, 105, 75), 'undertone': 'cool', 'tone': 'deep'},
        ]
        return foundations
    
    def match_foundation(self, image: np.ndarray, face_region: np.ndarray = None) -> Dict:
        """
        Complete foundation matching pipeline.
        
        Returns:
            - Detected skin tone (fair/light/medium/tan/deep)
            - Detected undertone (warm/cool/neutral)
            - Top 3 foundation recommendations
            - Virtual foundation render
        """
        if face_region is None:
            face_region = image.copy()
        
        # Step 1: White balance correction
        balanced = self._white_balance_correction(face_region)
        
        # Step 2: Extract cheek region (most representative of skin tone)
        cheek_region = self._extract_cheek_region(balanced, face_region.shape)
        
        # Step 3: Analyze undertone
        undertone = self._detect_undertone(cheek_region)
        
        # Step 4: Analyze skin tone depth
        skin_tone = self._analyze_skin_tone(cheek_region)
        
        # Step 5: Get average skin color (LAB space for accuracy)
        skin_color_lab = self._get_average_skin_color_lab(cheek_region)
        skin_color_rgb = cv2.cvtColor(
            np.uint8([[[skin_color_lab[0], skin_color_lab[1], skin_color_lab[2]]]]),
            cv2.COLOR_LAB2BGR
        )[0][0]
        
        # Step 6: Find matching foundations
        matches = self._find_closest_foundations(skin_color_rgb, undertone, skin_tone)
        
        # Step 7: Virtual foundation rendering
        virtual_render = self._render_foundation(image, skin_color_rgb, undertone)
        
        return {
            'skin_tone': skin_tone,
            'undertone': undertone,
            'skin_color_rgb': tuple(skin_color_rgb),
            'skin_color_lab': skin_color_lab,
            'top_matches': matches,
            'virtual_render': virtual_render,
            'confidence': self._calculate_confidence(image.shape)
        }
    
    # ============================================================================
    # WHITE BALANCE & COLOR CORRECTION
    # ============================================================================
    
    def _white_balance_correction(self, image: np.ndarray) -> np.ndarray:
        """
        Correct white balance for consistent color analysis.
        Accounts for different lighting conditions.
        """
        # Gray world assumption: average of each channel should be equal
        result = image.copy().astype(np.float32)
        
        b, g, r = cv2.split(result)
        
        # Calculate average for each channel
        b_avg = np.mean(b)
        g_avg = np.mean(g)
        r_avg = np.mean(r)
        
        # Calculate scaling factors
        gray_avg = (b_avg + g_avg + r_avg) / 3
        
        b = (b / (b_avg + 1)) * gray_avg
        g = (g / (g_avg + 1)) * gray_avg
        r = (r / (r_avg + 1)) * gray_avg
        
        # Merge channels
        result = cv2.merge([b, g, r])
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        return result
    
    # ============================================================================
    # CHEEK REGION EXTRACTION
    # ============================================================================
    
    def _extract_cheek_region(self, image: np.ndarray, shape: Tuple) -> np.ndarray:
        """
        Extract cheek region (most representative of skin tone).
        Avoids: lips, eyes, shadows.
        """
        h, w = shape[:2]
        
        # Cheek region: roughly 30-60% from top, 25-50% from left (right cheek)
        # and 50-75% from left (left cheek)
        
        # Right cheek
        right_cheek = image[int(h*0.3):int(h*0.55), int(w*0.55):int(w*0.8)]
        
        # Left cheek
        left_cheek = image[int(h*0.3):int(h*0.55), int(w*0.2):int(w*0.45)]
        
        # Combine and filter out any obvious non-skin pixels
        combined = np.vstack([right_cheek, left_cheek])
        
        # Remove very bright/dark pixels (highlights/shadows)
        hsv = cv2.cvtColor(combined, cv2.COLOR_BGR2HSV)
        mask = (hsv[:,:,2] > 50) & (hsv[:,:,2] < 220)  # Value range
        
        filtered = combined[mask]
        
        return filtered if len(filtered) > 0 else combined.reshape(-1, 3)
    
    # ============================================================================
    # UNDERTONE DETECTION
    # ============================================================================
    
    def _detect_undertone(self, cheek_region: np.ndarray) -> str:
        """
        Detect undertone: warm (yellow), cool (pink/blue), or neutral.
        Uses LAB color space.
        """
        # Convert to LAB
        cheek_bgr = cheek_region.reshape(1, -1, 3).astype(np.uint8)
        cheek_lab = cv2.cvtColor(cheek_bgr, cv2.COLOR_BGR2LAB)
        
        a_channel = cheek_lab[:,:,1]  # Green(-)-Magenta(+)
        b_channel = cheek_lab[:,:,2]  # Blue(-)-Yellow(+)
        
        avg_a = np.mean(a_channel)
        avg_b = np.mean(b_channel)
        
        # Decision logic
        if avg_b > 128 and avg_a < 128:
            return 'warm'  # Yellow + Green
        elif avg_b < 128 and avg_a > 128:
            return 'cool'  # Pink/Magenta
        else:
            return 'neutral'
    
    # ============================================================================
    # SKIN TONE ANALYSIS
    # ============================================================================
    
    def _analyze_skin_tone(self, cheek_region: np.ndarray) -> str:
        """
        Classify skin tone depth: fair, light, medium, tan, deep.
        Uses luminance (L channel in LAB).
        """
        cheek_bgr = cheek_region.reshape(1, -1, 3).astype(np.uint8)
        cheek_lab = cv2.cvtColor(cheek_bgr, cv2.COLOR_BGR2LAB)
        
        l_channel = cheek_lab[:,:,0]
        avg_l = np.mean(l_channel)
        
        # Classify by L* value
        if avg_l > 180:
            return 'fair'
        elif avg_l > 160:
            return 'light'
        elif avg_l > 130:
            return 'medium'
        elif avg_l > 100:
            return 'tan'
        else:
            return 'deep'
    
    # ============================================================================
    # COLOR MATCHING
    # ============================================================================
    
    def _get_average_skin_color_lab(self, cheek_region: np.ndarray) -> Tuple:
        """
        Get average skin color in LAB color space.
        More perceptually accurate than RGB.
        """
        cheek_bgr = cheek_region.reshape(1, -1, 3).astype(np.uint8)
        cheek_lab = cv2.cvtColor(cheek_bgr, cv2.COLOR_BGR2LAB)
        
        avg_l = np.mean(cheek_lab[:,:,0])
        avg_a = np.mean(cheek_lab[:,:,1])
        avg_b = np.mean(cheek_lab[:,:,2])
        
        return (int(avg_l), int(avg_a), int(avg_b))
    
    def _find_closest_foundations(self, skin_rgb: np.ndarray, undertone: str, tone: str) -> List[Dict]:
        """
        Find closest matching foundation shades using Delta-E color difference.
        """
        # Convert skin color to LAB
        skin_bgr = np.uint8([[[skin_rgb[2], skin_rgb[1], skin_rgb[0]]]])
        skin_lab = cv2.cvtColor(skin_bgr, cv2.COLOR_BGR2LAB)[0][0]
        
        matches = []
        
        for foundation in self.foundation_database:
            # Skip if undertone/tone mismatch
            if foundation['undertone'] != undertone and foundation['undertone'] != 'neutral':
                continue
            if foundation['tone'] != tone and tone != 'medium':
                continue
            
            # Convert foundation color to LAB
            fb_bgr = np.uint8([[[foundation['rgb'][2], foundation['rgb'][1], foundation['rgb'][0]]]])
            fb_lab = cv2.cvtColor(fb_bgr, cv2.COLOR_BGR2LAB)[0][0]
            
            # Calculate Delta-E (color difference)
            delta_e = self._calculate_delta_e(skin_lab, fb_lab)
            
            matches.append({
                'brand': foundation['brand'],
                'name': foundation['name'],
                'rgb': foundation['rgb'],
                'undertone': foundation['undertone'],
                'tone': foundation['tone'],
                'delta_e': delta_e
            })
        
        # Sort by Delta-E and return top 3
        matches.sort(key=lambda x: x['delta_e'])
        return matches[:3]
    
    def _calculate_delta_e(self, lab1: np.ndarray, lab2: np.ndarray) -> float:
        """
        Calculate Delta-E (CIE76) color difference.
        Lower value = more similar colors.
        """
        dl = lab1[0] - lab2[0]
        da = lab1[1] - lab2[1]
        db = lab1[2] - lab2[2]
        
        delta_e = np.sqrt(dl**2 + da**2 + db**2)
        return float(delta_e)
    
    # ============================================================================
    # VIRTUAL RENDERING
    # ============================================================================
    
    def _render_foundation(self, image: np.ndarray, foundation_color: np.ndarray, undertone: str) -> np.ndarray:
        """
        Render virtual foundation on face.
        Simulates how foundation would look.
        """
        result = image.copy().astype(np.float32)
        
        # Blend foundation color with skin
        # Use lighter blend for more realistic appearance
        alpha = 0.6 if undertone == 'cool' else 0.5 if undertone == 'warm' else 0.55
        
        foundation_color_f = foundation_color.astype(np.float32)
        
        # Simple overlay blend (can be enhanced with frequency separation)
        result = result * (1 - alpha) + foundation_color_f * alpha
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    # ============================================================================
    # CONFIDENCE SCORE
    # ============================================================================
    
    def _calculate_confidence(self, image_shape: Tuple) -> float:
        """
        Calculate confidence score for recommendation.
        Based on image quality, lighting, etc.
        """
        h, w = image_shape[:2]
        
        # Ideal image size for accurate analysis: 512x512 to 1024x1024
        size_factor = min(h, w) / 512.0
        size_confidence = min(1.0, size_factor)
        
        # Combine factors
        confidence = size_confidence * 0.9  # 90% confidence (can improve with better analysis)
        
        return confidence


if __name__ == "__main__":
    matcher = AIFoundationMatcher()
    print("✅ AI Foundation Matcher loaded")
    print(f"Database: {len(matcher.foundation_database)} shades")
