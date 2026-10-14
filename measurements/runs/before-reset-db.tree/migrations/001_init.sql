-- Reserved for a future database backend. Applied migrations are never edited.
CREATE TABLE items (
    sku        TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    qty        INTEGER NOT NULL DEFAULT 0,
    location   TEXT NOT NULL DEFAULT 'unsorted',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
