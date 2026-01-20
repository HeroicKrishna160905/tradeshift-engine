-- 1. Enable the Superpower (As per screenshot)
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 2. Create the "Phonebook" table (Metadata)
-- Person 3's script will write to this table.
CREATE TABLE IF NOT EXISTS simulation_metadata (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    file_path VARCHAR(255) NOT NULL, -- Path inside MinIO
    created_at TIMESTAMPTZ DEFAULT NOW()
);