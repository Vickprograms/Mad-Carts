-- Users table: includes customers and delivery drivers
-- Users table
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(20),
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_driver BOOLEAN DEFAULT FALSE
);

-- Products table
CREATE TABLE Products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL,
    size VARCHAR(50),
    media TEXT,
    description TEXT,
    brand VARCHAR(100)
);

-- Orders table
CREATE TABLE Orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    received_at TIMESTAMP,
    condition TEXT,
    delivery_date DATE,
    pickup_location TEXT,
    payment_method VARCHAR(50),
    delivery_driver_id UUID REFERENCES Users(id),
    status VARCHAR(50) DEFAULT 'Pending'
);

-- OrderItems table
CREATE TABLE OrderItems (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES Orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

-- Feedback table
CREATE TABLE Feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id),
    product_id UUID NOT NULL REFERENCES Products(id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback_message TEXT,
    media TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE RecentSearches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE,
    search_term TEXT NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE RecentVisits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES Products(id) ON DELETE CASCADE,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);