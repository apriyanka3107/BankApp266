-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS bankacc;
DROP TABLE IF EXISTS post;

CREATE TABLE bankacc (
  accid INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR (50) NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  balance DECIMAL(15,2) NOT NULL
);

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );
