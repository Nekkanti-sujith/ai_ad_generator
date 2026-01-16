"""
controlnet_utils.py

Responsibilities:
- Load a pose reference image
- Convert it into an OpenPose map for ControlNet
- No scene logic, no branding, no AI creativity here
"""

from PIL import Image
from controlnet_aux import OpenposeDetector

# -------------------------------------------------
# LOAD OPENPOSE DETECTOR
# -------------------------------------------------
# This model is lightweight and public
openpose = OpenposeDetector.from_pretrained(
    "lllyasviel/ControlNet"
)

# -------------------------------------------------
# LOAD POSE TEMPLATE IMAGE
# -------------------------------------------------
def load_pose_image(
    path: str,
    size=(768, 768)
) -> Image.Image:
    """
    Load and resize pose reference image.

    Args:
        path: Path to pose image (PNG/JPG)
        size: Target resolution for SDXL

    Returns:
        PIL.Image
    """
    return Image.open(path).convert("RGB").resize(size) 


# -------------------------------------------------
# GENERATE OPENPOSE MAP
# -------------------------------------------------
def generate_pose_map(
    pose_image: Image.Image
) -> Image.Image:
    """
    Generate OpenPose control map from pose image.

    Args:
        pose_image: PIL.Image pose reference

    Returns:
        PIL.Image (pose map)
    """
    pose_map = openpose(pose_image)
    return pose_map
