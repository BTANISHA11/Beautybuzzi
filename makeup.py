import cv2
import numpy as np
from skimage.filters import gaussian
from test import evaluate

def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, channel_axis=-1)
    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img
    img_out = np.clip(img_out / 255.0, 0, 1) * 255
    return np.array(img_out, dtype=np.uint8)

def apply_makeup(image, parsing, part=17, color=[230, 50, 20]):
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part in [12, 13]:  # lips
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    elif part in [14]:  # eyeliner
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    elif part in [15]:  # eyeshadow
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    elif part in [16]:  # blush
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]
    else:
        image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    if part == 17:  # hair
        changed = sharpen(changed)

    changed[parsing != part] = image[parsing != part]
    return changed

def apply_region_blend(image, mask, color, alpha=0.4):
    color_layer = np.full_like(image, color, dtype=np.uint8)
    blended = cv2.addWeighted(image, 1 - alpha, color_layer, alpha, 0)
    output = image.copy()
    output[mask] = blended[mask]
    return output