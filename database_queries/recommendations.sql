CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    advisor_id INT REFERENCES advisors(id),
    symbol VARCHAR(20) NOT NULL,
    strategy_details TEXT NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

