CREATE DATABASE IF NOT EXISTS PROJECT;
USE PROJECT;


DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS migration;
DROP TABLE IF EXISTS user;


CREATE TABLE user(
	username VARCHAR(20) PRIMARY KEY,
	password VARCHAR(32) NOT NULL,
	name VARCHAR(20) NOT NULL,
	email_id VARCHAR(50) NOT NULL UNIQUE,
	Is_Moderator BOOLEAN DEFAULT FALSE, 
	Is_Admin BOOLEAN DEFAULT FALSE,
	contributions INT DEFAULT 0
);

CREATE TABLE migration(
	mig_id INT PRIMARY KEY AUTO_INCREMENT,
	src_lat FLOAT,
	src_lng FLOAT,
	dest_lat FLOAT,
	dest_lng FLOAT 
);

CREATE TABLE post(
	post_id INT PRIMARY KEY AUTO_INCREMENT,
	nameofarticle VARCHAR(255),
	upvotes INT DEFAULT 0,
	downvotes INT DEFAULT 0,
	Is_Approved BOOLEAN DEFAULT FALSE,
	content TEXT NOT NULL,
	video_link VARCHAR(255),
	post_time TIMESTAMP NOT NULL,
	writer_username VARCHAR(20) NOT NULL,
	approver_username VARCHAR(20),
	migrated INT,
	FOREIGN KEY(writer_username) REFERENCES user(username),
	FOREIGN KEY(approver_username) REFERENCES user(username),
	FOREIGN KEY(migrated) REFERENCES migration(mig_id)
);

CREATE TABLE comment(
	comment_id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(20) NOT NULL,
	comment TEXT NOT NULL,
	post INT NOT NULL,
	commented_time TIMESTAMP NOT NULL,
	FOREIGN KEY(post) REFERENCES post(post_id) ON DELETE CASCADE
);

INSERT INTO user VALUES ('admin','21232f297a57a5a743894a0e4a801fc3','Administrator','admin@example.com',TRUE,TRUE,0);
INSERT INTO user VALUES ('mod','ad148a3ca8bd0ef3b48c52454c493ec5','Moderator','mod@example.com',TRUE,FALSE,0);
INSERT INTO user VALUES ('collab','d5029374377771fd628239fd1f4e9d02','Collaborator','collab@example.com',FALSE,FALSE,0);

INSERT INTO migration VALUES (1, -34.90, 150.7, -32.3, 149.6);
INSERT INTO migration VALUES (2, -34.90, 150.7, -32.9, 150);

INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, Is_Approved, migrated) VALUES ('Post1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', 'mod', TRUE, 1);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username) VALUES ('Post2', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, Is_Approved, migrated) VALUES ('Post3', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', 'mod', TRUE, 2);

INSERT INTO comment VALUES(1,'name1','comment1',1,'2019-03-24 10:00:00');
INSERT INTO comment VALUES(2,'name2','comment2',1,'2019-03-25 10:00:00');
INSERT INTO comment VALUES(3,'name3','comment3',1,'2019-03-27 10:00:00');
INSERT INTO comment VALUES(4,'name1','comment1',2,'2019-03-28 10:00:00');
INSERT INTO comment VALUES(5,'name2','comment2',2,'2019-03-29 10:00:00');

