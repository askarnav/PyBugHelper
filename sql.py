import sqlite3


class SQLX:
    def __init__(self, data):
        self.data = sqlite3.connect(data)
        self.data.row_factory = sqlite3.Row
        self.cursor = self.data.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.data:
            self.cursor.close()
            self.data.close()

    def create_table(self, table, schema):
        query = f"CREATE TABLE IF NOT EXISTS '{table}' ({schema})"
        self.cursor.execute(query)
        self.data.commit()

    def select_all(self, table, where_clause=None, where_params=()):
        query = f"SELECT * FROM '{table}'"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, tuple(where_params))
        return [dict(row) for row in self.cursor.fetchall()]

    def select_one(self, table, where_clause=None, where_params=()):
        query = f"SELECT * FROM '{table}'"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, tuple(where_params))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def insert(self, table, values):
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO '{table}' VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.data.commit()

    def update(self, table, values, where_clause, where_params=()):
        set_clause = ', '.join([f"'{col}' = ?" for col in values.keys()])
        query = f"UPDATE '{table}' SET {set_clause} WHERE {where_clause}"
        execute_params = tuple(values.values()) + tuple(where_params)
        self.cursor.execute(query, execute_params)
        self.data.commit()

    def drop(self, table):
        self.cursor.execute(f"DROP TABLE IF EXISTS '{table}'")
        self.data.commit()

    def remove(self, table, where_clause, where_params=()):
        query = f"DELETE FROM '{table}' WHERE {where_clause}"
        self.cursor.execute(query, tuple(where_params))
        self.data.commit()



