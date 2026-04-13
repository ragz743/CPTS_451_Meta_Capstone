import oracledb
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE


def get_connection():
    return oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        service_name=DB_SERVICE
    )


def fetch_all(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or {})
        columns = [col[0] for col in cur.description]
        rows = cur.fetchall()
        results = [dict(zip(columns, row)) for row in rows]
        return results
    finally:
        cur.close()
        conn.close()


def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or {})
        conn.commit()
    finally:
        cur.close()
        conn.close()