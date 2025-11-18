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