import os

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class DatabaseHandler:
    def __init__(self):
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        dbname = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            cursor_factory=RealDictCursor
        )
        self._create_tables()

    def _create_tables(self):
        with self.conn.cursor() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS file_index (
                  id SERIAL PRIMARY KEY,
                  file_name TEXT,
                  file_path TEXT UNIQUE,
                  file_type TEXT NULL,
                  file_content TEXT,
                  indexed_at TIMESTAMP,
                  file_size BIGINT,
                  last_access_time TIMESTAMP NULL,
                  directory_depth INTEGER NULL,
                  index_score DOUBLE PRECISION NULL
                );
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                  id SERIAL PRIMARY KEY,
                  query TEXT NOT NULL,
                  searched_at TIMESTAMP NOT NULL DEFAULT now()
                );
            """)
        self.conn.commit()

    def insert_file(self, fi):
        with self.conn.cursor() as c:
            c.execute("""
                INSERT INTO file_index
                  (file_name, file_path, file_type, file_content,
                   indexed_at, file_size, last_access_time,
                   directory_depth, index_score)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (file_path) DO UPDATE SET
                  file_name        = EXCLUDED.file_name,
                  file_type        = EXCLUDED.file_type,
                  file_content     = EXCLUDED.file_content,
                  indexed_at       = EXCLUDED.indexed_at,
                  file_size        = EXCLUDED.file_size,
                  last_access_time = EXCLUDED.last_access_time,
                  directory_depth  = EXCLUDED.directory_depth,
                  index_score      = EXCLUDED.index_score;
            """, (
                fi['name'], fi['path'], fi.get('type'), fi.get('content'),
                datetime.fromisoformat(fi['indexed_at']), fi.get('size'),
                datetime.fromisoformat(fi.get('accessed')) if fi.get('accessed') else None,
                fi.get('depth'), fi.get('index_score')
            ))
        self.conn.commit()

    def list_all(self):
        with self.conn.cursor() as c:
            c.execute(
                "SELECT file_name, file_path, file_type, file_content, index_score, directory_depth "
                "FROM file_index;"
            )
            return c.fetchall()

    def record_query(self, query):
        with self.conn.cursor() as c:
            c.execute("INSERT INTO search_history (query) VALUES (%s);", (query,))
        self.conn.commit()

    def suggest(self, prefix, limit=10):
        with self.conn.cursor() as c:
            c.execute("""
                SELECT query FROM (
                  SELECT query, MAX(searched_at) AS last
                    FROM search_history
                   WHERE query ILIKE %s
                GROUP BY query
                ) AS sub
                ORDER BY sub.last DESC
                LIMIT %s;
            """, (prefix + '%', limit))
            rows = c.fetchall()
        return [r['query'] for r in rows]
