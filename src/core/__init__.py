"""
Core AI modules for real-time face detection, rendering, tracking, and skin analysis
"""

import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import modules from root level (maintaining backward compatibility)
try:
    from realtime_ar import RealtimeARPipeline
    from rendering_engine import ProfessionalRenderingEngine
    from face_3d_tracker import Face3DTracker
    from skin_analysis_v2 import DermatologyGradeSkinAnalyzer
except ImportError as e:
    raise ImportError(f"Failed to import core modules: {e}")

__all__ = [
    "RealtimeARPipeline",
    "ProfessionalRenderingEngine",
    "Face3DTracker",
    "DermatologyGradeSkinAnalyzer",
]
