USE registry_db;
CREATE TABLE IF NOT EXISTS services (     
    id CHAR(36) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT, 
    url VARCHAR(2048) );    
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL PRIMARY KEY, 
    password_hash VARCHAR(255) NOT NULL,
    write_access VARCHAR(10) DEFAULT 'NONE');
INSERT INTO users (username, password_hash, write_access)
VALUES (
    'admin',
    '$2b$12$YWtcqFBtYJZp6w8IrhInZeaV5n399APutEKhbW/PNeo5DADlsIA0e',
    'FULL'
);
