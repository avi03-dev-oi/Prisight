"""
Backend/app/admin/routers/leaderboard_router.py
"""

import json
import sqlite3

from fastapi import APIRouter, Query

router = APIRouter()


def _get_conn(db_path: str = "./prisight.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/admin/tuning/leaderboard")
def get_leaderboard(
    db_path: str = Query(
        default="./prisight.db",
        include_in_schema=False,
    ),
):
    """
    Return all tuning results sorted by best_rmse ascending.
    Each row includes parsed best_params as a dict.
    """
    conn = _get_conn(db_path)

    rows = conn.execute(
        """
        SELECT
            id,
            model_name,
            best_rmse,
            best_mae,
            best_r2,
            best_mape,
            best_params,
            created_at
        FROM tuning_results
        ORDER BY best_rmse ASC
        """
    ).fetchall()

    conn.close()

    result = []

    for rank, row in enumerate(rows, start=1):
        entry = dict(row)

        # Parse JSON params string → dict
        try:
            entry["best_params"] = json.loads(
                entry["best_params"] or "{}"
            )
        except (json.JSONDecodeError, TypeError):
            entry["best_params"] = {}

        entry["rank"] = rank

        result.append(entry)

    return result


@router.delete("/admin/tuning/leaderboard/{record_id}")
def delete_leaderboard_entry(
    record_id: int,
    db_path: str = Query(
        default="./prisight.db",
        include_in_schema=False,
    ),
):
    """
    Delete a specific leaderboard entry by id.
    Useful for clearing stale/test runs.
    """
    conn = _get_conn(db_path)

    deleted = conn.execute(
        "DELETE FROM tuning_results WHERE id = ?",
        (record_id,),
    ).rowcount

    conn.commit()
    conn.close()

    if deleted == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"Record {record_id} not found.",
        )

    return {"deleted": record_id}


@router.delete("/admin/tuning/leaderboard")
def clear_leaderboard(
    db_path: str = Query(
        default="./prisight.db",
        include_in_schema=False,
    ),
):
    """
    Clear all leaderboard entries.
    Useful for resetting before a fresh round of tuning.
    """
    conn = _get_conn(db_path)

    conn.execute("DELETE FROM tuning_results")

    conn.commit()
    conn.close()

    return {"message": "Leaderboard cleared."}