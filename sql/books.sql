-- Table with Incrementing Integer ID
CREATE TABLE academy_award_winning_films (
    id INTEGER PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    year INTEGER,
    awards INTEGER,
    nominations INTEGER
);

-- Table with UUID (Other RDBMS)
CREATE TABLE academy_award_winning_films (
    id VARCHAR(36) PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    year INTEGER,
    awards INTEGER,
    nominations INTEGER
);

-- Table with UUID (Postgres - supports UUID natively)
CREATE TABLE books (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    num_available INTEGER NOT NULL,
    rating INTEGER,
    category VARCHAR(70) NOT NULL
);