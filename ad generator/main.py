from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import os

from prompts import build_image_prompt
from ai_models import generate_ad_image

app = FastAPI(title="AI Ad Generator – OpenAI Only")


class AdRequest(BaseModel):
    product: str
    persona: str
    scene: str
    interaction: str   # "holding" | "drinking"
    emotion: str
    visual_style: str
    tagline: str


@app.post("/generate-ad")
def generate_ad(req: AdRequest):

    prompt = build_image_prompt(
        product=req.product,
        persona=req.persona,
        scene=req.scene,
        interaction=req.interaction,
        emotion=req.emotion,
        visual_style=req.visual_style,
        tagline=req.tagline
    )

    image = generate_ad_image(prompt)

    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/ad_{uuid.uuid4()}.png"
    image.save(output_path)

    return {
        "image_path": output_path,
        "prompt_used": prompt
    }
