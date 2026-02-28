import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Define DB path
DB_PATH = Path(__file__).parent.parent / "trading_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ticker TEXT NOT NULL,
            status TEXT NOT NULL,
            technical_pass INTEGER,
            fundamental_pass INTEGER,
            risk_metrics TEXT,
            rejection_reason TEXT,
            full_state TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_evaluation(state: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    ticker = state.get("current_ticker", "UNKNOWN")
    status = state.get("status", "Unknown")
    t_pass = 1 if state.get("technical_pass") else (0 if state.get("technical_pass") is False else None)
    f_pass = 1 if state.get("fundamental_pass") else (0 if state.get("fundamental_pass") is False else None)
    
    risk_metrics_json = json.dumps(state.get("risk_metrics")) if state.get("risk_metrics") else None
    rej_reason = state.get("rejection_reason")
    full_state_json = json.dumps(state)
    
    cursor.execute('''
        INSERT INTO evaluations (timestamp, ticker, status, technical_pass, fundamental_pass, risk_metrics, rejection_reason, full_state)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, ticker, status, t_pass, f_pass, risk_metrics_json, rej_reason, full_state_json))
    
    conn.commit()
    conn.close()

# Initialize DB when module loads
init_db()
