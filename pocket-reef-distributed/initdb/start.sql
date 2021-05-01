CREATE USER IF NOT EXISTS 'reefuser'@'localhost';
ALTER USER 'reefuser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

CREATE DATABASE IF NOT EXISTS reef;
GRANT ALL PRIVILEGES ON reef.* to 'reefuser'@'localhost';

use reef;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id        	int				NOT NULL AUTO_INCREMENT,
    name		varchar(50)     NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS node;
CREATE TABLE node (
    ip				varchar(40)     NOT NULL,
    total_space		BIGINT(8)     NOT NULL,
    free_space		BIGINT(8)     NOT NULL,
    status			varchar(10)     NOT NULL,
    node_key 		varchar(10)     NOT NULL,
    PRIMARY KEY (ip)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS file;
CREATE TABLE file (
	ip 			varchar(40) 	NOT NULL,
	user_id		varchar(50)		NOT NULL,
	id			varchar(100)		NOT NULL,
	directory	varchar(11)	NOT NULL,
	is_dir		tinyint(1)		DEFAULT '0',
	PRIMARY KEY (`ip`,`user_id`,`id`,`directory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;	


