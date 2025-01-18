CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    symbol VARCHAR(20) NOT NULL,
    order_type VARCHAR(10) NOT NULL, -- 'BUY' or 'SELL'
    price NUMERIC(12, 2),
    quantity INT NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

