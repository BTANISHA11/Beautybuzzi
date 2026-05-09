"""
Utility modules for makeup application, model inference, and helper functions
"""

import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import utility modules from root level
try:
    from makeup import apply_makeup_layer
    from mediapipe_makeup import (
        apply_lip_makeup,
        apply_eyeshadow_makeup,
        apply_blush_makeup,
    )
    from model import load_model
    from resnet import ResNet18
except ImportError:
    # Non-critical utilities - graceful degradation
    pass

__all__ = [
    "apply_makeup_layer",
    "apply_lip_makeup",
    "apply_eyeshadow_makeup",
    "apply_blush_makeup",
    "load_model",
    "ResNet18",
]
