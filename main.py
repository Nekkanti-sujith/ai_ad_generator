import uuid
import os
import threading
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from ai_models import generate_ad_image
from auth import verify_api_key

app = FastAPI(title="AI Ad Generator API (Async)")

os.makedirs("outputs", exist_ok=True)

# -----------------------------------
# IN-MEMORY JOB STORE (MVP)
# -----------------------------------
JOBS = {}

# -----------------------------------
# REQUEST SCHEMA
# -----------------------------------
class AdRequest(BaseModel):
    product: str
    persona: str
    scene: str
    interaction: str
    emotion: str
    visual_style: str
    tagline: str

# -----------------------------------
# PROMPT BUILDER
# -----------------------------------
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

# -----------------------------------
# BACKGROUND WORKER
# -----------------------------------
def process_job(job_id: str, req: AdRequest):
    try:
        prompt = build_prompt(req)
        image = generate_ad_image(prompt)

        filename = f"ad_{job_id}.png"
        output_path = os.path.join("outputs", filename)
        image.save(output_path)

        JOBS[job_id]["status"] = "completed"
        JOBS[job_id]["image_path"] = output_path
        JOBS[job_id]["prompt_used"] = prompt

    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)

# -----------------------------------
# CREATE AD (FAST RESPONSE)
# -----------------------------------
@app.post("/generate-ad")
def generate_ad(
    req: AdRequest,
    _: str = Depends(verify_api_key)
):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "processing",
        "image_path": None
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

# -----------------------------------
# CHECK STATUS
# -----------------------------------
@app.get("/status/{job_id}")
def check_status(
    job_id: str,
    _: str = Depends(verify_api_key)
):
    if job_id not in JOBS:
        return {"error": "Job not found"}

    return JOBS[job_id]
