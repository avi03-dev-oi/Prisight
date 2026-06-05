from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.admin.services.admin_evaluation_service import AdminEvaluationService
from app.admin.schemas.admin_evaluation import (
    EvaluationCreate,
    EvaluationResponse,
    EvaluationDetailResponse,
    EvaluationSummary,
    PredictionResponse,
    ModelComparisonResponse,
    PaginatedEvaluationsResponse,
    ImportResponse,
    PredictionPoint,
    EpochHistory,
)
from app.admin.auth import require_admin


# ✅ require_admin applied to ALL routes via dependencies=
router = APIRouter(
    prefix="/admin",
    tags=["Admin Model Evaluation"],
    dependencies=[Depends(require_admin)],
)


@router.get("/evaluations", response_model=PaginatedEvaluationsResponse)
async def get_evaluations(
    model: Optional[str] = Query(None, description="Filter by model name"),
    dataset: Optional[str] = Query(None, description="Filter by dataset name"),
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    sort_by: str = Query("created_at", description="Sort by field"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of model evaluations with filtering and sorting."""
    result = await AdminEvaluationService.get_evaluations(
        db=db,
        model_name=model,
        dataset_name=dataset,
        product_id=product_id,
        start_date=start_date,
        end_date=end_date,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
    )

    return PaginatedEvaluationsResponse(
        items=[EvaluationResponse.model_validate(e) for e in result["items"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
    )


@router.get("/evaluations/{evaluation_id}", response_model=EvaluationDetailResponse)
async def get_evaluation_detail(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed evaluation including predictions and training history."""
    evaluation = await AdminEvaluationService.get_evaluation_by_id(db, evaluation_id)

    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    predictions = await AdminEvaluationService.get_predictions(db, evaluation_id)
    prediction_points = [
        PredictionPoint(
            timestep=p.timestep,
            actual_value=p.actual_value,
            predicted_value=p.predicted_value,
            residual=p.residual,
        )
        for p in predictions
    ]

    history = await AdminEvaluationService.get_training_history(db, evaluation_id)
    epoch_history = [
        EpochHistory(
            epoch=h.epoch,
            loss=h.loss,
            val_loss=h.val_loss,
            mae=h.mae,
            val_mae=h.val_mae,
        )
        for h in history
    ]

    return EvaluationDetailResponse(
    id=evaluation.id,
    model_name=evaluation.model_name,
    dataset_name=evaluation.dataset_name,
    product_id=evaluation.product_id,
    rmse=evaluation.rmse,
    mae=evaluation.mae,
    r2_score=evaluation.r2_score,
    mape=evaluation.mape,
    epochs=evaluation.epochs,
    training_time_seconds=evaluation.training_time_seconds,
    parameters_count=evaluation.parameters_count,
    window_size=evaluation.window_size,
    batch_size=evaluation.batch_size,
    learning_rate=evaluation.learning_rate,
    created_at=evaluation.created_at,
    notes=evaluation.notes,
    predictions=prediction_points,
    training_history=epoch_history,
)


@router.get("/model-comparison", response_model=ModelComparisonResponse)
async def get_model_comparison(
    db: AsyncSession = Depends(get_db),
):
    """Get model comparison data for visualization."""
    comparison = await AdminEvaluationService.get_model_comparison(db)
    return ModelComparisonResponse(**comparison)


@router.get("/model-history/{model_name}", response_model=List[EvaluationSummary])
async def get_model_history(
    model_name: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all evaluations for a specific model."""
    evaluations = await AdminEvaluationService.get_model_history(db, model_name)
    return [EvaluationSummary.model_validate(e) for e in evaluations]


@router.get("/predictions/{evaluation_id}", response_model=PredictionResponse)
async def get_predictions(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get predictions for a specific evaluation."""
    predictions = await AdminEvaluationService.get_predictions(db, evaluation_id)

    if not predictions:
        evaluation = await AdminEvaluationService.get_evaluation_by_id(db, evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return PredictionResponse(evaluation_id=evaluation_id, predictions=[])

    return PredictionResponse(
        evaluation_id=evaluation_id,
        predictions=[
            PredictionPoint(
                timestep=p.timestep,
                actual_value=p.actual_value,
                predicted_value=p.predicted_value,
                residual=p.residual,
            )
            for p in predictions
        ],
    )


@router.get("/training-history/{evaluation_id}")
async def get_training_history(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get training history for a specific evaluation."""
    history = await AdminEvaluationService.get_training_history(db, evaluation_id)

    if not history:
        evaluation = await AdminEvaluationService.get_evaluation_by_id(db, evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return {"evaluation_id": evaluation_id, "history": []}

    return {
        "evaluation_id": evaluation_id,
        "history": [
            {
                "epoch": h.epoch,
                "loss": h.loss,
                "val_loss": h.val_loss,
                "mae": h.mae,
                "val_mae": h.val_mae,
            }
            for h in history
        ],
    }


@router.get("/model-names")
async def get_model_names(db: AsyncSession = Depends(get_db)):
    """Get list of all unique model names."""
    names = await AdminEvaluationService.get_model_names(db)
    return {"model_names": names}


@router.get("/dataset-names")
async def get_dataset_names(db: AsyncSession = Depends(get_db)):
    """Get list of all unique dataset names."""
    names = await AdminEvaluationService.get_dataset_names(db)
    return {"dataset_names": names}


@router.post("/evaluations", response_model=ImportResponse)
async def create_evaluation(
    data: EvaluationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new model evaluation."""
    try:
        evaluation = await AdminEvaluationService.create_evaluation(db, data)
        return ImportResponse(
            success=True,
            message="Evaluation created successfully",
            evaluation_id=evaluation.id,
            imported_count=1,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/evaluations/with-data", response_model=ImportResponse)
async def create_evaluation_with_data(
    data: EvaluationCreate,
    predictions: Optional[List[dict]] = None,
    training_history: Optional[List[dict]] = None,
    db: AsyncSession = Depends(get_db),
):
    """Create a new model evaluation with predictions and training history."""
    try:
        evaluation = await AdminEvaluationService.create_evaluation(
            db, data, predictions, training_history
        )
        return ImportResponse(
            success=True,
            message="Evaluation created successfully",
            evaluation_id=evaluation.id,
            imported_count=1,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-import", response_model=ImportResponse)
async def bulk_import_evaluations(
    evaluations: List[EvaluationCreate],
    db: AsyncSession = Depends(get_db),
):
    """Bulk import multiple evaluations."""
    try:
        count = 0
        for eval_data in evaluations:
            await AdminEvaluationService.create_evaluation(db, eval_data)
            count += 1

        return ImportResponse(
            success=True,
            message=f"Successfully imported {count} evaluations",
            imported_count=count,
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/evaluations/{evaluation_id}")
async def delete_evaluation(
    evaluation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete an evaluation and its related data."""
    success = await AdminEvaluationService.delete_evaluation(db, evaluation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    return {"success": True, "message": "Evaluation deleted successfully"}


@router.get("/stats/summary")
async def get_stats_summary(db: AsyncSession = Depends(get_db)):
    """Get summary statistics for the dashboard."""
    comparison = await AdminEvaluationService.get_model_comparison(db)

    models = comparison.get("models", [])
    best_by_metric = comparison.get("best_by_metric", {})

    best_rmse = best_by_metric.get("rmse")
    best_mae = best_by_metric.get("mae")
    best_r2 = best_by_metric.get("r2_score")

    return {
        "total_evaluations": len(models),
        "best_model": best_rmse.model_name if best_rmse else None,
        "best_rmse": best_rmse.rmse if best_rmse else None,
        "best_mae": best_mae.mae if best_mae else None,
        "best_r2": best_r2.r2_score if best_r2 else None,
        "avg_training_time": (
            sum(m.training_time_seconds for m in models) / len(models)
            if models else 0
        ),
    }