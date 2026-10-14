-- Optional free-text notes per item. Nullable, so existing rows need no backfill.
ALTER TABLE items ADD COLUMN notes TEXT;
