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
	is_moderator BOOLEAN DEFAULT FALSE, 
	is_admin BOOLEAN DEFAULT FALSE,
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
	is_approved BOOLEAN DEFAULT FALSE,
	content TEXT NOT NULL,
	video_link VARCHAR(255),
	post_time TIMESTAMP NOT NULL,
	writer_username VARCHAR(20) NOT NULL,
	approver_username VARCHAR(20),
	migrated INT,
	is_blog BOOLEAN DEFAULT FALSE,
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
	is_user BOOLEAN,
	FOREIGN KEY(post) REFERENCES post(post_id) ON DELETE CASCADE
);

INSERT INTO user VALUES ('admin','21232f297a57a5a743894a0e4a801fc3','Administrator','admin@example.com',TRUE,TRUE,0);
INSERT INTO user VALUES ('mod','ad148a3ca8bd0ef3b48c52454c493ec5','Moderator','mod@example.com',TRUE,FALSE,0);
INSERT INTO user VALUES ('collab','d5029374377771fd628239fd1f4e9d02','Collaborator','collab@example.com',FALSE,FALSE,0);

INSERT INTO migration VALUES (1, 28.94, 71.83, 28.46, 72.54);
INSERT INTO migration VALUES (2, 28.94, 71.83, 26.98, 72.04);
INSERT INTO migration VALUES (3, NULL, NULL, 29.898, 73.866);

INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved, migrated, upvotes) VALUES ('Sri Ganaganagar Interview', 'An interview with Nilawanti in Sri Ganganagar district, Rajasthan who was 10 years old in 1947. She shares her family’s experience of displacement in Partition.', 'https://www.youtube.com/embed/Amg44-MX4ZM', '2019-02-28 10:00:00', 'collab', 'mod', TRUE, 3, 10);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username) VALUES ('Post2', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved, migrated) VALUES ('Post3', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', 'mod', TRUE, 2);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post4', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'mod', NULL , FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post5', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL , FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post6', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL , FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post7', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL, FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post8', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL, FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post9', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab', NULL, FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post10', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab',NULL,  FALSE);
INSERT INTO post (nameofarticle, content, video_link, post_time, writer_username, approver_username, is_approved) VALUES ('Post11', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://www.youtube.com/embed/aJaSCqPvwOA', '2019-02-28 10:00:00', 'collab',NULL,  FALSE);

INSERT INTO post (nameofarticle, content, post_time, writer_username, approver_username, is_approved, migrated, is_blog) VALUES ('"The Great Partition" Book review', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', '2019-03-28 10:00:00', 'collab', 'mod', TRUE, 2, TRUE);

INSERT INTO comment VALUES(1,'collab','Great Article !',1,'2019-03-24 10:00:00',TRUE);
INSERT INTO comment VALUES(2,'mod','Some Comment 1',1,'2019-03-25 10:00:00',TRUE);
INSERT INTO comment VALUES(3,'Name3','Some Comment 2',1,'2019-03-27 10:00:00',FALSE);
INSERT INTO comment VALUES(4,'Name1','Great Article !',2,'2019-03-28 10:00:00',FALSE);
INSERT INTO comment VALUES(5,'Name2','Some Comment 1',2,'2019-03-29 10:00:00',FALSE);

