"""
Notebook Export Utility for Model Evaluation Metrics

This module provides utilities to export model evaluation results from Jupyter notebooks
into a standardized JSON format that can be imported into the Prisight admin dashboard.

Usage in Notebooks:
    from app.ML.export_metrics import save_model_evaluation, export_evaluation

    # After training your model:
    result = save_model_evaluation(
        model_name="LSTM",
        dataset_name="Product_1_500days",
        metrics={"rmse": 4.54, "mae": 3.20, "r2": 0.63, "mape": 14.09},
        predictions={"actual": y_test, "predicted": y_pred},
        training_history={"loss": history.history['loss'], "val_loss": history.history['val_loss']},
        hyperparameters={"epochs": 300, "window_size": 30, "batch_size": 32}
    )

    # Export to file
    export_evaluation(result, filepath="my_evaluation.json")
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


# Default export directory
EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ML", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def save_model_evaluation(
    model_name: str,
    dataset_name: str,
    metrics: Dict[str, float],
    predictions: Optional[Dict[str, List[float]]] = None,
    training_history: Optional[Dict[str, List[float]]] = None,
    hyperparameters: Optional[Dict[str, Any]] = None,
    product_id: Optional[int] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a standardized evaluation export structure.

    Args:
        model_name: Name of the model (e.g., "LSTM", "GRU", "CNN-LSTM", "Transformer")
        dataset_name: Name of the dataset or product (e.g., "Product_1_500days")
        metrics: Dictionary containing evaluation metrics
            Required: rmse, mae, r2_score
            Optional: mape
        predictions: Dictionary with actual and predicted values
            Keys: "actual", "predicted" (each a list of floats)
        training_history: Dictionary with training history
            Keys: "loss", "val_loss", "mae", "val_mae" (each a list of floats)
        hyperparameters: Dictionary of model hyperparameters
            Common: epochs, window_size, batch_size, learning_rate, dropout_rate
        product_id: Optional product ID association
        notes: Optional notes about the evaluation

    Returns:
        Dictionary containing the complete evaluation data structure

    Example:
        >>> result = save_model_evaluation(
        ...     model_name="LSTM",
        ...     dataset_name="Product_1",
        ...     metrics={"rmse": 4.54, "mae": 3.20, "r2": 0.63, "mape": 14.09},
        ...     predictions={"actual": [10, 20, 15], "predicted": [11, 19, 16]},
        ...     training_history={"loss": [0.5, 0.3, 0.2], "val_loss": [0.6, 0.4, 0.3]},
        ...     hyperparameters={"epochs": 100, "window_size": 30}
        ... )
        >>> print(result["model_name"])
        'LSTM'
    """
    # Build the export structure
    export_data = {
        "metadata": {
            "export_version": "1.0",
            "export_timestamp": datetime.utcnow().isoformat(),
            "model_name": model_name,
            "dataset_name": dataset_name,
            "product_id": product_id,
        },
        "metrics": {
            "rmse": float(metrics.get("rmse", 0)),
            "mae": float(metrics.get("mae", 0)),
            "r2_score": float(metrics.get("r2_score", 0)),
            "mape": float(metrics.get("mape", 0)) if metrics.get("mape") else None,
        },
        "training": {
            "epochs": int(hyperparameters.get("epochs", 0)) if hyperparameters else 0,
            "training_time_seconds": float(hyperparameters.get("training_time_seconds", 0)) if hyperparameters else 0,
            "parameters_count": int(hyperparameters.get("parameters_count", 0)) if hyperparameters else None,
            "window_size": int(hyperparameters.get("window_size", 0)) if hyperparameters else None,
            "batch_size": int(hyperparameters.get("batch_size", 0)) if hyperparameters else None,
            "learning_rate": float(hyperparameters.get("learning_rate", 0)) if hyperparameters else None,
            "dropout_rate": float(hyperparameters.get("dropout_rate", 0)) if hyperparameters else None,
            "loss_history": [float(x) for x in training_history.get("loss", [])] if training_history else [],
            "val_loss_history": [float(x) for x in training_history.get("val_loss", [])] if training_history else [],
            "mae_history": [float(x) for x in training_history.get("mae", [])] if training_history else [],
            "val_mae_history": [float(x) for x in training_history.get("val_mae", [])] if training_history else [],
        },
        "predictions": {
            "actual": [float(x) for x in predictions.get("actual", [])] if predictions else [],
            "predicted": [float(x) for x in predictions.get("predicted", [])] if predictions else [],
        },
        "notes": notes,
    }

    return export_data


def export_evaluation(evaluation_data: Dict[str, Any], filepath: Optional[str] = None) -> str:
    """
    Export evaluation data to a JSON file.

    Args:
        evaluation_data: The evaluation data structure from save_model_evaluation()
        filepath: Optional custom filepath. If not provided, generates one automatically.

    Returns:
        Path to the exported file

    Example:
        >>> data = save_model_evaluation(model_name="LSTM", dataset_name="Product_1",
        ...     metrics={"rmse": 4.54, "mae": 3.20, "r2_score": 0.63})
        >>> filepath = export_evaluation(data)
        >>> print(filepath)
        '/path/to/app/ML/exports/lstm_product_1_20240115_120000.json'
    """
    metadata = evaluation_data.get("metadata", {})
    model_name = metadata.get("model_name", "unknown")
    dataset_name = metadata.get("dataset_name", "unknown")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if filepath is None:
        # Generate automatic filename
        safe_model = model_name.lower().replace(" ", "_")
        safe_dataset = dataset_name.lower().replace(" ", "_").replace("/", "_")
        filename = f"{safe_model}_{safe_dataset}_{timestamp}.json"
        filepath = os.path.join(EXPORT_DIR, filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Write to file
    with open(filepath, "w") as f:
        json.dump(evaluation_data, f, indent=2)

    return filepath


def load_evaluation(filepath: str) -> Dict[str, Any]:
    """
    Load evaluation data from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        Dictionary containing the evaluation data

    Example:
        >>> data = load_evaluation("/path/to/evaluation.json")
        >>> print(data["metrics"]["rmse"])
        4.54
    """
    with open(filepath, "r") as f:
        return json.load(f)


def list_exports(model_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List all evaluation exports, optionally filtered by model name.

    Args:
        model_name: Optional filter to only show exports for a specific model

    Returns:
        List of export metadata dictionaries
    """
    exports = []

    for filename in os.listdir(EXPORT_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(EXPORT_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    metadata = data.get("metadata", {})
                    if model_name is None or metadata.get("model_name", "").lower() == model_name.lower():
                        exports.append({
                            "filename": filename,
                            "filepath": filepath,
                            "model_name": metadata.get("model_name"),
                            "dataset_name": metadata.get("dataset_name"),
                            "timestamp": metadata.get("export_timestamp"),
                            "metrics": data.get("metrics", {}),
                        })
            except (json.JSONDecodeError, IOError):
                continue

    return sorted(exports, key=lambda x: x.get("timestamp", ""), reverse=True)


def get_best_model(exports: List[Dict[str, Any]], metric: str = "r2_score") -> Optional[Dict[str, Any]]:
    """
    Find the best model from a list of exports based on a metric.

    For RMSE, MAE, MAPE: lower is better
    For R2: higher is better

    Args:
        exports: List of export metadata dictionaries
        metric: Metric to optimize ("rmse", "mae", "r2_score", "mape")

    Returns:
        Best export dictionary or None if list is empty
    """
    if not exports:
        return None

    # Determine if lower is better
    lower_is_better = metric in ["rmse", "mae", "mape"]

    best = None
    best_value = float("inf") if lower_is_better else float("-inf")

    for export in exports:
        metrics = export.get("metrics", {})
        value = metrics.get(metric)

        if value is None:
            continue

        if lower_is_better:
            if value < best_value:
                best_value = value
                best = export
        else:
            if value > best_value:
                best_value = value
                best = export

    return best


def create_comparison_table(exports: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a comparison table from multiple evaluation exports.

    Args:
        exports: List of export metadata dictionaries

    Returns:
        Dictionary with model comparisons and rankings
    """
    if not exports:
        return {"models": [], "rankings": {}}

    models = []
    for export in exports:
        metadata = export.get("metadata", {})
        metrics = export.get("metrics", {})
        models.append({
            "model_name": metadata.get("model_name"),
            "dataset_name": metadata.get("dataset_name"),
            "rmse": metrics.get("rmse"),
            "mae": metrics.get("mae"),
            "r2_score": metrics.get("r2_score"),
            "mape": metrics.get("mape"),
            "export": export,
        })

    # Calculate rankings for each metric
    rankings = {}
    for metric in ["rmse", "mae", "r2_score", "mape"]:
        sorted_models = sorted(
            [m for m in models if m[metric] is not None],
            key=lambda x: x[metric],
            reverse=(metric == "r2_score"),  # Higher is better for R2
        )
        rankings[metric] = [
            {"rank": i + 1, "model_name": m["model_name"], "value": m[metric]}
            for i, m in enumerate(sorted_models)
        ]

    return {
        "models": models,
        "rankings": rankings,
        "best_by_metric": {
            "rmse": get_best_model(exports, "rmse"),
            "mae": get_best_model(exports, "mae"),
            "r2_score": get_best_model(exports, "r2_score"),
            "mape": get_best_model(exports, "mape"),
        },
    }