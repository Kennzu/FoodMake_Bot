USE food_list;

DROP TABLE IF EXISTS food_breakfast;
DROP TABLE IF EXISTS food_lanch;  -- Обратите внимание на исправление опечатки (lanch -> lunch)
DROP TABLE IF EXISTS food_dinner;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS couple_requests;
DROP TABLE IF EXISTS couples_user;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users_db (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    username VARCHAR(255),
    first_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS couples_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    couple_uuid CHAR(36) UNIQUE,
    partner1_id BIGINT,
    partner2_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (partner1_id) REFERENCES users(telegram_id),
    FOREIGN KEY (partner2_id) REFERENCES users(telegram_id),
    UNIQUE (partner1_id, partner2_id)
);

CREATE TABLE IF NOT EXISTS couple_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id BIGINT,
    receiver_id BIGINT,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(telegram_id),
    FOREIGN KEY (receiver_id) REFERENCES users(telegram_id)
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    couple_uuid CHAR(36) UNIQUE,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (couple_uuid) REFERENCES couples_user(couple_uuid)
);

CREATE TABLE IF NOT EXISTS food_breakfast (
    id INT AUTO_INCREMENT PRIMARY KEY,
    couple_uuid CHAR(36) UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    calories INT,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (couple_uuid) REFERENCES couples_user(couple_uuid)
);

CREATE TABLE IF NOT EXISTS food_lanch (
    id INT AUTO_INCREMENT PRIMARY KEY,
    couple_uuid CHAR(36) UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    calories INT,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (couple_uuid) REFERENCES couples_user(couple_uuid)
);

CREATE TABLE IF NOT EXISTS food_dinner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    couple_uuid CHAR(36) UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    calories INT,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (couple_uuid) REFERENCES couples_user(couple_uuid)
);