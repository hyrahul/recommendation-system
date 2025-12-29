-- db/seed/phase2_faq.sql

INSERT INTO faq (question, answer)
VALUES
(
  'How can I enroll in a lecture?',
  'You can enroll in a lecture after logging in, depending on your affiliation.'
),
(
  '강의 접근 권한이 없다고 표시됩니다.',
  '소속 및 권한 그룹에 따라 강의 접근이 제한될 수 있습니다.'
);


-- db/seed/phase2_qna.sql

INSERT INTO qna (question, answer)
VALUES
(
  'What is battery degradation?',
  'Battery degradation is the gradual loss of capacity over time.'
),
(
  '배터리 열화란 무엇인가요?',
  '배터리 열화는 사용에 따라 성능과 용량이 감소하는 현상입니다.'
);


-- db/seed/phase2_permission.sql

INSERT INTO permission_group (permission_grp_id, name)
VALUES
(1, 'KOREA_USER'),
(2, 'GLOBAL_USER');

INSERT INTO permission_group_user (permission_grp_id, user_id)
VALUES
(1, 1);


-- db/seed/phase2_video.sql

INSERT INTO video (video_id, lecture_id, title)
VALUES
(1, 1, 'Battery Basics Introduction Video');

INSERT INTO video_student (video_id, user_id, watched)
VALUES
(1, 1, false);


