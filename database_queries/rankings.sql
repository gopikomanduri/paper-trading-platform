CREATE TABLE rankings (
    id SERIAL PRIMARY KEY,
    contest_id INT REFERENCES contests(id),
    user_id INT REFERENCES users(id),
    rank INT NOT NULL,
    profit_loss NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
