import psycopg2

"""
    BLM3780 DBMS Final Project @ Yildiz Technical University
    Parsa Kazerooni - 19011915
    Utku Mehmetoglu - 19011069

Queries
-- 2.1 Find the names of all the instructors from Biology department
-- SELECT name FROM instructor WHERE dept_name = 'Biology'

-- 2.2 Find the names of courses in Computer science department which have 3 credits
-- SELECT title FROM course WHERE dept_name = 'Comp. Sci.' AND credits=3

-- 2.3 For the student with ID 12345 (or any other value), show all course_id and title of all courses registered for by the student.
-- SELECT course_id, title FROM takes natural join course WHERE id='1000'

-- 2.4 As above, but show the total number of credits for such courses (taken by that student).
-- SELECT sum(credits) FROM takes natural join course WHERE ID = '1000'

-- 2.5 As above, but display the total credits for each of the students, along with the ID of the student
-- SELECT id, sum(credits) FROM takes natural join course GROUP BY id

-- 2.6 Find the names of all students who have taken any Comp. Sci. course ever (no duplicate)
-- SELECT DISTINCT s.name FROM student as s natural join (takes natural join course) WHERE dept_name='Comp. Sci.'

-- 2.7 Display the IDs of all instructors who have never taught a course
-- SELECT id FROM instructor WHERE id NOT IN (SELECT id FROM teaches)

-- 2.8 As above, but display the names of the instructors also, not just the IDs.
-- SELECT id, name FROM instructor WHERE id NOT IN (SELECT id FROM teaches)


Before Executing, DROP all pkey constraints in the database.
-- ALTER TABLE advisor DROP CONSTRAINT IF EXISTS advisor_pkey CASCADE;
-- ALTER TABLE classroom DROP CONSTRAINT IF EXISTS classroom_pkey CASCADE;
-- ALTER TABLE course DROP CONSTRAINT IF EXISTS course_pkey CASCADE;
-- ALTER TABLE department DROP CONSTRAINT IF EXISTS department_pkey CASCADE;
-- ALTER TABLE instructor DROP CONSTRAINT IF EXISTS instructor_pkey CASCADE;
-- ALTER TABLE prereq DROP CONSTRAINT IF EXISTS prereq_pkey CASCADE;
-- ALTER TABLE section DROP CONSTRAINT IF EXISTS section_pkey CASCADE;
-- ALTER TABLE student DROP CONSTRAINT IF EXISTS student_pkey CASCADE;
-- ALTER TABLE takes DROP CONSTRAINT IF EXISTS takes_pkey CASCADE;
-- ALTER TABLE teaches DROP CONSTRAINT IF EXISTS teaches_pkey CASCADE;
-- ALTER TABLE time_slot DROP CONSTRAINT IF EXISTS time_slot_pkey CASCADE;
"""


def connect2db():
    # Connect to the PostgreSQL database.  Returns a database connection.
    return psycopg2.connect(
        host="localhost",
        database="universitydb",
        user="postgres"
        # password=""
    )


def get_tables(cur):
    # Return a list of tables.
    cur.execute("SELECT * FROM information_schema.tables \
                WHERE table_type='BASE TABLE' AND table_schema='public';")
    return cur.fetchall()


def get_columns(cur, table):
    # Return a list of columns of the given table.
    cur.execute("SELECT * FROM information_schema.columns \
                WHERE table_name='" + table + "' AND table_schema='public';")
    return cur.fetchall()


def get_indexes(cur, table):
    # Return a list of indexes of the given table.
    cur.execute("SELECT indexname, indexdef FROM pg_indexes \
        WHERE tablename = '{}';".format(table))

    return cur.fetchall()


def fetch_query(cur, query):
    # Return the result of the given query.
    cur.execute(query)
    return cur.fetchall()


def explain_query(cur, query):
    # Return the result of the given query.
    cur.execute("EXPLAIN ANALYZE " + query)
    return cur.fetchall()  # returns query plan


def getExecuteTimeFromQueryPlan(queryPlan):  # queryPlan <- explain_query()
    # last rows of queryPlan is like below
    # ('Planning Time: 1.926 ms'), ('Execution Time: 27.657 ms')
    # --> returns 28.073

    print("\tTime benchmarks : ", queryPlan[-2:])  # LOG - last two rows

    return float(queryPlan[-2:][1][0].split(':')[1].replace(' ms', ''))


def getTotalTimeFromQueryPlan(queryPlan):  # queryPlan <- explain_query()
    # last rows of queryPlan is like below
    # ('Planning Time: 1.926 ms'), ('Execution Time: 27.657 ms')
    # --> returns 28.073
    print("\tTime benchmarks : ", queryPlan[-2:])  # LOG - last two rows

    return sum(float(x[0].split(':')[1].replace(' ms', '')) for x in queryPlan[-2:])


def query_createIndex(tableName, columnName):
    return "CREATE INDEX IF NOT EXISTS idx_{tn}_{cn} ON {tn}({cn});".format(tn=tableName, cn=columnName)


def dropIndex_query(tableName, columnName):  # Useless for now
    return "DROP INDEX idx_{tn}_{cn};".format(tn=tableName, cn=columnName)


def drop_all_indexes(cur):
    # Drop all indexes of all tables.
    # #TODO Drop pkey constraints beforehand
    cur.execute(
        "SELECT indexname FROM pg_indexes WHERE schemaname = 'public';")
    indexes = cur.fetchall()
    for index in indexes:
        cur.execute("DROP INDEX IF EXISTS " + index[0] + " CASCADE;")
        # print("DROP INDEX IF EXISTS " + index[0])

# ---- Global Variables ----


queries = [
    "SELECT name FROM instructor WHERE dept_name = 'Biology'",
    "SELECT title FROM course WHERE dept_name = 'Comp. Sci.' AND credits=3",
    "SELECT course_id, title FROM takes natural join course WHERE id='1000'",
    "SELECT sum(credits) FROM takes natural join course WHERE ID = '1000'",
    "SELECT id, sum(credits) FROM takes natural join course GROUP BY id",
    "SELECT DISTINCT s.name FROM student as s natural join (takes natural join course) WHERE dept_name='Comp. Sci.'",
    "SELECT id FROM instructor WHERE id NOT IN (SELECT id FROM teaches)",
    "SELECT id, name FROM instructor WHERE id NOT IN (SELECT id FROM teaches)"
]


# Ideal indexes on columns for each task:
# 1: instructor.dept_name
# 2: course.dept_name, course.credits
# 3: takes.id, course.course_id
# 4: takes.id, course.course_id
# 5: takes.id, course.course_id
# 6: student.id , takes.id , course.course_id, course.dept_name
# 7: instructor.id, teaches.id
# 8: instructor.id, teaches.id
idealIndexes = [
    query_createIndex("instructor", "dept_name"),

    query_createIndex("course", "dept_name") +
    query_createIndex("course", "credits"),

    query_createIndex("takes", "id") +
    query_createIndex("course", "course_id"),

    query_createIndex("takes", "id") +
    query_createIndex("course", "course_id"),

    query_createIndex("takes", "id") +
    query_createIndex("course", "course_id"),

    query_createIndex("student", "id") +
    query_createIndex("takes", "id") +
    query_createIndex("course", "course_id") +
    query_createIndex("course", "dept_name"),

    query_createIndex("instructor", "id") +
    query_createIndex("teaches", "id"),

    query_createIndex("instructor", "id") +
    query_createIndex("teaches", "id"),
]
# Minimal subset of ideal indexes: Golden Index
# course(dept_name, course_id), takes(id), instructor(id), teaches(id)
GOLDENINDEX = query_createIndex("course", "dept_name") + \
    query_createIndex("course", "course_id") + \
    query_createIndex("takes", "id") + \
    query_createIndex("instructor", "id") + \
    query_createIndex("teaches", "id")


# ---- Main ----
def main():
    tasks = []
    for i in range(len(queries)):
        tasks.append({"query": queries[i], "indexQuery": idealIndexes[i]})

    # Keep track of time stats for each task
    timeStats = [[] for i in range(len(tasks))]
    timeStats_golden = timeStats.copy()

    taskNum = 0  # keep track of task number
    for task in tasks:
        print("\n-*- Task", taskNum+1)
        print("    Query:", task["query"])

        try:
            conn = connect2db()
            conn.autocommit = True
            print("\npgsql connection is opened")
            cur = conn.cursor()

            # # First, No indexes
            #  Drop all indexes
            drop_all_indexes(cur)

            print("\t1) running query w/o indexes...")

            records = explain_query(cur, task["query"])
            # optional: can be replaced by getTotalTimeFromQueryPlan() to get Planning + Execution time
            time = getExecuteTimeFromQueryPlan(records)
            timeStats[taskNum].append(time)
            print("\t* Query plan:", records)
            print("\n\t-> Total time:", time, "ms")

            # Second, Test with ideal indexes for each task
            print("\n\t2) running query w/ indexes...")

            print("\t* Index Query:", task["indexQuery"])
            cur.execute(task["indexQuery"])  # create the indexes

            records = explain_query(cur, task["query"])
            time = getExecuteTimeFromQueryPlan(records)
            timeStats[taskNum].append(time)
            print("\t* Query plan:", records)
            print("\n\t-> Total time:", time)

            # Third, Test with golden index
            print("\n\t3) running w/ golden index...")
            drop_all_indexes(cur)  # delete previous indexes to reset
            print("\t* Index Query:", GOLDENINDEX)
            cur.execute(GOLDENINDEX)  # create the indexes

            records = explain_query(cur, task["query"])
            time = getExecuteTimeFromQueryPlan(records)
            timeStats_golden[taskNum].append(time)
            print("\t* Query plan:", records)
            print("\n\t-> Total time:", time)

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

        finally:
            # closing database connection.
            if conn:
                cur.close()
                conn.close()
                print("\npgsql connection is closed")

        taskNum += 1

    # Print time stats
    print("\n\n-*- Time stats: [Not Indexed] -> [Indexed] (ms)")
    for i in range(len(timeStats)):
        print("- Task", i+1, end=": ")
        print("{} -> {} ms".format(timeStats[i][0], timeStats[i][1]))
        print("\tgaind speed: {} %".format(
            timeStats[i][0]/timeStats[i][1]*100 - 100))

    # Print golden index time stats
    print("\n\n-*- Golden index Time stats: [Not Indexed] -> [Indexed] (ms)")
    for i in range(len(timeStats)):
        print("- Task", i+1, end=": ")
        print("{} -> {} ms".format(timeStats[i][0], timeStats[i][1]))
        print("\tgaind speed: {} %".format(
            timeStats[i][0]/timeStats[i][1]*100 - 100))

    print("quiting...")


if __name__ == '__main__':
    main()


''' Example Output
YTU-CE/DBMS/Project on  master [!?] via 🐍 v3.8.11 
❯ /Users/parsa/lib/miniconda3/bin/python /Users/parsa/Projects/YTU-CE/DBMS/Project/controller.py

-*- Task 1
    Query: SELECT name FROM instructor WHERE dept_name = 'Biology'

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.090 ms',), ('Execution Time: 0.020 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=0.00..1.62 rows=1 width=58) (actual time=0.009..0.011 rows=2 loops=1)',), ("  Filter: ((dept_name)::text = 'Biology'::text)",), ('  Rows Removed by Filter: 48',), ('Planning Time: 0.090 ms',), ('Execution Time: 0.020 ms',)]

        -> Total time: 0.02 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_instructor_dept_name ON instructor(dept_name);
        Time benchmarks :  [('Planning Time: 0.083 ms',), ('Execution Time: 0.010 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=0.00..1.62 rows=1 width=58) (actual time=0.005..0.007 rows=2 loops=1)',), ("  Filter: ((dept_name)::text = 'Biology'::text)",), ('  Rows Removed by Filter: 48',), ('Planning Time: 0.083 ms',), ('Execution Time: 0.010 ms',)]

        -> Total time: 0.01

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.076 ms',), ('Execution Time: 0.011 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=0.00..1.62 rows=1 width=58) (actual time=0.004..0.006 rows=2 loops=1)',), ("  Filter: ((dept_name)::text = 'Biology'::text)",), ('  Rows Removed by Filter: 48',), ('Planning Time: 0.076 ms',), ('Execution Time: 0.011 ms',)]

        -> Total time: 0.011

pgsql connection is closed

-*- Task 2
    Query: SELECT title FROM course WHERE dept_name = 'Comp. Sci.' AND credits=3

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.111 ms',), ('Execution Time: 0.023 ms',)]
        * Query plan: [('Seq Scan on course  (cost=0.00..5.00 rows=5 width=17) (actual time=0.006..0.018 rows=3 loops=1)',), ("  Filter: (((dept_name)::text = 'Comp. Sci.'::text) AND (credits = '3'::numeric))",), ('  Rows Removed by Filter: 197',), ('Planning Time: 0.111 ms',), ('Execution Time: 0.023 ms',)]

        -> Total time: 0.023 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_credits ON course(credits);
        Time benchmarks :  [('Planning Time: 0.098 ms',), ('Execution Time: 0.016 ms',)]
        * Query plan: [('Seq Scan on course  (cost=0.00..5.00 rows=5 width=17) (actual time=0.003..0.013 rows=3 loops=1)',), ("  Filter: (((dept_name)::text = 'Comp. Sci.'::text) AND (credits = '3'::numeric))",), ('  Rows Removed by Filter: 197',), ('Planning Time: 0.098 ms',), ('Execution Time: 0.016 ms',)]

        -> Total time: 0.016

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.110 ms',), ('Execution Time: 0.019 ms',)]
        * Query plan: [('Seq Scan on course  (cost=0.00..5.00 rows=5 width=17) (actual time=0.004..0.014 rows=3 loops=1)',), ("  Filter: (((dept_name)::text = 'Comp. Sci.'::text) AND (credits = '3'::numeric))",), ('  Rows Removed by Filter: 197',), ('Planning Time: 0.110 ms',), ('Execution Time: 0.019 ms',)]

        -> Total time: 0.019

pgsql connection is closed

-*- Task 3
    Query: SELECT course_id, title FROM takes natural join course WHERE id='1000'

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.315 ms',), ('Execution Time: 1.341 ms',)]
        * Query plan: [('Hash Join  (cost=6.50..601.71 rows=15 width=21) (actual time=0.091..1.330 rows=13 loops=1)',), ('  Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('  ->  Seq Scan on takes  (cost=0.00..595.00 rows=15 width=4) (actual time=0.050..1.287 rows=13 loops=1)',), ("        Filter: ((id)::text = '1000'::text)",), ('        Rows Removed by Filter: 29987',), ('  ->  Hash  (cost=4.00..4.00 rows=200 width=21) (actual time=0.035..0.035 rows=200 loops=1)',), ('        Buckets: 1024  Batches: 1  Memory Usage: 19kB',), ('        ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=21) (actual time=0.004..0.015 rows=200 loops=1)',), ('Planning Time: 0.315 ms',), ('Execution Time: 1.341 ms',)]

        -> Total time: 1.341 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);
        Time benchmarks :  [('Planning Time: 0.286 ms',), ('Execution Time: 0.090 ms',)]
        * Query plan: [('Hash Join  (cost=10.90..59.55 rows=15 width=21) (actual time=0.064..0.076 rows=13 loops=1)',), ('  Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('  ->  Bitmap Heap Scan on takes  (cost=4.40..52.84 rows=15 width=4) (actual time=0.032..0.041 rows=13 loops=1)',), ("        Recheck Cond: ((id)::text = '1000'::text)",), ('        Heap Blocks: exact=13',), ('        ->  Bitmap Index Scan on idx_takes_id  (cost=0.00..4.40 rows=15 width=0) (actual time=0.029..0.029 rows=13 loops=1)',), ("              Index Cond: ((id)::text = '1000'::text)",), ('  ->  Hash  (cost=4.00..4.00 rows=200 width=21) (actual time=0.029..0.029 rows=200 loops=1)',), ('        Buckets: 1024  Batches: 1  Memory Usage: 19kB',), ('        ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=21) (actual time=0.003..0.012 rows=200 loops=1)',), ('Planning Time: 0.286 ms',), ('Execution Time: 0.090 ms',)]

        -> Total time: 0.09

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.294 ms',), ('Execution Time: 0.069 ms',)]
        * Query plan: [('Hash Join  (cost=10.90..59.55 rows=15 width=21) (actual time=0.048..0.059 rows=13 loops=1)',), ('  Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('  ->  Bitmap Heap Scan on takes  (cost=4.40..52.84 rows=15 width=4) (actual time=0.016..0.025 rows=13 loops=1)',), ("        Recheck Cond: ((id)::text = '1000'::text)",), ('        Heap Blocks: exact=13',), ('        ->  Bitmap Index Scan on idx_takes_id  (cost=0.00..4.40 rows=15 width=0) (actual time=0.014..0.014 rows=13 loops=1)',), ("              Index Cond: ((id)::text = '1000'::text)",), ('  ->  Hash  (cost=4.00..4.00 rows=200 width=21) (actual time=0.029..0.029 rows=200 loops=1)',), ('        Buckets: 1024  Batches: 1  Memory Usage: 19kB',), ('        ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=21) (actual time=0.003..0.013 rows=200 loops=1)',), ('Planning Time: 0.294 ms',), ('Execution Time: 0.069 ms',)]

        -> Total time: 0.069

pgsql connection is closed

-*- Task 4
    Query: SELECT sum(credits) FROM takes natural join course WHERE ID = '1000'

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.342 ms',), ('Execution Time: 1.297 ms',)]
        * Query plan: [('Aggregate  (cost=601.75..601.76 rows=1 width=32) (actual time=1.274..1.275 rows=1 loops=1)',), ('  ->  Hash Join  (cost=6.50..601.71 rows=15 width=5) (actual time=0.091..1.263 rows=13 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Seq Scan on takes  (cost=0.00..595.00 rows=15 width=4) (actual time=0.051..1.220 rows=13 loops=1)',), ("              Filter: ((id)::text = '1000'::text)",), ('              Rows Removed by Filter: 29987',), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.037..0.037 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.004..0.016 rows=200 loops=1)',), ('Planning Time: 0.342 ms',), ('Execution Time: 1.297 ms',)]

        -> Total time: 1.297 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);
        Time benchmarks :  [('Planning Time: 0.276 ms',), ('Execution Time: 0.079 ms',)]
        * Query plan: [('Aggregate  (cost=59.59..59.60 rows=1 width=32) (actual time=0.062..0.063 rows=1 loops=1)',), ('  ->  Hash Join  (cost=10.90..59.55 rows=15 width=5) (actual time=0.047..0.059 rows=13 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Bitmap Heap Scan on takes  (cost=4.40..52.84 rows=15 width=4) (actual time=0.019..0.029 rows=13 loops=1)',), ("              Recheck Cond: ((id)::text = '1000'::text)",), ('              Heap Blocks: exact=13',), ('              ->  Bitmap Index Scan on idx_takes_id  (cost=0.00..4.40 rows=15 width=0) (actual time=0.016..0.017 rows=13 loops=1)',), ("                    Index Cond: ((id)::text = '1000'::text)",), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.026..0.026 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.003..0.013 rows=200 loops=1)',), ('Planning Time: 0.276 ms',), ('Execution Time: 0.079 ms',)]

        -> Total time: 0.079

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.310 ms',), ('Execution Time: 0.093 ms',)]
        * Query plan: [('Aggregate  (cost=59.59..59.60 rows=1 width=32) (actual time=0.079..0.080 rows=1 loops=1)',), ('  ->  Hash Join  (cost=10.90..59.55 rows=15 width=5) (actual time=0.064..0.075 rows=13 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Bitmap Heap Scan on takes  (cost=4.40..52.84 rows=15 width=4) (actual time=0.022..0.031 rows=13 loops=1)',), ("              Recheck Cond: ((id)::text = '1000'::text)",), ('              Heap Blocks: exact=13',), ('              ->  Bitmap Index Scan on idx_takes_id  (cost=0.00..4.40 rows=15 width=0) (actual time=0.019..0.019 rows=13 loops=1)',), ("                    Index Cond: ((id)::text = '1000'::text)",), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.038..0.038 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.006..0.024 rows=200 loops=1)',), ('Planning Time: 0.310 ms',), ('Execution Time: 0.093 ms',)]

        -> Total time: 0.093

pgsql connection is closed

-*- Task 5
    Query: SELECT id, sum(credits) FROM takes natural join course GROUP BY id

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.226 ms',), ('Execution Time: 8.344 ms',)]
        * Query plan: [('HashAggregate  (cost=1089.00..1114.00 rows=2000 width=37) (actual time=8.097..8.289 rows=2000 loops=1)',), ('  Group Key: takes.id',), ('  Batches: 1  Memory Usage: 1137kB',), ('  ->  Hash Join  (cost=6.50..939.00 rows=30000 width=10) (actual time=0.035..4.470 rows=30000 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.003..0.983 rows=30000 loops=1)',), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.028..0.028 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.004..0.015 rows=200 loops=1)',), ('Planning Time: 0.226 ms',), ('Execution Time: 8.344 ms',)]

        -> Total time: 8.344 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);
        Time benchmarks :  [('Planning Time: 0.290 ms',), ('Execution Time: 7.776 ms',)]
        * Query plan: [('HashAggregate  (cost=1089.00..1114.00 rows=2000 width=37) (actual time=7.526..7.725 rows=2000 loops=1)',), ('  Group Key: takes.id',), ('  Batches: 1  Memory Usage: 1137kB',), ('  ->  Hash Join  (cost=6.50..939.00 rows=30000 width=10) (actual time=0.031..4.278 rows=30000 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.002..0.844 rows=30000 loops=1)',), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.025..0.025 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.003..0.012 rows=200 loops=1)',), ('Planning Time: 0.290 ms',), ('Execution Time: 7.776 ms',)]

        -> Total time: 7.776

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.282 ms',), ('Execution Time: 8.055 ms',)]
        * Query plan: [('HashAggregate  (cost=1089.00..1114.00 rows=2000 width=37) (actual time=7.769..7.956 rows=2000 loops=1)',), ('  Group Key: takes.id',), ('  Batches: 1  Memory Usage: 1137kB',), ('  ->  Hash Join  (cost=6.50..939.00 rows=30000 width=10) (actual time=0.035..4.393 rows=30000 loops=1)',), ('        Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('        ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.002..0.856 rows=30000 loops=1)',), ('        ->  Hash  (cost=4.00..4.00 rows=200 width=9) (actual time=0.026..0.027 rows=200 loops=1)',), ('              Buckets: 1024  Batches: 1  Memory Usage: 17kB',), ('              ->  Seq Scan on course  (cost=0.00..4.00 rows=200 width=9) (actual time=0.003..0.013 rows=200 loops=1)',), ('Planning Time: 0.282 ms',), ('Execution Time: 8.055 ms',)]

        -> Total time: 8.055

pgsql connection is closed

-*- Task 6
    Query: SELECT DISTINCT s.name FROM student as s natural join (takes natural join course) WHERE dept_name='Comp. Sci.'

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.749 ms',), ('Execution Time: 2.974 ms',)]
        * Query plan: [('Unique  (cost=702.48..702.88 rows=81 width=6) (actual time=2.951..2.958 rows=55 loops=1)',), ('  ->  Sort  (cost=702.48..702.68 rows=81 width=6) (actual time=2.951..2.952 rows=70 loops=1)',), ('        Sort Key: s.name',), ('        Sort Method: quicksort  Memory: 28kB',), ('        ->  Hash Join  (cost=45.98..699.91 rows=81 width=6) (actual time=0.274..2.793 rows=70 loops=1)',), ('              Hash Cond: ((takes.id)::text = (s.id)::text)',), ('              ->  Hash Join  (cost=4.62..652.12 rows=1500 width=14) (actual time=0.047..2.556 rows=1260 loops=1)',), ('                    Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('                    ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.003..0.884 rows=30000 loops=1)',), ('                    ->  Hash  (cost=4.50..4.50 rows=10 width=13) (actual time=0.038..0.038 rows=10 loops=1)',), ('                          Buckets: 1024  Batches: 1  Memory Usage: 9kB',), ('                          ->  Seq Scan on course  (cost=0.00..4.50 rows=10 width=13) (actual time=0.005..0.016 rows=10 loops=1)',), ("                                Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                                Rows Removed by Filter: 190',), ('              ->  Hash  (cost=40.00..40.00 rows=108 width=20) (actual time=0.165..0.165 rows=108 loops=1)',), ('                    Buckets: 1024  Batches: 1  Memory Usage: 14kB',), ('                    ->  Seq Scan on student s  (cost=0.00..40.00 rows=108 width=20) (actual time=0.008..0.155 rows=108 loops=1)',), ("                          Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                          Rows Removed by Filter: 1892',), ('Planning Time: 0.749 ms',), ('Execution Time: 2.974 ms',)]

        -> Total time: 2.974 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_student_id ON student(id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);
        Time benchmarks :  [('Planning Time: 0.860 ms',), ('Execution Time: 2.822 ms',)]
        * Query plan: [('Unique  (cost=702.48..702.88 rows=81 width=6) (actual time=2.798..2.805 rows=55 loops=1)',), ('  ->  Sort  (cost=702.48..702.68 rows=81 width=6) (actual time=2.798..2.800 rows=70 loops=1)',), ('        Sort Key: s.name',), ('        Sort Method: quicksort  Memory: 28kB',), ('        ->  Hash Join  (cost=45.98..699.91 rows=81 width=6) (actual time=0.177..2.642 rows=70 loops=1)',), ('              Hash Cond: ((takes.id)::text = (s.id)::text)',), ('              ->  Hash Join  (cost=4.62..652.12 rows=1500 width=14) (actual time=0.019..2.470 rows=1260 loops=1)',), ('                    Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('                    ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.002..0.798 rows=30000 loops=1)',), ('                    ->  Hash  (cost=4.50..4.50 rows=10 width=13) (actual time=0.013..0.014 rows=10 loops=1)',), ('                          Buckets: 1024  Batches: 1  Memory Usage: 9kB',), ('                          ->  Seq Scan on course  (cost=0.00..4.50 rows=10 width=13) (actual time=0.003..0.012 rows=10 loops=1)',), ("                                Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                                Rows Removed by Filter: 190',), ('              ->  Hash  (cost=40.00..40.00 rows=108 width=20) (actual time=0.103..0.104 rows=108 loops=1)',), ('                    Buckets: 1024  Batches: 1  Memory Usage: 14kB',), ('                    ->  Seq Scan on student s  (cost=0.00..40.00 rows=108 width=20) (actual time=0.003..0.091 rows=108 loops=1)',), ("                          Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                          Rows Removed by Filter: 1892',), ('Planning Time: 0.860 ms',), ('Execution Time: 2.822 ms',)]

        -> Total time: 2.822

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.721 ms',), ('Execution Time: 2.888 ms',)]
        * Query plan: [('Unique  (cost=702.48..702.88 rows=81 width=6) (actual time=2.864..2.872 rows=55 loops=1)',), ('  ->  Sort  (cost=702.48..702.68 rows=81 width=6) (actual time=2.864..2.866 rows=70 loops=1)',), ('        Sort Key: s.name',), ('        Sort Method: quicksort  Memory: 28kB',), ('        ->  Hash Join  (cost=45.98..699.91 rows=81 width=6) (actual time=0.181..2.706 rows=70 loops=1)',), ('              Hash Cond: ((takes.id)::text = (s.id)::text)',), ('              ->  Hash Join  (cost=4.62..652.12 rows=1500 width=14) (actual time=0.025..2.532 rows=1260 loops=1)',), ('                    Hash Cond: ((takes.course_id)::text = (course.course_id)::text)',), ('                    ->  Seq Scan on takes  (cost=0.00..520.00 rows=30000 width=9) (actual time=0.002..0.798 rows=30000 loops=1)',), ('                    ->  Hash  (cost=4.50..4.50 rows=10 width=13) (actual time=0.018..0.018 rows=10 loops=1)',), ('                          Buckets: 1024  Batches: 1  Memory Usage: 9kB',), ('                          ->  Seq Scan on course  (cost=0.00..4.50 rows=10 width=13) (actual time=0.003..0.012 rows=10 loops=1)',), ("                                Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                                Rows Removed by Filter: 190',), ('              ->  Hash  (cost=40.00..40.00 rows=108 width=20) (actual time=0.102..0.102 rows=108 loops=1)',), ('                    Buckets: 1024  Batches: 1  Memory Usage: 14kB',), ('                    ->  Seq Scan on student s  (cost=0.00..40.00 rows=108 width=20) (actual time=0.003..0.092 rows=108 loops=1)',), ("                          Filter: ((dept_name)::text = 'Comp. Sci.'::text)",), ('                          Rows Removed by Filter: 1892',), ('Planning Time: 0.721 ms',), ('Execution Time: 2.888 ms',)]

        -> Total time: 2.888

pgsql connection is closed

-*- Task 7
    Query: SELECT id FROM instructor WHERE id NOT IN (SELECT id FROM teaches)

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.057 ms',), ('Execution Time: 0.045 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=24) (actual time=0.022..0.027 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.002..0.006 rows=100 loops=1)',), ('Planning Time: 0.057 ms',), ('Execution Time: 0.045 ms',)]

        -> Total time: 0.045 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.101 ms',), ('Execution Time: 0.031 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=24) (actual time=0.020..0.025 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.003..0.006 rows=100 loops=1)',), ('Planning Time: 0.101 ms',), ('Execution Time: 0.031 ms',)]

        -> Total time: 0.031

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.109 ms',), ('Execution Time: 0.037 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=24) (actual time=0.022..0.027 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.001..0.005 rows=100 loops=1)',), ('Planning Time: 0.109 ms',), ('Execution Time: 0.037 ms',)]

        -> Total time: 0.037

pgsql connection is closed

-*- Task 8
    Query: SELECT id, name FROM instructor WHERE id NOT IN (SELECT id FROM teaches)

pgsql connection is opened
        1) running query w/o indexes...
        Time benchmarks :  [('Planning Time: 0.052 ms',), ('Execution Time: 0.040 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=82) (actual time=0.022..0.027 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.002..0.006 rows=100 loops=1)',), ('Planning Time: 0.052 ms',), ('Execution Time: 0.040 ms',)]

        -> Total time: 0.04 ms

        2) running query w/ indexes...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.077 ms',), ('Execution Time: 0.026 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=82) (actual time=0.017..0.022 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.001..0.004 rows=100 loops=1)',), ('Planning Time: 0.077 ms',), ('Execution Time: 0.026 ms',)]

        -> Total time: 0.026

        3) running w/ golden index...
        * Index Query: CREATE INDEX IF NOT EXISTS idx_course_dept_name ON course(dept_name);CREATE INDEX IF NOT EXISTS idx_course_course_id ON course(course_id);CREATE INDEX IF NOT EXISTS idx_takes_id ON takes(id);CREATE INDEX IF NOT EXISTS idx_instructor_id ON instructor(id);CREATE INDEX IF NOT EXISTS idx_teaches_id ON teaches(id);
        Time benchmarks :  [('Planning Time: 0.106 ms',), ('Execution Time: 0.034 ms',)]
        * Query plan: [('Seq Scan on instructor  (cost=2.25..3.88 rows=25 width=82) (actual time=0.019..0.024 rows=19 loops=1)',), ('  Filter: (NOT (hashed SubPlan 1))',), ('  Rows Removed by Filter: 31',), ('  SubPlan 1',), ('    ->  Seq Scan on teaches  (cost=0.00..2.00 rows=100 width=5) (actual time=0.001..0.005 rows=100 loops=1)',), ('Planning Time: 0.106 ms',), ('Execution Time: 0.034 ms',)]

        -> Total time: 0.034

pgsql connection is closed


-*- Time stats: [Not Indexed] -> [Indexed] (ms)
- Task 1: 0.02 -> 0.01 ms
        gaind speed: 100.0 %
- Task 2: 0.023 -> 0.016 ms
        gaind speed: 43.75 %
- Task 3: 1.341 -> 0.09 ms
        gaind speed: 1390.0 %
- Task 4: 1.297 -> 0.079 ms
        gaind speed: 1541.7721518987341 %
- Task 5: 8.344 -> 7.776 ms
        gaind speed: 7.304526748971199 %
- Task 6: 2.974 -> 2.822 ms
        gaind speed: 5.38625088589653 %
- Task 7: 0.045 -> 0.031 ms
        gaind speed: 45.16129032258064 %
- Task 8: 0.04 -> 0.026 ms
        gaind speed: 53.84615384615387 %


-*- Golden index Time stats: [Not Indexed] -> [Indexed] (ms)
- Task 1: 0.02 -> 0.01 ms
        gaind speed: 100.0 %
- Task 2: 0.023 -> 0.016 ms
        gaind speed: 43.75 %
- Task 3: 1.341 -> 0.09 ms
        gaind speed: 1390.0 %
- Task 4: 1.297 -> 0.079 ms
        gaind speed: 1541.7721518987341 %
- Task 5: 8.344 -> 7.776 ms
        gaind speed: 7.304526748971199 %
- Task 6: 2.974 -> 2.822 ms
        gaind speed: 5.38625088589653 %
- Task 7: 0.045 -> 0.031 ms
        gaind speed: 45.16129032258064 %
- Task 8: 0.04 -> 0.026 ms
        gaind speed: 53.84615384615387 %

quiting...

'''
