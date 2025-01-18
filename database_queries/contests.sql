CREATE TABLE contests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    entry_fee NUMERIC(12, 2) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    duration INT NOT NULL,              -- Duration in minutes
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);
