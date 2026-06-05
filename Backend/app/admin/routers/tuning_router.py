"""
Backend/app/admin/routers/tuning_router.py

API endpoints for Optuna hyperparameter tuning.
"""
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.admin.auth import require_admin
from app.admin.services.tuning_service import (
    start_tuning_job, get_job, list_jobs, cancel_job
)

router = APIRouter(
    prefix="/admin/tuning",
    tags=["Hyperparameter Tuning"],
    dependencies=[Depends(require_admin)],
)


class TuningRequest(BaseModel):
    model_type: str  = Field(..., description="lstm | gru | transformer")
    product_id: int  = Field(..., description="Product ID to tune on")
    n_trials:   int  = Field(20, ge=5, le=100, description="Number of Optuna trials")


@router.post("/start")
async def start_tuning(req: TuningRequest):
    """Start a new hyperparameter tuning job."""
    if req.model_type not in ("lstm", "gru", "transformer"):
        raise HTTPException(400, "model_type must be lstm, gru, or transformer")

    job_id = str(uuid.uuid4())[:8]
    start_tuning_job(
        job_id=job_id,
        model_type=req.model_type,
        product_id=req.product_id,
        n_trials=req.n_trials,
        db_path="./prisight.db",
    )
    return {"job_id": job_id, "status": "started", "message": f"Tuning {req.model_type} started with {req.n_trials} trials"}


@router.get("/jobs")
async def get_all_jobs():
    """List all tuning jobs."""
    return {"jobs": list_jobs()}


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get full status and results of a specific job."""
    job = get_job(job_id)
    if not job:
        raise HTTPException(404, f"Job {job_id} not found")
    return job


@router.delete("/jobs/{job_id}")
async def cancel_tuning_job(job_id: str):
    """Cancel a running tuning job."""
    success = cancel_job(job_id)
    if not success:
        raise HTTPException(400, "Job not found or not running")
    return {"job_id": job_id, "status": "cancelled"}