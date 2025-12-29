INSERT INTO users (username, full_name, affiliation)
VALUES
  ('lee.dohyun', 'Lee Dohyun', 'Korea'),
  ('kim.minseo', 'Kim Minseo', 'Korea'),
  ('john.smith', 'John Smith', 'USA'),
  ('li.wei', 'Li Wei', 'China')
ON CONFLICT (username) DO NOTHING;


INSERT INTO categories (name, visibility)
VALUES
  ('Battery Basics', 'Korea'),
  ('Advanced Battery Systems', 'Korea'),
  ('Global Standards for Overseas', 'OverseasCommon'),
  ('US Battery Regulations', 'USA')
ON CONFLICT (name) DO NOTHING;



-- Basic
INSERT INTO lectures (title, category_id, difficulty)
SELECT 'Introduction to Battery Basics', id, 'Basic'
FROM categories WHERE name = 'Battery Basics'
ON CONFLICT DO NOTHING;

-- Intermediate
INSERT INTO lectures (title, category_id, difficulty)
SELECT 'Battery Materials and Chemistry', id, 'Intermediate'
FROM categories WHERE name = 'Battery Basics'
ON CONFLICT DO NOTHING;

-- Advanced
INSERT INTO lectures (title, category_id, difficulty)
SELECT 'Advanced Battery Design', id, 'Advanced'
FROM categories WHERE name = 'Advanced Battery Systems'
ON CONFLICT DO NOTHING;

-- Overseas only
INSERT INTO lectures (title, category_id, difficulty)
SELECT 'International Battery Standards', id, 'Basic'
FROM categories WHERE name = 'Global Standards for Overseas'
ON CONFLICT DO NOTHING;

-- USA only
INSERT INTO lectures (title, category_id, difficulty)
SELECT 'US Battery Compliance', id, 'Basic'
FROM categories WHERE name = 'US Battery Regulations'
ON CONFLICT DO NOTHING;


-- Intermediate requires Basic
INSERT INTO lecture_prerequisites
SELECT i.id, b.id
FROM lectures i
JOIN lectures b
  ON b.title = 'Introduction to Battery Basics'
WHERE i.title = 'Battery Materials and Chemistry'
ON CONFLICT DO NOTHING;

-- Advanced requires Intermediate
INSERT INTO lecture_prerequisites
SELECT a.id, i.id
FROM lectures a
JOIN lectures i
  ON i.title = 'Battery Materials and Chemistry'
WHERE a.title = 'Advanced Battery Design'
ON CONFLICT DO NOTHING;

-- Lee: beginner
INSERT INTO lecture_students
SELECT u.id, l.id, 'NotStarted'
FROM users u
JOIN lectures l ON l.title = 'Introduction to Battery Basics'
WHERE u.username = 'lee.dohyun'
ON CONFLICT DO NOTHING;

-- Kim: completed basic
INSERT INTO lecture_students
SELECT u.id, l.id, 'Completed'
FROM users u
JOIN lectures l ON l.title = 'Introduction to Battery Basics'
WHERE u.username = 'kim.minseo'
ON CONFLICT DO NOTHING;

-- Kim: in progress intermediate
INSERT INTO lecture_students
SELECT u.id, l.id, 'InProgress'
FROM users u
JOIN lectures l ON l.title = 'Battery Materials and Chemistry'
WHERE u.username = 'kim.minseo'
ON CONFLICT DO NOTHING;

-- John (USA): completed overseas
INSERT INTO lecture_students
SELECT u.id, l.id, 'Completed'
FROM users u
JOIN lectures l ON l.title = 'International Battery Standards'
WHERE u.username = 'john.smith'
ON CONFLICT DO NOTHING;



psql -d recommendation_db -f db/seed/phase1_seed.sql
SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM lectures;
SELECT * FROM lecture_prerequisites;
SELECT * FROM lecture_students;
