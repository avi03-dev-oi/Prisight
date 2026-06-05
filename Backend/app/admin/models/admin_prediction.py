from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class AdminModelPrediction(Base):
    """
    Stores actual vs predicted values for each evaluation.
    Enables visualization of prediction quality over the test set.
    """
    __tablename__ = "admin_model_predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    evaluation_id = Column(Integer, ForeignKey("admin_model_evaluations.id"), nullable=False)

    timestep = Column(Integer, nullable=False)  # Index in test set (0, 1, 2, ...)
    actual_value = Column(Float, nullable=False)  # Ground truth
    predicted_value = Column(Float, nullable=False)  # Model prediction
    residual = Column(Float, nullable=False)  # actual - predicted
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AdminModelPrediction(id={self.id}, eval_id={self.evaluation_id}, timestep={self.timestep})>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "timestep": self.timestep,
            "actual_value": self.actual_value,
            "predicted_value": self.predicted_value,
            "residual": self.residual,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }