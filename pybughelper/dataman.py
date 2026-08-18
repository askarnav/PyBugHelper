import sqlite3


class SQLX:
    """
    A lightweight, robust wrapper for managing SQLite database engines.

    Provides high-level abstraction patterns for performing basic CRUD operations
    safely using clean python context execution managers. Handles connection
    lifecycles, row conversions to native dict formats, and tuple verification.
    """
    def __init__(self, db_path):
        """
        Initializes the connection and configures row processing factory defaults.

        Args:
            db_path (str): The physical filesystem string location path pointing
                          to target database files (.db, .sqlite).
        """
        self.data = sqlite3.connect(db_path)
        self.data.row_factory = sqlite3.Row
        self.cursor = self.data.cursor()

    def __enter__(self):
        """Allows class operations to be executed cleanly inside with blocks."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Handles closing out connection loops automatically when block terminates."""
        self.close()

    def close(self):
        """Safely commits processing records, terminates cursor states, and drops connections."""
        if self.data:
            self.cursor.close()
            self.data.close()

    def create_table(self, table, schema):
        """
        Builds target tables cleanly inside environments if missing.

        Args:
            table (str): Target alphanumeric identifier name string for initialization.
            schema (str): Standard schema command structures (e.g., 'id INTEGER PRIMARY KEY').
        """
        query = f"CREATE TABLE IF NOT EXISTS {table} ({schema})"
        self.cursor.execute(query)
        self.data.commit()

    # noinspection PyMethodMayBeStatic
    def _ensure_tuple(self, params):
        """Standardizes single arguments or collections into query-safe tuple variables."""
        if isinstance(params, (list, tuple)):
            return tuple(params)
        return (params,) if params is not None and params != () else ()

    def select_all(self, table, where_clause=None, where_params=()):
        """
        Queries entire contents matching parameter scopes.

        Args:
            table (str): Target table name identifier.
            where_clause (str, optional): Target SQL filter expression strings.
            where_params (tuple/list/any, optional): Dynamic parameter variable arguments.

        Returns:
            list[dict]: Array records unpacked as key-value pairings.
        """
        query = f"SELECT * FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, self._ensure_tuple(where_params))
        return [dict(row) for row in self.cursor.fetchall()]

    def select_one(self, table, where_clause=None, where_params=()):
        """
        Queries structural matches returning only primary record targets.

        Args:
            table (str): Target database table workspace.
            where_clause (str, optional): Target filter queries.
            where_params (tuple/any, optional): Safe sanitized tracking options.

        Returns:
            dict | None: Extracted dictionary object records if targeted.
        """
        query = f"SELECT * FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        self.cursor.execute(query, self._ensure_tuple(where_params))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def insert(self, table, data_dict):
        """
        Maps dictionary fields cleanly to database records.

        Args:
            table (str): Processing storage workspace table identifier.
            data_dict (dict): Target data bindings format mapping schemas.
        """
        columns = ', '.join([f'"{col}"' for col in data_dict.keys()])
        placeholders = ', '.join(['?'] * len(data_dict))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, tuple(data_dict.values()))
        self.data.commit()

    def update(self, table, values, where_clause, where_params=()):
        """
        Updates database rows safely using parameterized structures.

        Args:
            table (str): Core dataset storage destination identifier.
            values (dict): Modified data pairing states to persist.
            where_clause (str): Filtering logic constraint boundary.
            where_params (tuple/any, optional): Argument inputs targeting conditions safely.
        """
        set_clause = ', '.join([f'"{col}" = ?' for col in values.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        execute_params = tuple(values.values()) + self._ensure_tuple(where_params)
        self.cursor.execute(query, execute_params)
        self.data.commit()

    def drop(self, table):
        """Permanently deletes an explicit target dataset from disk files."""
        self.cursor.execute(f"DROP TABLE IF EXISTS {table}")
        self.data.commit()

    def remove(self, table, where_clause, where_params=()):
        """Deletes target row records cleanly using strict identifier parameter tracking."""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.cursor.execute(query, self._ensure_tuple(where_params))
        self.data.commit()
