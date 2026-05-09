"""
mediapipe_makeup.py — Landmark-accurate, texture-preserving makeup rendering.

Replaces the flat HSV-overlay pipeline with:
  • MediaPipe Face Mesh (468 landmarks + iris refinement)
  • CIE-LAB colour space blending — preserves skin luminance & texture
  • Gaussian-feathered soft masks for natural transitions
  • Precise polygon-based lip, eyeshadow, blush, eyeliner, highlighter
  • Beard tint using jaw-contour landmarks
  • Foundation shade matching via cheek-region LAB sampling

All functions accept/return standard RGB NumPy arrays (H×W×3 uint8).
"""

import cv2
import numpy as np

import os

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)

MEDIAPIPE_OK = False
_mp = None
_FaceLandmarker = None
_FaceLandmarkerOptions = None
_BaseOptions = None
_RunningMode = None

try:
    import mediapipe as _mp_module
    from mediapipe.tasks import python as _mp_tasks
    from mediapipe.tasks.python import vision as _mp_vision

    _mp = _mp_module
    _FaceLandmarker = _mp_vision.FaceLandmarker
    _FaceLandmarkerOptions = _mp_vision.FaceLandmarkerOptions
    _BaseOptions = _mp_tasks.BaseOptions
    _RunningMode = _mp_vision.RunningMode

    if not os.path.exists(_MODEL_PATH):
        import urllib.request
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)

    MEDIAPIPE_OK = True
except Exception:
    MEDIAPIPE_OK = False

# ── Landmark index groups (MediaPipe 468-point canonical face mesh) ────────────

LIPS_OUTER = [
    61, 185, 40, 39, 37, 0, 267, 269, 270, 409,
    291, 375, 321, 405, 314, 17, 84, 181, 91, 146,
]
LIPS_INNER = [
    78, 191, 80, 81, 82, 13, 312, 311, 310, 415,
    308, 324, 318, 402, 317, 14, 87, 178, 88, 95,
]
LEFT_EYE  = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
LEFT_BROW  = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
RIGHT_BROW = [300, 293, 334, 296, 336, 285, 295, 282, 283, 276]
LEFT_CHEEK_IDX  = 205
RIGHT_CHEEK_IDX = 425
NOSE_BRIDGE = [168, 6, 197, 195, 5]
JAW_LINE    = [172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397]
LIP_UNDER   = [17, 314, 405, 321, 375, 291, 61, 146, 91, 181, 84]

# ── Foundation shade database ──────────────────────────────────────────────────
# (name, LAB_L, LAB_A, LAB_B, hex_rgb)
FOUNDATION_SHADES = [
    ("Porcelain",     85,  2,  5, "#FDE3D0"),
    ("Ivory",         80,  4,  8, "#F5D5B8"),
    ("Fair",          74,  6, 10, "#EDBE99"),
    ("Light Beige",   68,  8, 12, "#D4A882"),
    ("Natural Beige", 62, 10, 14, "#C48B65"),
    ("Sand",          58, 11, 15, "#BC7B52"),
    ("Medium",        54, 12, 16, "#A86742"),
    ("Warm Medium",   50, 13, 17, "#9A5832"),
    ("Tan",           46, 14, 18, "#8B4A28"),
    ("Deep Tan",      42, 13, 16, "#7A3D21"),
    ("Mahogany",      38, 12, 14, "#6B3219"),
    ("Deep",          34, 11, 12, "#5C2815"),
    ("Rich",          30, 10, 10, "#4A2010"),
    ("Espresso",      26,  9,  8, "#3A1A0C"),
]


# ── Internal helpers ───────────────────────────────────────────────────────────

def _pts(lm, indices):
    """Convert landmark list (list of (x_px, y_px) tuples) to int32 array."""
    return np.array([lm[i] for i in indices], dtype=np.int32)


def _blend(image_rgb, mask_u8, color_rgb, alpha, feather):
    """
    Texture-preserving colour blend in CIE-LAB space.

    Only A + B channels (chroma) are replaced; the L channel (luminance /
    skin texture) is fully preserved. The mask is Gaussian-feathered so
    edges transition naturally without hard outlines.
    """
    k = max(1, feather) * 2 + 1
    mf = cv2.GaussianBlur(
        mask_u8.astype(np.float32) / 255.0, (k, k), 0
    ) * np.clip(alpha, 0.0, 1.0)

    lab_img = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    col_lab = cv2.cvtColor(
        np.full((1, 1, 3), color_rgb, dtype=np.uint8), cv2.COLOR_RGB2LAB
    )[0, 0].astype(np.float32)

    out = lab_img.copy()
    out[..., 1] = (1 - mf) * lab_img[..., 1] + mf * col_lab[1]  # A
    out[..., 2] = (1 - mf) * lab_img[..., 2] + mf * col_lab[2]  # B

    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)


# ── Public API ─────────────────────────────────────────────────────────────────

def get_landmarks(image_rgb):
    """
    Run MediaPipe Face Landmarker (Tasks API) on an RGB image.
    Returns list of (x_px, y_px) tuples (478 points) or None.
    """
    if not MEDIAPIPE_OK:
        return None
    try:
        h, w = image_rgb.shape[:2]
        options = _FaceLandmarkerOptions(
            base_options=_BaseOptions(model_asset_path=_MODEL_PATH),
            running_mode=_RunningMode.IMAGE,
        )
        with _FaceLandmarker.create_from_options(options) as det:
            mp_img = _mp.Image(
                image_format=_mp.ImageFormat.SRGB,
                data=np.ascontiguousarray(image_rgb),
            )
            result = det.detect(mp_img)
        if not result.face_landmarks:
            return None
        raw = result.face_landmarks[0]
        return [(int(p.x * w), int(p.y * h)) for p in raw]
    except Exception:
        return None


def apply_lipstick(image_rgb, lm, color_rgb, intensity=0.75):
    """Precise lip colouring using outer lip polygon."""
    h, w = image_rgb.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    pts = _pts(lm, LIPS_OUTER)
    cv2.fillPoly(mask, [cv2.convexHull(pts)], 255)
    # Exclude inner lip for more realistic look
    inner = _pts(lm, LIPS_INNER)
    cv2.fillPoly(mask, [cv2.convexHull(inner)], 200)   # partial keep inner
    return _blend(image_rgb, mask, color_rgb, alpha=intensity, feather=3)


def apply_eyeshadow(image_rgb, lm, color_rgb, intensity=0.45):
    """Gradient eyeshadow blended above the eyelid crease."""
    h, w = image_rgb.shape[:2]
    result = image_rgb.copy()
    for eye_idx in [LEFT_EYE, RIGHT_EYE]:
        mask = np.zeros((h, w), dtype=np.uint8)
        pts = _pts(lm, eye_idx)
        span = int((pts[:, 1].max() - pts[:, 1].min()) * 1.8)
        expanded = pts.copy()
        expanded[:, 1] -= span
        combined = cv2.convexHull(np.vstack([pts, expanded]))
        cv2.fillConvexPoly(mask, combined, 255)
        result = _blend(result, mask, color_rgb, alpha=intensity, feather=10)
    return result


def apply_blush(image_rgb, lm, color_rgb, intensity=0.38):
    """Soft elliptical blush on both cheekbones."""
    h, w = image_rgb.shape[:2]
    result = image_rgb.copy()
    left_c  = lm[LEFT_CHEEK_IDX]
    right_c = lm[RIGHT_CHEEK_IDX]
    radius = int(w * 0.088)
    for cx, cy in [left_c, right_c]:
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (cx, cy), (radius, int(radius * 0.65)), 0, 0, 360, 255, -1)
        result = _blend(result, mask, color_rgb, alpha=intensity, feather=radius // 2)
    return result


def apply_eyeliner(image_rgb, lm, color_rgb=(0, 0, 0), thickness=2, intensity=0.90):
    """Feathered eyeliner drawn along the eye contour hull."""
    h, w = image_rgb.shape[:2]
    result = image_rgb.copy()
    for eye_idx in [LEFT_EYE, RIGHT_EYE]:
        pts = _pts(lm, eye_idx)
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.drawContours(mask, [cv2.convexHull(pts)], 0, 255, max(1, thickness))
        result = _blend(result, mask, color_rgb, alpha=intensity, feather=1)
    return result


def apply_highlighter(image_rgb, lm, intensity=0.28):
    """
    Simulate highlighter on nose bridge and brow bone by boosting
    the L (luminance) channel in CIE-LAB space.
    """
    h, w = image_rgb.shape[:2]
    radius = max(6, int(w * 0.012))
    mask = np.zeros((h, w), dtype=np.uint8)
    for pt in _pts(lm, NOSE_BRIDGE):
        cv2.circle(mask, tuple(pt), radius, 255, -1)
    k = radius * 6 + 1
    mf = cv2.GaussianBlur(
        mask.astype(np.float32) / 255.0, (k, k), 0
    ) * np.clip(intensity, 0, 1)
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = np.clip(lab[..., 0] + mf * 40, 0, 255)
    return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2RGB)


def apply_beard_tint(image_rgb, lm, color_rgb, intensity=0.35):
    """
    Apply a beard/stubble tint to the jaw and chin region, excluding the lips.
    Works best with dark desaturated colours.
    """
    h, w = image_rgb.shape[:2]
    pts = np.vstack([
        _pts(lm, JAW_LINE),
        _pts(lm, LIP_UNDER),
    ])
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillConvexPoly(mask, cv2.convexHull(pts), 255)
    # Remove lip overlap
    lip_pts = _pts(lm, LIPS_OUTER)
    cv2.fillPoly(mask, [cv2.convexHull(lip_pts)], 0)
    return _blend(image_rgb, mask, color_rgb, alpha=intensity, feather=18)


def apply_brow_tint(image_rgb, lm, color_rgb, intensity=0.65):
    """Tint both eyebrows independently."""
    h, w = image_rgb.shape[:2]
    result = image_rgb.copy()
    for brow_idx in [LEFT_BROW, RIGHT_BROW]:
        mask = np.zeros((h, w), dtype=np.uint8)
        pts = _pts(lm, brow_idx)
        cv2.fillConvexPoly(mask, cv2.convexHull(pts), 255)
        result = _blend(result, mask, color_rgb, alpha=intensity, feather=2)
    return result


# ── Skin tone & foundation matching ───────────────────────────────────────────

def detect_skin_tone(image_rgb, lm):
    """
    Sample both cheek patches in CIE-LAB colour space to estimate skin tone.

    Returns
    -------
    (lab_array, rgb_array) : (np.ndarray shape (3,), np.ndarray shape (3,))
        or (None, None) if detection fails.
    """
    h, w = image_rgb.shape[:2]
    r = max(12, int(w * 0.025))
    samples = []
    for idx in [LEFT_CHEEK_IDX, RIGHT_CHEEK_IDX]:
        cx, cy = lm[idx]
        patch = image_rgb[max(0, cy - r):cy + r, max(0, cx - r):cx + r]
        if patch.size:
            samples.append(patch.reshape(-1, 3).mean(axis=0))
    if not samples:
        return None, None
    avg_rgb = np.clip(np.array(samples).mean(axis=0), 0, 255).astype(np.uint8)
    avg_lab = cv2.cvtColor(avg_rgb.reshape(1, 1, 3), cv2.COLOR_RGB2LAB)[0, 0]
    return avg_lab, avg_rgb


def match_foundation(skin_lab):
    """
    Find the three closest foundation shades by CIE-LAB Euclidean distance.

    Returns
    -------
    list of (distance, name, hex_color) — sorted best match first.
    """
    dists = []
    for name, L, A, B, hex_col in FOUNDATION_SHADES:
        d = ((skin_lab[0] - L) ** 2 + (skin_lab[1] - A) ** 2 + (skin_lab[2] - B) ** 2) ** 0.5
        dists.append((d, name, hex_col))
    dists.sort()
    return dists[:3]
