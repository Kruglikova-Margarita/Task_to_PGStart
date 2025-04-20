DROP TABLE IF EXISTS badges CASCADE;
DROP TABLE IF EXISTS post_links CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS post_history CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS post_types CASCADE;
DROP TABLE IF EXISTS vote_types CASCADE;
DROP TABLE IF EXISTS post_history_types CASCADE;
DROP TABLE IF EXISTS link_types CASCADE;

-- Users

CREATE TABLE users (
	id INT PRIMARY KEY,
	reputation INT,
	creation_date TIMESTAMP,
	display_name TEXT,
	last_access_date TIMESTAMP,
	website_url TEXT,
	location TEXT, 
	about_me TEXT,
	views INT,
	up_votes INT,
	down_votes INT,
	account_id INT
);

CREATE TABLE badges (
	id INT PRIMARY KEY,
	user_id INT REFERENCES users(id),
	name TEXT,
	date TIMESTAMP,
	class SMALLINT,
	tag_based BOOLEAN
);





-- Posts

CREATE TABLE post_types (
	id INT PRIMARY KEY,
	name VARCHAR(30)
);

CREATE TABLE posts (
	id INT PRIMARY KEY,
	post_type_id SMALLINT REFERENCES post_types(id),
	accepted_answer_id INT REFERENCES posts(id),
	parent_id INT REFERENCES posts(id),
	creation_date TIMESTAMP,
	score INT,
	view_count INT,
	body TEXT,
	owner_user_id INT REFERENCES users(id),
	owner_display_name TEXT,
	last_editor_user_id INT,
	last_editor_display_name TEXT,
	last_edit_date TIMESTAMP,
	last_activity_date TIMESTAMP,
	title TEXT,
	tags TEXT,
	answer_count INT,
	comment_count INT,
	favorite_count INT,
	closed_date TIMESTAMP,
	community_owned_date TIMESTAMP
);

CREATE TABLE link_types (
	id SMALLINT PRIMARY KEY,
	name VARCHAR(9)
);

CREATE TABLE post_links (
	id INT PRIMARY KEY,
	creation_date TIMESTAMP,
	post_id INT REFERENCES posts(id),
	related_post_id INT REFERENCES posts(id),
	link_type_id SMALLINT REFERENCES link_types(id)
);

CREATE TABLE comments (
	id INT PRIMARY KEY,
	post_id INT REFERENCES posts(id),
	score INT,
	text_field TEXT,
	creation_date TIMESTAMP,
	user_display_name TEXT,
	user_id INT REFERENCES users(id)
);





-- Tags

CREATE TABLE tags (
	id INT PRIMARY KEY,
	tag_name TEXT,
	count INT,
	excpert_post_id INT REFERENCES posts(id),
	wiki_post_id INT REFERENCES posts(id)
);





-- Votes and Feedback

CREATE TABLE vote_types (
	id INT PRIMARY KEY,
	name VARCHAR(7)
);

CREATE TABLE votes (
	id INT PRIMARY KEY,
	post_id INT REFERENCES posts(id),
	vote_type_id SMALLINT REFERENCES vote_types(id),
	creation_date TIMESTAMP
);





-- History

CREATE TABLE post_history_types (
	id INT PRIMARY KEY,
	name VARCHAR(75)
);

CREATE TABLE post_history (
	id INT PRIMARY KEY,
	post_history_type_id SMALLINT REFERENCES post_history_types(id),
	post_id INT REFERENCES posts(id),
	revision_guid VARCHAR(40),
	creation_date TIMESTAMP,
	user_id INT REFERENCES users(id),
	user_display_name TEXT,
	comment TEXT,
	text TEXT
);





















































