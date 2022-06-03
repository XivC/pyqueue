CREATE TABLE IF NOT EXISTS $name$ (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    state TEXT NOT NULL,
    task BLOB NOT NULL
);