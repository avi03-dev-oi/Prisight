"""
Backend/app/admin/services/tuning_service.py
"""

import threading
import numpy as np

from datetime import datetime
from typing import Optional, Dict, Any

_jobs: Dict[str, Dict[str, Any]] = {}
_jobs_lock = threading.Lock()


def get_job(job_id: str) -> Optional[Dict]:
    return _jobs.get(job_id)


def list_jobs() -> list:
    with _jobs_lock:
        return [
            {
                "job_id": k,
                **{
                    f: v[f]
                    for f in [
                        "model_type",
                        "status",
                        "progress",
                        "n_trials",
                        "best_value",
                        "started_at",
                        "finished_at",
                    ]
                    if f in v
                },
            }
            for k, v in _jobs.items()
        ]


def cancel_job(job_id: str) -> bool:
    with _jobs_lock:
        job = _jobs.get(job_id)

        if job and job["status"] == "running":
            job["status"] = "cancelled"
            return True

    return False


def start_tuning_job(
    job_id: str,
    model_type: str,
    product_id: int,
    n_trials: int=20,
    db_path: str="./prisight.db",
):
    with _jobs_lock:
        _jobs[job_id] = {
            "job_id": job_id,
            "model_type": model_type,
            "product_id": product_id,
            "status": "running",
            "progress": 0,
            "n_trials": n_trials,
            "best_value": None,
            "best_params": None,
            "trials": [],
            "started_at": datetime.utcnow().isoformat(),
            "finished_at": None,
            "error": None,
        }

    thread = threading.Thread(
        target=_run_tuning,
        args=(
            job_id,
            model_type,
            product_id,
            n_trials,
            db_path,
        ),
        daemon=True,
    )

    thread.start()


def _run_tuning(
    job_id,
    model_type,
    product_id,
    n_trials,
    db_path,
):
    try:
        import sqlite3
        import pandas as pd
        import optuna

        optuna.logging.set_verbosity(
            optuna.logging.WARNING
        )

        conn = sqlite3.connect(db_path)

        df = pd.read_sql_query(
            """
            SELECT
                date,
                selling_price,
                units_sold,
                product_id
            FROM sales_history
            WHERE product_id = ?
            ORDER BY date
            """,
            conn,
            params=(product_id,),
        )

        conn.close()

        print(
            f"Loaded {len(df)} rows for product {product_id}"
        )

        if len(df) < 30:
            raise ValueError(
                f"Not enough data for product {product_id}. "
                f"Found {len(df)} rows."
            )

        df["date"] = pd.to_datetime(df["date"])

        df = (
            df.sort_values("date")
            .reset_index(drop=True)
        )

        df["rolling_avg_7"] = (
            df["units_sold"]
            .rolling(7, min_periods=1)
            .mean()
        )

        df["rolling_avg_14"] = (
            df["units_sold"]
            .rolling(14, min_periods=1)
            .mean()
        )

        df["rolling_avg_30"] = (
            df["units_sold"]
            .rolling(30, min_periods=1)
            .mean()
        )

        df["lag_1"] = (
            df["units_sold"]
            .shift(1)
            .fillna(0)
        )

        df["lag_7"] = (
            df["units_sold"]
            .shift(7)
            .fillna(0)
        )

        df["demand_trend"] = (
            df["units_sold"]
            .diff()
            .fillna(0)
        )

        df["is_weekend"] = (
            df["date"]
            .dt.dayofweek
            .isin([5, 6])
            .astype(int)
        )

        df["weekday_sin"] = np.sin(
            2 * np.pi * 
            df["date"].dt.dayofweek / 7
        )

        df["weekday_cos"] = np.cos(
            2 * np.pi * 
            df["date"].dt.dayofweek / 7
        )

        df["month_sin"] = np.sin(
            2 * np.pi * 
            df["date"].dt.month / 12
        )

        df["month_cos"] = np.cos(
            2 * np.pi * 
            df["date"].dt.month / 12
        )

        FEATURE_COLS = [
            "selling_price",
            "rolling_avg_7",
            "rolling_avg_14",
            "rolling_avg_30",
            "lag_1",
            "lag_7",
            "demand_trend",
            "is_weekend",
            "weekday_sin",
            "weekday_cos",
            "month_sin",
            "month_cos",
        ]

        TARGET_COL = "units_sold"

        def objective(trial):

            with _jobs_lock:
                if (
                    _jobs[job_id]["status"]
                    == "cancelled"
                ):
                    raise optuna.exceptions.TrialPruned()

            window_size = trial.suggest_categorical(
                "window_size",
                [14, 21, 28, 35, 42, 49, 56],
            )

            batch_size = trial.suggest_categorical(
                "batch_size",
                [16, 32, 64],
            )

            learning_rate = trial.suggest_float(
                "learning_rate",
                1e-4,
                1e-2,
                log=True,
            )

            dropout_rate = trial.suggest_float(
                "dropout_rate",
                0.1,
                0.4,
            )

            if model_type.lower() == "lstm":

                units_1 = trial.suggest_categorical(
                    "units_1",
                    [64, 128, 256],
                )

                units_2 = trial.suggest_categorical(
                    "units_2",
                    [32, 64, 128],
                )

                units_3 = trial.suggest_categorical(
                    "units_3",
                    [16, 32, 64],
                )

            elif model_type.lower() == "gru":

                units_1 = trial.suggest_categorical(
                    "units_1",
                    [64, 128, 256],
                )

                units_2 = trial.suggest_categorical(
                    "units_2",
                    [32, 64, 128],
                )

            elif model_type.lower() == "transformer":

                d_model = trial.suggest_categorical(
                    "d_model",
                    [16, 32, 64],
                )

                n_heads = trial.suggest_categorical(
                    "n_heads",
                    [1, 2, 4],
                )

                ff_dim = trial.suggest_categorical(
                    "ff_dim",
                    [32, 64, 128],
                )

                n_blocks = trial.suggest_int(
                    "n_blocks",
                    1,
                    3,
                )

            X = []
            y = []

            for i in range(
                len(df) - window_size
            ):
                X.append(
                    df[FEATURE_COLS]
                    .iloc[i:i + window_size]
                    .values
                )

                y.append(
                    df[TARGET_COL]
                    .iloc[i + window_size]
                )

            X = np.array(X)
            y = np.array(y)

            train_size = int(
                len(X) * 0.8
            )

            from sklearn.preprocessing import MinMaxScaler

            n_features = X.shape[2]

            scaler_x = MinMaxScaler()
            scaler_y = MinMaxScaler()

            X_train = scaler_x.fit_transform(
                X[:train_size].reshape(
                    -1,
                    n_features,
                )
            ).reshape(
                X[:train_size].shape
            )

            X_test = scaler_x.transform(
                X[train_size:].reshape(
                    -1,
                    n_features,
                )
            ).reshape(
                X[train_size:].shape
            )

            y_train = scaler_y.fit_transform(
                y[:train_size]
                .reshape(-1, 1)
            ).flatten()

            y_test = y[train_size:]

            import tensorflow as tf

            from tensorflow.keras.models import Sequential

            from tensorflow.keras.layers import (
                LSTM,
                GRU,
                Dense,
                Dropout,
            )

            from tensorflow.keras.optimizers import Adam

            from tensorflow.keras.callbacks import (
                EarlyStopping,
            )

            tf.get_logger().setLevel(
                "ERROR"
            )

            input_shape = (
                window_size,
                n_features,
            )

            if model_type.lower() == "lstm":
                model = Sequential([
                    LSTM(
                        units_1,
                        return_sequences=True,
                        input_shape=input_shape,
                    ),
                    Dropout(dropout_rate),

                    LSTM(
                        units_2,
                        return_sequences=True,
                    ),
                    Dropout(dropout_rate),

                    LSTM(units_3),
                    Dropout(dropout_rate),

                    Dense(32, activation="relu"),
                    Dense(1),
                ])

            elif model_type.lower() == "gru":
                model = Sequential([
                    GRU(
                        units_1,
                        return_sequences=True,
                        input_shape=input_shape,
                    ),
                    Dropout(dropout_rate),

                    GRU(units_2),
                    Dropout(dropout_rate),

                    Dense(32, activation="relu"),
                    Dense(1),
                ])

            elif model_type.lower() == "transformer":

                from tensorflow.keras.layers import (
                    Input,
                    LayerNormalization,
                    MultiHeadAttention,
                    GlobalAveragePooling1D,
                )

                from tensorflow.keras.models import Model

                inp = Input(shape=input_shape)

                x = inp

                for _ in range(n_blocks):

                    attn = MultiHeadAttention(
                        num_heads=n_heads,
                        key_dim=d_model,
                    )(x, x)

                    x = LayerNormalization()(x + attn)

                    ff = Dense(
                        ff_dim,
                        activation="relu",
                    )(x)

                    ff = Dense(x.shape[-1])(ff)

                    x = LayerNormalization()(x + ff)

                x = GlobalAveragePooling1D()(x)

                x = Dense(
                    32,
                    activation="relu",
                )(x)

                out = Dense(1)(x)

                model = Model(inp, out)

            model.compile(
                optimizer=Adam(
                    learning_rate
                ),
                loss="mse",
                metrics=["mae"],
            )

            early_stop = EarlyStopping(
                monitor="val_loss",
                patience=5,
                restore_best_weights=True,
            )

            model.fit(
                X_train,
                y_train,
                epochs=20,
                batch_size=batch_size,
                validation_split=0.15,
                callbacks=[early_stop],
                verbose=0,
            )

            pred_scaled = model.predict(
                X_test,
                verbose=0,
            ).flatten()

            preds = scaler_y.inverse_transform(
                pred_scaled.reshape(-1, 1)
            ).flatten()

            from sklearn.metrics import (
                mean_squared_error,
                mean_absolute_error,
                r2_score,
            )

            rmse = float(
                np.sqrt(
                    mean_squared_error(
                        y_test,
                        preds,
                    )
                )
            )

            mae = float(
                mean_absolute_error(
                    y_test,
                    preds,
                )
            )

            r2 = float(
                r2_score(
                    y_test,
                    preds,
                )
            )

            mape = float(
                np.mean(
                    np.abs(
                        (y_test - preds)
                        / (y_test + 1e-8)
                    )
                ) * 100
            )

            with _jobs_lock:
                _jobs[job_id]["trials"].append({
                    "trial_number": trial.number,
                    "rmse": round(rmse, 4),
                    "mae": round(mae, 4),
                    "r2": round(r2, 4),
                    "mape": round(mape, 2),
                    "params": dict(trial.params),
                })

                _jobs[job_id]["progress"] = int(
                    (trial.number + 1)
                    / n_trials
                    * 100
                )

            return rmse

        study = optuna.create_study(
            direction="minimize"
        )

        study.optimize(
            objective,
            n_trials=n_trials,
        )

        with _jobs_lock:
            job = _jobs[job_id]

            job["status"] = "completed"
            job["progress"] = 100
            job["best_value"] = float(
                study.best_value
            )
            job["best_params"] = (
                study.best_params
            )
            job["finished_at"] = (
                datetime.utcnow()
                .isoformat()
            )

        # ── Persist best result to leaderboard table ──
        import json

        trials = _jobs[job_id]["trials"]

        best_mae = min(
            t["mae"] for t in trials
        )

        best_r2 = max(
            t["r2"] for t in trials
        )

        best_mape = min(
            t["mape"] for t in trials
        )

        conn = sqlite3.connect(db_path)

        conn.execute(
            """
            INSERT INTO tuning_results
            (
                model_name,
                best_rmse,
                best_mae,
                best_r2,
                best_mape,
                best_params
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                model_type.upper(),
                float(study.best_value),
                best_mae,
                best_r2,
                best_mape,
                json.dumps(study.best_params),
            ),
        )

        conn.commit()
        conn.close()

    except Exception as exc:

        import traceback

        print("\n" + "=" * 80)
        print("TUNING JOB FAILED")
        print("=" * 80)

        traceback.print_exc()

        print("=" * 80)

        with _jobs_lock:

            job = _jobs.get(job_id)

            if job:
                job["status"] = "failed"
                job["error"] = str(exc)
                job["finished_at"] = (
                    datetime.utcnow()
                    .isoformat()
                )