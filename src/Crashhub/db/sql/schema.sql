CREATE TABLE IF NOT EXISTS crashkind (
    id SERIAL PRIMARY KEY,
    file TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    github_id INTEGER NOT NULL DEFAULT -1
);

CREATE TABLE IF NOT EXISTS crash (
    id SERIAL PRIMARY KEY,
    kind_id INTEGER NOT NULL REFERENCES crashkind (id),
    app_version VARCHAR(255) NOT NULL,
    os TEXT NOT NULL,
    wallet_type VARCHAR(255) NOT NULL,
    exc_string TEXT NOT NULL,
    stack TEXT NOT NULL,
    description TEXT NOT NULL,
    locale VARCHAR(5) NOT NULL DEFAULT '',
    python_version VARCHAR(255) NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS crash_kind_id ON crash (kind_id);

CREATE TABLE IF NOT EXISTS logentry (
    id SERIAL PRIMARY KEY,
    sender_ip VARCHAR(255) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
