# recommend_hairstyle.py
import os
import random
import cv2
import numpy as np
import streamlit as st

HAIRSTYLE_DIR = "hairstyles"

def get_face_shape(image):
    """
    Dummy face shape detector. Replace with ML-based detection if needed.
    """
    h, w, _ = image.shape
    aspect_ratio = w / h

    if aspect_ratio > 0.9:
        return "round"
    elif aspect_ratio < 0.8:
        return "long"
    else:
        return "oval"

def recommend_hairstyle(face_shape):
    """
    Return a recommended hairstyle file based on face shape.
    You can customize this logic.
    """
    hairstyle_map = {
        "round": ["bob.png", "pixie.png"],
        "long": ["curly.png", "layered.png"],
        "oval": ["straight.png", "wavy.png"],
    }
    options = hairstyle_map.get(face_shape, [])
    if not options:
        return None
    return random.choice(options)

def apply_hairstyle_overlay(image, hairstyle_path):
    """
    Apply hairstyle overlay with alpha blending.
    """
    overlay = cv2.imread(hairstyle_path, cv2.IMREAD_UNCHANGED)
    if overlay is None:
        raise FileNotFoundError(f"Hairstyle not found: {hairstyle_path}")

    overlay = cv2.resize(overlay, (image.shape[1], image.shape[0]))
    if overlay.shape[2] == 4:
        alpha = overlay[:, :, 3] / 255.0
        for c in range(3):
            image[:, :, c] = image[:, :, c] * (1 - alpha) + overlay[:, :, c] * alpha
    return image
