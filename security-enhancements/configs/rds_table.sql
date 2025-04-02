CREATE TABLE ip_errors (
    ip VARCHAR(45) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    error_count INTEGER NOT NULL,
    CONSTRAINT valid_error_count CHECK (error_count > 0)
);