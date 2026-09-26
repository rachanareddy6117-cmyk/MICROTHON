from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

SAMPLE_CATEGORIES = ("crypto_assets", "findings", "firewall_events", "repositories")
SEED_PATH = Path(__file__).resolve().parents[1] / "demo_samples.json"
DATABASE_PATH = Path(
    os.getenv(
        "PQC_SAMPLE_DB_PATH",
        str(Path(__file__).resolve().parents[2] / "data" / "pqc_demo_samples.sqlite3"),
    )
)


def _connect() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_sample_database() -> None:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sample_records (
                category TEXT NOT NULL,
                record_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                PRIMARY KEY (category, record_id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sample_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        seeded = connection.execute(
            "SELECT value FROM sample_metadata WHERE key = 'seed_version'"
        ).fetchone()
        if seeded:
            return
        for category in SAMPLE_CATEGORIES:
            for index, record in enumerate(seed.get(category, []), start=1):
                record_id = str(record.get("id", f"{category}-{index}"))
                connection.execute(
                    "INSERT INTO sample_records(category, record_id, payload) VALUES (?, ?, ?)",
                    (category, record_id, json.dumps(record, separators=(",", ":"))),
                )
        connection.execute(
            "INSERT INTO sample_metadata(key, value) VALUES (?, ?)",
            ("seed_version", "2026.09.26.1"),
        )
        connection.execute(
            "INSERT INTO sample_metadata(key, value) VALUES (?, ?)",
            ("notice", seed["notice"]),
        )


def list_sample_data() -> dict[str, Any]:
    initialize_sample_database()
    with _connect() as connection:
        result: dict[str, Any] = {}
        for category in SAMPLE_CATEGORIES:
            rows = connection.execute(
                "SELECT payload FROM sample_records WHERE category = ? ORDER BY record_id",
                (category,),
            ).fetchall()
            result[category] = [json.loads(row["payload"]) for row in rows]
        notice = connection.execute(
            "SELECT value FROM sample_metadata WHERE key = 'notice'"
        ).fetchone()
        result["notice"] = notice["value"] if notice else "Synthetic demonstration data."
        result["database"] = "isolated SQLite sample database"
        return result
