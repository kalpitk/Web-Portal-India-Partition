CREATE DATABASE IF NOT EXISTS PROJECT;
USE PROJECT;


DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS migration;
DROP TABLE IF EXISTS user;


CREATE TABLE user(
	username VARCHAR(20) PRIMARY KEY,
	password VARCHAR(20) NOT NULL,
	name VARCHAR(20) NOT NULL,
	email_id VARCHAR(50) NOT NULL UNIQUE,
	Is_Moderator BOOLEAN DEFAULT FALSE, 
	Is_Admin BOOLEAN DEFAULT FALSE,
	contributions INT DEFAULT 0
);

CREATE TABLE migration(
	mig_id INT PRIMARY KEY,
	src_lati DECIMAL(9,6),
	src_long DECIMAL(9,6),
	dest_lati DECIMAL(9,6),
	dest_long DECIMAL(9,6) 
);

CREATE TABLE post(
	post_id INT PRIMARY KEY,
	namefarticle VARCHAR(255),
	upvotes INT DEFAULT 0,
	downvotes INT DEFAULT 0,
	Is_Approved BOOLEAN DEFAULT FALSE,
	content TEXT NOT NULL,
	video_link VARCHAR(255),
	post_time TIMESTAMP NOT NULL,
	writer_username VARCHAR(20) NOT NULL,
	approver_username VARCHAR(20) NOT NULL,
	migrated INT,
	FOREIGN KEY(writer_username) REFERENCES user(username),
	FOREIGN KEY(approver_username) REFERENCES user(username),
	FOREIGN KEY(migrated) REFERENCES migration(mig_id)
);

CREATE TABLE comment(
	comment_id INT PRIMARY KEY,
	name VARCHAR(20) NOT NULL,
	comment TEXT NOT NULL,
	post INT NOT NULL,
	FOREIGN KEY(post) REFERENCES post(post_id) ON DELETE CASCADE
);

INSERT INTO user VALUES ('admin','admin','Administrator','admin@example.com',TRUE,TRUE,0);
INSERT INTO user VALUES ('mod','mod','Moderator','mod@example.com',TRUE,FALSE,0);
INSERT INTO user VALUES ('collab','collab','Collaborator','collab@example.com',FALSE,FALSE,0);
