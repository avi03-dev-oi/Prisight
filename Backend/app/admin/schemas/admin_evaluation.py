from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    """Schema for creating a new model evaluation."""
    model_name: str = Field(..., max_length=50, description="Model name (e.g., LSTM, GRU, Transformer)")
    dataset_name: str = Field(..., max_length=100, description="Dataset or product name")
    product_id: Optional[int] = Field(None, description="Optional product ID")

    # Core Metrics
    rmse: float = Field(..., gt=0, description="Root Mean Squared Error")
    mae: float = Field(..., gt=0, description="Mean Absolute Error")
    r2_score: float = Field(..., ge=0, le=1, description="R² Score (0-1)")
    mape: Optional[float] = Field(None, ge=0, le=100, description="MAPE percentage")

    # Training Info
    epochs: int = Field(..., gt=0, description="Number of training epochs")
    training_time_seconds: float = Field(..., gt=0, description="Training time in seconds")
    parameters_count: Optional[int] = Field(None, gt=0, description="Total trainable parameters")

    # Hyperparameters
    window_size: Optional[int] = Field(None, gt=0, description="Sequence window size")
    batch_size: Optional[int] = Field(None, gt=0, description="Batch size")
    learning_rate: Optional[float] = Field(None, gt=0, description="Learning rate")
    dropout_rate: Optional[float] = Field(None, ge=0, le=1, description="Dropout rate")

    # Additional
    notes: Optional[str] = Field(None, description="Optional notes")


class PredictionPoint(BaseModel):
    """Schema for a single prediction point."""
    timestep: int = Field(..., ge=0, description="Index in test set")
    actual_value: float = Field(..., description="Ground truth value")
    predicted_value: float = Field(..., description="Model prediction")
    residual: float = Field(..., description="Actual - Predicted")


class EpochHistory(BaseModel):
    """Schema for training history at a single epoch."""
    epoch: int = Field(..., ge=0, description="Epoch number")
    loss: float = Field(..., description="Training loss")
    val_loss: Optional[float] = Field(None, description="Validation loss")
    mae: Optional[float] = Field(None, description="Training MAE")
    val_mae: Optional[float] = Field(None, description="Validation MAE")


class EvaluationResponse(BaseModel):
    """Lightweight response for list views."""
    id: int
    model_name: str
    dataset_name: str
    product_id: Optional[int]
    rmse: float
    mae: float
    r2_score: float
    mape: Optional[float]
    epochs: int
    training_time_seconds: float
    created_at: datetime

    class Config:
        from_attributes = True


class EvaluationDetailResponse(BaseModel):
    """Full evaluation detail response."""
    id: int
    model_name: str
    dataset_name: str
    product_id: Optional[int]

    # Metrics
    rmse: float
    mae: float
    r2_score: float
    mape: Optional[float]

    # Training Info
    epochs: int
    training_time_seconds: float
    parameters_count: Optional[int]

    # Hyperparameters
    window_size: Optional[int]
    batch_size: Optional[int]
    learning_rate: Optional[float]
    dropout_rate: Optional[float] = None

    # Metadata
    created_at: datetime
    notes: Optional[str]

    # Related data (loaded separately via API)
    predictions: List[PredictionPoint] = []
    training_history: List[EpochHistory] = []

    class Config:
        from_attributes = True


class EvaluationSummary(BaseModel):
    """Summary for model history views."""
    id: int
    model_name: str
    dataset_name: str
    rmse: float
    mae: float
    r2_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class ModelComparisonItem(BaseModel):
    """Item for model comparison table."""
    model_name: str
    dataset_name: str
    rmse: float
    mae: float
    r2_score: float
    mape: Optional[float]
    epochs: int
    training_time_seconds: float
    parameters_count: Optional[int]
    best_for: Optional[str] = None  # Which metric this model is best at


class ModelComparisonResponse(BaseModel):
    """Response for model comparison endpoint."""
    models: List[ModelComparisonItem]
    best_by_metric: dict
    rankings: dict


class PaginatedEvaluationsResponse(BaseModel):
    """Paginated response for evaluations list."""
    items: List[EvaluationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ImportResponse(BaseModel):
    """Response for import operations."""
    success: bool
    message: str
    evaluation_id: Optional[int] = None
    imported_count: int = 0


class PredictionResponse(BaseModel):
    """Response for predictions endpoint."""
    evaluation_id: int
    predictions: List[PredictionPoint]


class TrainingHistoryResponse(BaseModel):
    """Response for training history endpoint."""
    evaluation_id: int
    history: List[EpochHistory]


class EvaluationFilters(BaseModel):
    """Filter parameters for listing evaluations."""
    model_name: Optional[str] = None
    dataset_name: Optional[str] = None
    product_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"
