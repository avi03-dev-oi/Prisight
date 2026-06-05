from sqlalchemy import Column, Integer, Float, String, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base


class AdminModelEvaluation(Base):
    """
    Stores model evaluation metrics for all ML models.
    Supports comparison across LSTM, GRU, CNN-LSTM, CNN-GRU, Transformer, etc.
    """
    __tablename__ = "admin_model_evaluations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Model Identification
    model_name = Column(String(50), nullable=False)  # LSTM, GRU, CNN-LSTM, CNN-GRU, Transformer
    dataset_name = Column(String(100), nullable=False)  # Product name or dataset identifier
    product_id = Column(Integer, nullable=True)  # Optional product association

    # Core Evaluation Metrics
    rmse = Column(Float, nullable=False)  # Root Mean Squared Error
    mae = Column(Float, nullable=False)  # Mean Absolute Error
    r2_score = Column(Float, nullable=False)  # Coefficient of Determination
    mape = Column(Float, nullable=True)  # Mean Absolute Percentage Error (%)

    # Training Information
    epochs = Column(Integer, nullable=False)
    training_time_seconds = Column(Float, nullable=False)
    parameters_count = Column(Integer, nullable=True)  # Total trainable parameters

    # Hyperparameters
    window_size = Column(Integer, nullable=True)
    batch_size = Column(Integer, nullable=True)
    learning_rate = Column(Float, nullable=True)
    dropout_rate = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)

    # Relationships
    predictions = "AdminModelPrediction"  # Forward reference for SQLAlchemy
    training_history = "AdminTrainingHistory"  # Forward reference for SQLAlchemy

    def __repr__(self):
        return f"<AdminModelEvaluation(id={self.id}, model={self.model_name}, rmse={self.rmse}, r2={self.r2_score})>"

    def to_dict(self):
        """Convert model to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "product_id": self.product_id,
            "rmse": self.rmse,
            "mae": self.mae,
            "r2_score": self.r2_score,
            "mape": self.mape,
            "epochs": self.epochs,
            "training_time_seconds": self.training_time_seconds,
            "parameters_count": self.parameters_count,
            "window_size": self.window_size,
            "batch_size": self.batch_size,
            "learning_rate": self.learning_rate,
            "dropout_rate": self.dropout_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "notes": self.notes,
        }

    def to_summary_dict(self):
        """Lightweight dictionary for list views."""
        return {
            "id": self.id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "rmse": self.rmse,
            "mae": self.mae,
            "r2_score": self.r2_score,
            "mape": self.mape,
            "epochs": self.epochs,
            "training_time_seconds": self.training_time_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }