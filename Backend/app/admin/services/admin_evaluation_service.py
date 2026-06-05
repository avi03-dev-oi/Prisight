from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc, asc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.admin.models.admin_model_evaluation import AdminModelEvaluation
from app.admin.models.admin_prediction import AdminModelPrediction
from app.admin.models.admin_training_history import AdminTrainingHistory
from app.admin.schemas.admin_evaluation import (
    EvaluationCreate,
    ModelComparisonItem,
)


class AdminEvaluationService:
    """Service for managing model evaluations."""

    @staticmethod
    async def create_evaluation(
        db: AsyncSession,
        data: EvaluationCreate,
        predictions: Optional[List[Dict[str, float]]] = None,
        training_history: Optional[List[Dict[str, float]]] = None,
    ) -> AdminModelEvaluation:
        """
        Create a new model evaluation with optional predictions and training history.

        Args:
            db: Database session
            data: Evaluation data
            predictions: Optional list of prediction points
            training_history: Optional list of epoch history

        Returns:
            Created AdminModelEvaluation instance
        """
        evaluation = AdminModelEvaluation(
            model_name=data.model_name,
            dataset_name=data.dataset_name,
            product_id=data.product_id,
            rmse=data.rmse,
            mae=data.mae,
            r2_score=data.r2_score,
            mape=data.mape,
            epochs=data.epochs,
            training_time_seconds=data.training_time_seconds,
            parameters_count=data.parameters_count,
            window_size=data.window_size,
            batch_size=data.batch_size,
            learning_rate=data.learning_rate,
            dropout_rate=data.dropout_rate,
            notes=data.notes,
        )

        db.add(evaluation)
        await db.flush()  # Get the evaluation ID

        # Add predictions if provided
        if predictions:
            for i, pred in enumerate(predictions):
                prediction = AdminModelPrediction(
                    evaluation_id=evaluation.id,
                    timestep=pred.get("timestep", i),
                    actual_value=pred["actual_value"],
                    predicted_value=pred["predicted_value"],
                    residual=pred["actual_value"] - pred["predicted_value"],
                )
                db.add(prediction)

        # Add training history if provided
        if training_history:
            for epoch_data in training_history:
                history = AdminTrainingHistory(
                    evaluation_id=evaluation.id,
                    epoch=epoch_data["epoch"],
                    loss=epoch_data["loss"],
                    val_loss=epoch_data.get("val_loss"),
                    mae=epoch_data.get("mae"),
                    val_mae=epoch_data.get("val_mae"),
                )
                db.add(history)

        await db.commit()
        await db.refresh(evaluation)

        return evaluation

    @staticmethod
    async def get_evaluations(
        db: AsyncSession,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        product_id: Optional[int] = None,
        start_date=None,
        end_date=None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """
        Get paginated evaluations with optional filtering.

        Args:
            db: Database session
            model_name: Filter by model name
            dataset_name: Filter by dataset name
            product_id: Filter by product ID
            start_date: Filter by start date
            end_date: Filter by end date
            sort_by: Field to sort by
            sort_order: "asc" or "desc"
            page: Page number (1-indexed)
            page_size: Items per page

        Returns:
            Dictionary with items, total, page, page_size, total_pages
        """
        # Build filters
        conditions = []
        if model_name:
            conditions.append(AdminModelEvaluation.model_name.ilike(f"%{model_name}%"))
        if dataset_name:
            conditions.append(AdminModelEvaluation.dataset_name.ilike(f"%{dataset_name}%"))
        if product_id is not None:
            conditions.append(AdminModelEvaluation.product_id == product_id)
        if start_date:
            conditions.append(AdminModelEvaluation.created_at >= start_date)
        if end_date:
            conditions.append(AdminModelEvaluation.created_at <= end_date)

        # Build query
        query = select(AdminModelEvaluation)
        if conditions:
            query = query.where(and_(*conditions))

        # Get total count
        count_query = select(AdminModelEvaluation)
        if conditions:
            count_query = count_query.where(and_(*conditions))
        result = await db.execute(count_query)
        total = len(result.scalars().all())

        # Apply sorting
        sort_column = getattr(AdminModelEvaluation, sort_by, AdminModelEvaluation.created_at)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Apply pagination
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await db.execute(query)
        evaluations = result.scalars().all()

        # Calculate pagination info
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        return {
            "items": evaluations,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    @staticmethod
    async def get_evaluation_by_id(db: AsyncSession, evaluation_id: int):
        result = await db.execute(
            select(AdminModelEvaluation).where(AdminModelEvaluation.id == evaluation_id)
        )
        return result.scalars().first()

    @staticmethod
    async def get_model_comparison(db: AsyncSession) -> Dict[str, Any]:
        """
        Get all evaluations for model comparison.

        Args:
            db: Database session

        Returns:
            Dictionary with models list, best_by_metric, and rankings
        """
        query = select(AdminModelEvaluation).order_by(
            AdminModelEvaluation.created_at.desc()
        )
        result = await db.execute(query)
        evaluations = result.scalars().all()

        if not evaluations:
            return {"models": [], "best_by_metric": {}, "rankings": {}}

        # Group by model_name and get best (lowest RMSE) for each
        model_best: Dict[str, AdminModelEvaluation] = {}
        for eval in evaluations:
            key = eval.model_name
            if key not in model_best or eval.rmse < model_best[key].rmse:
                model_best[key] = eval

        # Build comparison items
        models = []
        for model_name, eval in sorted(model_best.items(), key=lambda x: x[1].rmse):
            item = ModelComparisonItem(
                model_name=model_name,
                dataset_name=eval.dataset_name,
                rmse=eval.rmse,
                mae=eval.mae,
                r2_score=eval.r2_score,
                mape=eval.mape,
                epochs=eval.epochs,
                training_time_seconds=eval.training_time_seconds,
                parameters_count=eval.parameters_count,
            )
            models.append(item)

        # Find best by each metric
        best_by_metric = {
            "rmse": min(models, key=lambda x: x.rmse),
            "mae": min(models, key=lambda x: x.mae),
            "r2_score": max(models, key=lambda x: x.r2_score),
            "mape": min(models, key=lambda x: x.mape) if any(x.mape for x in models) else None,
        }

        # Calculate rankings
        rankings = {
            "rmse": sorted(models, key=lambda x: x.rmse),
            "mae": sorted(models, key=lambda x: x.mae),
            "r2_score": sorted(models, key=lambda x: x.r2_score, reverse=True),
            "mape": sorted(models, key=lambda x: x.mape) if any(x.mape for x in models) else [],
        }

        return {
            "models": models,
            "best_by_metric": best_by_metric,
            "rankings": rankings,
        }

    @staticmethod
    async def get_model_history(
        db: AsyncSession,
        model_name: str,
    ) -> List[AdminModelEvaluation]:
        """
        Get all evaluations for a specific model.

        Args:
            db: Database session
            model_name: Model name to filter by

        Returns:
            List of AdminModelEvaluation instances
        """
        query = (
            select(AdminModelEvaluation)
            .where(AdminModelEvaluation.model_name.ilike(f"%{model_name}%"))
            .order_by(AdminModelEvaluation.created_at.desc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_predictions(
        db: AsyncSession,
        evaluation_id: int,
    ) -> List[AdminModelPrediction]:
        """
        Get all predictions for an evaluation.

        Args:
            db: Database session
            evaluation_id: Evaluation ID

        Returns:
            List of AdminModelPrediction instances
        """
        query = (
            select(AdminModelPrediction)
            .where(AdminModelPrediction.evaluation_id == evaluation_id)
            .order_by(AdminModelPrediction.timestep)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_training_history(
        db: AsyncSession,
        evaluation_id: int,
    ) -> List[AdminTrainingHistory]:
        """
        Get training history for an evaluation.

        Args:
            db: Database session
            evaluation_id: Evaluation ID

        Returns:
            List of AdminTrainingHistory instances
        """
        query = (
            select(AdminTrainingHistory)
            .where(AdminTrainingHistory.evaluation_id == evaluation_id)
            .order_by(AdminTrainingHistory.epoch)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def delete_evaluation(
        db: AsyncSession,
        evaluation_id: int,
    ) -> bool:
        """
        Delete an evaluation and its related data.

        Args:
            db: Database session
            evaluation_id: Evaluation ID

        Returns:
            True if deleted, False if not found
        """
        evaluation = await AdminEvaluationService.get_evaluation_by_id(db, evaluation_id)
        if not evaluation:
            return False

        # Delete related records first (cascade would handle this if configured)
        await db.delete(evaluation)
        await db.commit()
        return True

    @staticmethod
    async def get_model_names(db: AsyncSession) -> List[str]:
        """Get list of all unique model names."""
        query = select(AdminModelEvaluation.model_name).distinct()
        result = await db.execute(query)
        return [row[0] for row in result.all()]

    @staticmethod
    async def get_dataset_names(db: AsyncSession) -> List[str]:
        """Get list of all unique dataset names."""
        query = select(AdminModelEvaluation.dataset_name).distinct()
        result = await db.execute(query)
        return [row[0] for row in result.all()]