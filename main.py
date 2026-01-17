from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uuid
import os

from ai_models import generate_ad_image
from auth import verify_api_key

app = FastAPI(title="AI Ad Generator API")

# -----------------------------
# REQUEST SCHEMA
# -----------------------------
class AdRequest(BaseModel):
    product: str
    persona: str
    scene: str
    interaction: str
    emotion: str
    visual_style: str
    tagline: str


# -----------------------------
# PROMPT BUILDER
# -----------------------------
def build_prompt(req: AdRequest) -> str:
    return f"""
High-quality lifestyle advertising photograph.

Product:
{req.product}

Person:
{req.persona}

Scene:
{req.scene}

Interaction:
Person is {req.interaction} the product using their right hand.

Emotion:
{req.emotion}

Visual style:
{req.visual_style}

Text on image:
Stylish, modern, italic headline reading "{req.tagline}" placed at the top.

Rules:
- Photorealistic
- Professional advertising photography
- Natural human posture
- No extra fingers
- No distorted hands
"""


# -----------------------------
# API ENDPOINT
# -----------------------------
@app.post("/generate-ad")
def generate_ad(
    req: AdRequest,
    _: str = Depends(verify_api_key)
):
    prompt = build_prompt(req)

    image = generate_ad_image(prompt)

    os.makedirs("outputs", exist_ok=True)
    filename = f"ad_{uuid.uuid4()}.png"
    output_path = os.path.join("outputs", filename)

    image.save(output_path)

    return {
        "status": "success",
        "image_path": output_path,
        "prompt_used": prompt
    }
