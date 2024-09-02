-- Table with Incrementing Integer ID
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability INTEGER NOT NULL,
    star_rating DECIMAL(3, 2),
    category VARCHAR(70) NOT NULL
);

-- Table with UUID (Other RDBMS)
CREATE TABLE books (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability INTEGER NOT NULL,
    star_rating DECIMAL(3, 2),
    category VARCHAR(70) NOT NULL
);

-- Table with UUID (Postgres - supports UUID natively)
CREATE TABLE books (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability INTEGER NOT NULL,
    star_rating DECIMAL(3, 2),
    category VARCHAR(70) NOT NULL
);
