BEGIN TRANSACTION;
CREATE TABLE `vine_post_test` (
	`username`	TEXT NOT NULL,
	`created`	TEXT,
	`likes`	INTEGER DEFAULT 0,
	`reposts`	INTEGER DEFAULT 0,
	`loops`	INTEGER DEFAULT 0,
	`comments`	INTEGER DEFAULT 0,
	`description`	TEXT,
	`video_link`	TEXT NOT NULL,
	`revine_check`	INTEGER,
	`revined_user`	TEXT,
	PRIMARY KEY(video_link)
);
CREATE TABLE `vine_page_test` (
	`username`	TEXT NOT NULL,
	`date`	TEXT NOT NULL,
	`user_id`	INTEGER NOT NULL,
	`post_count`	INTEGER DEFAULT 0,
	`follower_count`	INTEGER DEFAULT 0,
	`following_count`	INTEGER DEFAULT 0,
	`loop_count`	INTEGER DEFAULT 0,
	`like_count`	INTEGER DEFAULT 0,
	PRIMARY KEY(date,user_id)
);
CREATE TABLE entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);
INSERT INTO `entries` VALUES (1,'title1','text1');
INSERT INTO `entries` VALUES (2,'title2','text2');
INSERT INTO `entries` VALUES (3,'title3','text3');
INSERT INTO `entries` VALUES (5,'title4','text4');
INSERT INTO `entries` VALUES (6,'title5','text5');
COMMIT;
