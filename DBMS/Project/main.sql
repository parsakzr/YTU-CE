
-- ANALYZE;


-- get all indexes
-- SELECT
--     tablename,
--     indexname,
--     indexdef
-- FROM
--     pg_indexes
-- WHERE
--     schemaname = 'public';


-- Step 2: w/o indexing

-- drop all the indexes and pkeys

-- ALTER TABLE course DROP CONSTRAINT IF EXISTS course_pkey CASCADE;
-- ALTER TABLE teaches DROP CONSTRAINT IF EXISTS teaches_pkey CASCADE;
-- ALTER TABLE takes DROP CONSTRAINT IF EXISTS takes_pkey CASCADE;
-- ALTER TABLE instructor DROP CONSTRAINT IF EXISTS instructor_pkey CASCADE;
-- ALTER TABLE student DROP CONSTRAINT IF EXISTS student_pkey CASCADE;



-- 2.1 Find the names of all the instructors from Biology department
-- SELECT name FROM instructor WHERE dept_name = 'Biology'

-- 2.2 Find the names of courses in Computer science department which have 3 credits
-- SELECT title FROM course WHERE dept_name = 'Comp. Sci.' AND credits=3

-- 2.3 For the student with ID 12345 (or any other value), show all course_id and title of all courses registered for by the student.
-- SELECT course_id, title FROM takes natural join course WHERE id='1000'

-- 2.4 As above, but show the total number of credits for such courses (taken by that student).
-- SELECT sum(credits) FROM takes natural join course WHERE ID = '1000'

-- 2.5 As above, but display the total credits for each of the students, along with the ID of the student
-- EXPLAIN ANALYZE SELECT id, sum(credits) FROM takes natural join course GROUP BY id

-- 2.6 Find the names of all students who have taken any Comp. Sci. course ever (no duplicate)
-- SELECT DISTINCT s.name FROM student as s natural join (takes natural join course) WHERE dept_name='Comp. Sci.'

-- 2.7 Display the IDs of all instructors who have never taught a course
-- EXPLAIN ANALYZE SELECT id FROM instructor WHERE id NOT IN (SELECT id FROM teaches)

-- 2.8 As above, but display the names of the instructors also, not just the IDs.
-- SELECT id, name FROM instructor WHERE id NOT IN (SELECT id FROM teaches)