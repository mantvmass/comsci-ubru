CREATE DATABASE comsci;

CREATE TABLE accounts (
    id int(100) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email varchar(150) NOT NULL UNIQUE,
    username varchar(150) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    is_admin tinyint(1) NOT NULL DEFAULT 0,
    banned tinyint(1) NOT NULL DEFAULT 0,
    created_at timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE tokens (
    id int(100) NOT NULL,
    token varchar(255) NOT NULL UNIQUE,
    message varchar(255) NOT NULL,
    total_sub tinyint(1) NOT NULL DEFAULT 0, -- sub table
    qr_path varchar(255) NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=INNODB DEFAULT CHARSET=utf8;
ALTER TABLE tokens ADD CONSTRAINT tokens_id_accounts_id FOREIGN KEY (id) REFERENCES accounts(id);


CREATE TABLE sub (
    nickname varchar(50) NOT NULL,
    full_name varchar(150) NOT NULL,
    save_token varchar(255) NOT NULL, -- token table
    facebook_url varchar(200) NOT NULL,
    img_path varchar(255) NOT NULL,
    created_at timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=INNODB DEFAULT CHARSET=utf8;


CREATE TABLE super (
    username varchar(150) NOT NULL UNIQUE,
    secret_key varchar(255) NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8;