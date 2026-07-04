import psycopg2 

def db_init():
    conn = psycopg2.connect(
        host="localhost",
        database="ppe_db",
        user="postgres",
        password="1234"
        )
    cur = conn.cursor()

    cur.execute("""
       CREATE TABLE IF NOT EXISIS violations(
                id SERIAL PRIMARY KEY,
                person_id INTEGER,
                violation_type TEXT,
                timestamp timestamp TIMESTAMP DEFAULT NOW(),
                image_path TEXT
                )
     
    """)

    conn.commit()
    conn.close()
    cur.close()


def insert_violation(person_id, violation_type, time, image_path):
    conn = psycopg2.connect(
        host="localhost",
        database="ppe_db",
        user="postgres",
        password="1234"
        )
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO violations (person_id, violation_type, timestamp, image_path) VALUES (%s,%s,%s,%s);",
        (person_id, violation_type, time, image_path)
    )

    conn.commit()
    conn.close()
    cur.close()

def get_all_violation():
    conn = psycopg2.connect(
        host="localhost",
        database="ppe_db",
        user="postgres",
        password="1234"
        )
    cur = conn.cursor()

    cur.execute(
        "SELECT person_id, violation_type, timestamp, image_path FROM violations"
    )

    rows = cur.fetchall()
    conn.close()
    cur.close()

    return [{"person_id" : r[0], "violation_type" : r[1], "timestamp" : r[2], "image_path" : r[3]} for r in rows]

def get_violation_by_date(date):
    conn = psycopg2.connect(
        host="localhost",
        database="ppe_db",
        user="postgres",
        password="1234"
        )
    cur = conn.cursor()

    cur.execute(
        "SELECT person_id, violation_type, image_path FROM violations WHERE timestamp = %s",
        (date,)
    )

    rows = cur.fetchall()
    conn.close()
    cur.close()

    return  [{"person_id" : r[0], "violation_type" : r[1], "image_path" : r[2]} for r in rows]
  
def get_violation_by_id(person_id):
    conn = psycopg2.connect(
        host="localhost",
        database="ppe_db",
        user="postgres",
        password="1234"
        )
    cur = conn.cursor()

    cur.execute(
        "SELECT violation_type, timestamp, image_path FROM violations WHERE person_id = %s",
        (person_id,)
    )

    rows = cur.fetchall()
    conn.close()
    cur.close()

    return [{"violation_type" : r[0], "timestamp" : r[1], "image_path" : r[2]} for r in rows]
