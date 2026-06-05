from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class AdminTrainingHistory(Base):
    """
    Stores training history (loss, val_loss, mae, val_mae) per epoch.
    Enables visualization of training convergence and overfitting.
    """
    __tablename__ = "admin_training_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    evaluation_id = Column(Integer, ForeignKey("admin_model_evaluations.id"), nullable=False)

    epoch = Column(Integer, nullable=False)
    loss = Column(Float, nullable=False)
    val_loss = Column(Float, nullable=True)
    mae = Column(Float, nullable=True)
    val_mae = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AdminTrainingHistory(id={self.id}, eval_id={self.evaluation_id}, epoch={self.epoch})>"

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "evaluation_id": self.evaluation_id,
            "epoch": self.epoch,
            "loss": self.loss,
            "val_loss": self.val_loss,
            "mae": self.mae,
            "val_mae": self.val_mae,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }