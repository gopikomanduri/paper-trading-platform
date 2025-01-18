CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    advisor_id INT REFERENCES users(id),
    plan VARCHAR(50) NOT NULL,
    cost NUMERIC(12, 2) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL
);
