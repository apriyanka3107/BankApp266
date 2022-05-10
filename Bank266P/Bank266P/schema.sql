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
  balance FLOAT(15,2) NOT NULL
);

INSERT INTO bankacc (first_name,last_name,username, password, balance)
VALUES ('Main', 'Administrator', 'admin', '21232F297A57A5A743894A0E4A801FC3', '100.00');
