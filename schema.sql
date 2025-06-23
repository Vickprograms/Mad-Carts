-- Users table: includes customers and delivery drivers
CREATE TABLE Users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(20),
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_driver BOOLEAN DEFAULT FALSE
);

-- Products table
CREATE TABLE Products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL,
    size VARCHAR(50),
    media TEXT,
    description TEXT,
    brand VARCHAR(100)
);

-- Orders table: contains user and assigned driver
CREATE TABLE Orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    received_at TIMESTAMP,
    condition TEXT,
    delivery_date DATE,
    pickup_location TEXT,
    payment_method VARCHAR(50),
    delivery_driver_id BIGINT REFERENCES Users(id),
    status VARCHAR(50) DEFAULT 'Pending'
);

-- Order items table: links orders and products
CREATE TABLE OrderItems (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES Orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

-- Feedback table: one feedback per product per user
CREATE TABLE Feedback (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES Users(id),
    product_id BIGINT NOT NULL REFERENCES Products(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_message TEXT,
    media TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);