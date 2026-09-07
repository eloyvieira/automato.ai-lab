from mysql.connector.pooling import MySQLConnectionPool
from core.config import get_settings

_pool: MySQLConnectionPool | None = None

def get_mysql_pool() -> MySQLConnectionPool:
    global _pool
    if _pool is None:
        s = get_settings()
        _pool = MySQLConnectionPool(
            pool_name='ai_lab_pool', pool_size=s.mysql_pool_size,
            host=s.mysql_host, port=s.mysql_port, database=s.mysql_database,
            user=s.mysql_user, password=s.mysql_password,
        )
    return _pool

def fetch_all(query: str, params: tuple | dict | None = None) -> list[dict]:
    conn = get_mysql_pool().get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()

def fetch_one(query: str, params: tuple | dict | None = None) -> dict | None:
    rows = fetch_all(query, params)
    return rows[0] if rows else None
