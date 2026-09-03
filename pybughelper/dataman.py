import sqlite3
import logging

class SQLX:
    """
    A lightweight, robust wrapper for managing SQLite database engines.
    Handles connection lifecycles, row conversions to dict formats, and safe rollbacks.
    """
    def __init__(self, db_path):
        """Initializes connection and configures row processing factory defaults."""
        self.data = sqlite3.connect(db_path)
        # Set row_factory BEFORE creating the cursor so it inherits the property
        self.data.row_factory = sqlite3.Row
        self.cursor = self.data.cursor()

    def __enter__(self):
        """Allows class operations to be executed cleanly inside with blocks."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Handles closing out connections and ensures exceptions bubble up correctly."""
        self.close()
        return False  # Do NOT suppress exceptions; let Flask handle the error trace

    def close(self):
        """Safely commits processing records, terminates cursor states, and drops connections."""
        if self.data:
            try:
                self.cursor.close()
                self.data.close()
            except Exception as e:
                logging.error(f"Error closing database connection: {e}")

    def create_table(self, table, schema):
        """Builds target tables cleanly inside environments if missing."""
        query = f"CREATE TABLE IF NOT EXISTS {table} ({schema})"
        try:
            self.cursor.execute(query)
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            raise e

    def _ensure_tuple(self, params):
        """Standardizes single arguments or collections into query-safe tuple variables."""
        if isinstance(params, (list, tuple)):
            return tuple(params)
        return (params,) if params is not None and params != () else ()

    def select_all(self, table, where_clause=None, where_params=()):
        """Queries entire contents matching parameter scopes."""
        query = f"SELECT * FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, self._ensure_tuple(where_params))
        # row_factory makes rows behave like mappings, converting to native dicts safely
        return [dict(row) for row in self.cursor.fetchall()]

    def select_one(self, table, where_clause=None, where_params=()):
        """Queries structural matches returning only primary record targets."""
        query = f"SELECT * FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, self._ensure_tuple(where_params))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def insert(self, table, data_dict):
        """Maps dictionary fields cleanly to database records with safe rollback handling."""
        columns = ', '.join([f'"{col}"' for col in data_dict.keys()])
        placeholders = ', '.join(['?'] * len(data_dict))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, tuple(data_dict.values()))
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            raise e

    def update(self, table, values, where_clause, where_params=()):
        """Updates database rows safely using parameterized structures."""
        set_clause = ', '.join([f'"{col}" = ?' for col in values.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        execute_params = tuple(values.values()) + self._ensure_tuple(where_params)
        try:
            self.cursor.execute(query, execute_params)
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            raise e

    def drop(self, table):
        """Permanently deletes an explicit target dataset from disk files."""
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            raise e

    def remove(self, table, where_clause, where_params=()):
        """Deletes target row records cleanly using strict identifier parameter tracking."""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        try:
            self.cursor.execute(query, self._ensure_tuple(where_params))
            self.data.commit()
        except Exception as e:
            self.data.rollback()
            raise e
