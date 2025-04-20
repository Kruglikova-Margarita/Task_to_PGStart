WITH parent_posts AS (
	SELECT * FROM posts
), answer_posts AS (
	SELECT * FROM posts
)
SELECT parent_posts.accepted_answer_id, answer_posts.owner_user_id, users.display_name AS owner_user_name, answer_posts.score, parent_posts.tags AS parent_tags, answer_posts.tags AS answer_tags
FROM parent_posts 
INNER JOIN answer_posts ON (parent_posts.accepted_answer_id = answer_posts.id)
INNER JOIN users ON (answer_posts.owner_user_id = users.id)
WHERE (parent_posts.post_type_id = 1) AND (parent_posts.tags LIKE '%postgresql%') AND (parent_posts.tags IS NOT NULL)
ORDER BY answer_posts.score;
