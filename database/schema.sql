CREATE DATABASE livestock_app
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE livestock_app;

CREATE TABLE administrative_level (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE administrative_unit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    administrative_id INT,
    level_id INT NOT NULL,
    FOREIGN KEY (administrative_id) REFERENCES administrative_unit(id),
    FOREIGN KEY (level_id) REFERENCES administrative_level(id)
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    status TINYINT DEFAULT 1,
    unit_id INT,
    FOREIGN KEY (unit_id) REFERENCES administrative_unit(id)
);

CREATE TABLE account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE activities_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    activities TEXT,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES account(id)
);

CREATE TABLE permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE `group` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

CREATE TABLE user_groups (
    user_id INT,
    group_id INT,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (group_id) REFERENCES `group`(id)
);

CREATE TABLE user_permissions (
    user_id INT,
    permissions_id INT,
    PRIMARY KEY (user_id, permissions_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (permissions_id) REFERENCES permissions(id)
);

CREATE TABLE group_permissions (
    group_id INT,
    permissions_id INT,
    PRIMARY KEY (group_id, permissions_id),
    FOREIGN KEY (group_id) REFERENCES `group`(id),
    FOREIGN KEY (permissions_id) REFERENCES permissions(id)
);

CREATE TABLE gen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    origin VARCHAR(255),
    genetic_code VARCHAR(100),
    status TINYINT
);

CREATE TABLE species (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    scientific_name VARCHAR(255),
    conservation_status VARCHAR(255),
    export_restriction_status VARCHAR(255)
);

CREATE TABLE facility (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    certification VARCHAR(255),
    type VARCHAR(255),
    status TINYINT,
    scale VARCHAR(100),
    unit_id INT,
    FOREIGN KEY (unit_id) REFERENCES administrative_unit(id)
);

CREATE TABLE facility_gen (
    gen_id INT,
    facility_id INT,
    PRIMARY KEY (gen_id, facility_id),
    FOREIGN KEY (gen_id) REFERENCES gen(id),
    FOREIGN KEY (facility_id) REFERENCES facility(id)
);

CREATE TABLE facility_species (
    species_id INT,
    facility_id INT,
    PRIMARY KEY (species_id, facility_id),
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (facility_id) REFERENCES facility(id)
);

CREATE TABLE food (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    description TEXT
);

CREATE TABLE substances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(255),
    description TEXT,
    banned BOOLEAN DEFAULT FALSE
);

CREATE TABLE food_substance (
    food_id INT,
    substances_id INT,
    PRIMARY KEY (food_id, substances_id),
    FOREIGN KEY (food_id) REFERENCES food(id),
    FOREIGN KEY (substances_id) REFERENCES substances(id)
);

CREATE TABLE facility_food (
    facility_id INT,
    food_id INT,
    PRIMARY KEY (facility_id, food_id),
    FOREIGN KEY (facility_id) REFERENCES facility(id),
    FOREIGN KEY (food_id) REFERENCES food(id)
);

ALTER TABLE `group`
ADD COLUMN is_active TINYINT(1) DEFAULT 1;

ALTER TABLE permissions
ADD COLUMN is_active TINYINT(1) DEFAULT 1;

CREATE TABLE instructions (
     id INT AUTO_INCREMENT PRIMARY KEY,
     title VARCHAR(255),
     content TEXT
);