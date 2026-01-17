import uuid
import os
import threading
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from ai_models import generate_ad_image
from auth import verify_api_key
from storage import upload_image_to_s3

app = FastAPI(title="AI Ad Generator API (Async + S3)")

# In-memory job store (MVP)
JOBS = {}

os.makedirs("outputs", exist_ok=True)

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

Composition rules:
The composition must be centered and balanced, with generous empty space around all edges.
The main subject must be fully visible and not cropped.
No important elements should touch the image borders.

Product:
{req.product}

Person:
{req.persona}

Scene:
{req.scene}

Interaction:
The person is clearly {req.interaction} the product using their right hand.
The product is clearly visible and recognizable.

Emotion:
{req.emotion}

Visual style:
{req.visual_style}

Text placement:
A short, stylish headline is placed in the upper third of the image,
fully visible, not touching the edges, with clear spacing above and below.

Photography rules:
- Professional advertising photography
- Natural human posture
- No extra fingers
- No distorted hands
- No cropped heads, hands, or text
"""



# -----------------------------
# BACKGROUND WORKER
# -----------------------------
def process_job(job_id: str, req: AdRequest):
    try:
        prompt = build_prompt(req)

        image = generate_ad_image(prompt)

        local_path = f"outputs/ad_{job_id}.png"
        image.save(local_path)

        s3_key = f"ads/ad_{job_id}.png"
        image_url = upload_image_to_s3(local_path, s3_key)

        os.remove(local_path)

        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["image_url"] = image_url
        JOBS[job_id]["prompt_used"] = prompt

    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)


# -----------------------------
# CREATE AD (FAST)
# -----------------------------
@app.post("/generate-ad")
def generate_ad(
    req: AdRequest,
    _: str = Depends(verify_api_key)
):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "processing",
        "image_url": None
    }

    thread = threading.Thread(
        target=process_job,
        args=(job_id, req)
    )
    thread.start()

    return {
        "job_id": job_id,
        "status": "processing"
    }


# -----------------------------
# CHECK STATUS
# -----------------------------
@app.get("/status/{job_id}")
def check_status(
    job_id: str,
    _: str = Depends(verify_api_key)
):
    if job_id not in JOBS:
        return {"error": "Job not found"}

    return JOBS[job_id]
