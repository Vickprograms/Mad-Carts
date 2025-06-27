CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- USERS
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(20),
    username VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_driver BOOLEAN DEFAULT FALSE,
    role VARCHAR(20) DEFAULT 'customer'
);

-- PRODUCTS
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

-- ORDERS
CREATE TABLE Orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ORDER ITEMS
CREATE TABLE OrderItems (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES Orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL
);

-- DELIVERIES
CREATE TABLE Deliveries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES Orders(id) ON DELETE CASCADE,
    driver_id UUID REFERENCES Users(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    delivery_date DATE,
    delivery_notes TEXT,
    delivered_at TIMESTAMP
);

-- FEEDBACK
CREATE TABLE Feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id),
    product_id UUID NOT NULL REFERENCES Products(id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback_message TEXT,
    media TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CART
CREATE TABLE Carts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CART ITEMS
CREATE TABLE CartItems (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cart_id UUID NOT NULL REFERENCES Carts(id) ON DELETE CASCADE,
    product_id UUID NOT NULL,
    quantity INT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

-- SEARCHES
CREATE TABLE RecentSearches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE,
    search_term TEXT NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- VISITS
CREATE TABLE RecentVisits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES Products(id) ON DELETE CASCADE,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
