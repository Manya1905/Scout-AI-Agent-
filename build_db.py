import sqlite3
import json
from pathlib import Path

conn = sqlite3.connect("scout.db")

conn.execute("DROP TABLE IF EXISTS Calls")
conn.execute("""
CREATE TABLE Calls (
    call_id INTEGER PRIMARY KEY,
    run_id  TEXT,
    turn    INTEGER,
    started_at  TEXT,
    ended_at    TEXT,
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    stop_reason     TEXT
)
""")

conn.execute("DROP TABLE IF EXISTS Runs")
conn.execute("""
CREATE TABLE Runs (
    run_id TEXT PRIMARY KEY,
    user_query TEXT
)
""")

conn.execute("DROP TABLE IF EXISTS Tools")
conn.execute("""
CREATE TABLE Tools (
    tool_id INTEGER PRIMARY KEY,
    run_id TEXT,
    turn INTEGER,
    tool_name TEXT,
    args_json TEXT,
    started_at  TEXT,
    ended_at    TEXT,
    ok INTEGER,
    error_type TEXT,
    error_description TEXT,
    result_chars INTEGER
)
""")

for path in Path("Traces").glob("*.jsonl"):
    with open(f"{path}") as f:
        for line in f:
            record = json.loads(line)

            if record["type"] == "run":
                conn.execute(
                    "INSERT INTO Runs (run_id, user_query) VALUES (?, ?)",
                    (record["run_id"], record["user_query"])
                )

            elif record["type"] == "call":
                conn.execute(
                    "INSERT INTO Calls (run_id, turn, started_at, ended_at, input_tokens, output_tokens, stop_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (record["run_id"], record["turn"], record["started_at"], record["ended_at"], record["input_tokens"], record["output_tokens"], record["stop_reason"])
                )

            elif record["type"] == "tool":
                conn.execute(
                    "INSERT INTO Tools (run_id, turn, tool_name, args_json, started_at, ended_at, ok, error_type, error_description, result_chars) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (record["run_id"], record["turn"], record["tool_name"], record["args_json"], record["started_at"], record["ended_at"], record["ok"], record["error_type"], record["error_description"], record["result_chars"])
                )

conn.commit()
conn.close()