import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cami_netherlands.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS assessments (
            id              TEXT PRIMARY KEY,
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- Profile
            name            TEXT NOT NULL,
            email           TEXT NOT NULL,
            age             INTEGER NOT NULL,
            phone           TEXT,
            referral_source TEXT,
            language        TEXT DEFAULT 'en',

            -- Goals (JSON)
            goals           TEXT NOT NULL,

            -- Screening (JSON)
            screening       TEXT NOT NULL,

            -- Results
            track_recommended          TEXT,
            sentinel_status            TEXT,
            clinical_score             INTEGER DEFAULT 0,
            performance_score          INTEGER DEFAULT 0,
            medical_clearance_required BOOLEAN DEFAULT 0,

            -- Consent
            consent_health      BOOLEAN DEFAULT 0,
            consent_marketing   BOOLEAN DEFAULT 0,
            consent_liability   BOOLEAN DEFAULT 0,
            consent_timestamp   TEXT,

            -- Workflow
            status              TEXT DEFAULT 'new',
            payment_status      TEXT DEFAULT 'pending',
            payment_id          TEXT,
            stripe_payment_link TEXT,
            notes               TEXT,

            -- UTM tracking
            utm_source      TEXT,
            utm_medium      TEXT,
            utm_campaign    TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_email      ON assessments(email);
        CREATE INDEX IF NOT EXISTS idx_created_at ON assessments(created_at);
        CREATE INDEX IF NOT EXISTS idx_status     ON assessments(status);
        CREATE INDEX IF NOT EXISTS idx_track      ON assessments(track_recommended);
    """)
    conn.commit()

    # ── Migrations: add columns to existing DBs ──────────────────────────────
    _migrate(conn)
    conn.close()
    print(f"[DB] Initialized at {DB_PATH}")


def _migrate(conn):
    """Idempotent column additions for schema upgrades."""
    existing = {row[1] for row in conn.execute("PRAGMA table_info(assessments)")}
    migrations = [
        ("medical_clearance_required", "BOOLEAN DEFAULT 0"),
        ("stripe_payment_link",        "TEXT"),
        ("ai_analysis",                "TEXT"),
    ]
    for col, definition in migrations:
        if col not in existing:
            conn.execute(f"ALTER TABLE assessments ADD COLUMN {col} {definition}")
            print(f"[DB] Migration: added column {col}")
    conn.commit()
