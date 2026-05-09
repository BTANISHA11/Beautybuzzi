"""
AI feature modules for foundation matching, looks generation, and beauty chatbot
"""

import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import modules from root level (maintaining backward compatibility)
try:
    from foundation_matcher import AIFoundationMatcher
    from ai_generative_features import AIBeautyLookGenerator, AIBeautyChatbot
except ImportError as e:
    raise ImportError(f"Failed to import AI modules: {e}")

__all__ = [
    "AIFoundationMatcher",
    "AIBeautyLookGenerator",
    "AIBeautyChatbot",
]
