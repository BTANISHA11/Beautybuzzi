"""
Beautybuzzi - AI-Powered Beauty & Grooming Platform
Core module package
"""

__version__ = "1.0.0"
__author__ = "Beautybuzzi Team"

from src.core import realtime_ar, rendering_engine, face_3d_tracker, skin_analysis
from src.ai import foundation_matcher, generative_features

__all__ = [
    "realtime_ar",
    "rendering_engine",
    "face_3d_tracker",
    "skin_analysis",
    "foundation_matcher",
    "generative_features",
]
