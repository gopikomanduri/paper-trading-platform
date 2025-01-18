CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    type VARCHAR(50),       -- e.g., "BUY", "SELL", "CONTEST_ENTRY", "SUBSCRIPTION"
    amount NUMERIC(12, 2),  -- Positive for credit, negative for debit
    balance NUMERIC(12, 2), -- Balance after the transaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
