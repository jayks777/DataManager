import os

from peewee import SqliteDatabase


class DatabaseConnection:
    def __init__(self, db_type, name, database):
        self.db_type = db_type
        self.name = name
        self.database = database


class DatabaseManager:
    def __init__(self):
        self.connections = {}
        self.current = None

    def connect_sqlite(self, path):
        name = os.path.basename(path)
        db = SqliteDatabase(path)
        conn = DatabaseConnection("sqlite", name, db)
        self.connections[name] = conn
        self.current = conn
        return conn

    def create_sqlite(self, path, overwrite=False):
        if os.path.exists(path) and not overwrite:
            raise FileExistsError(f"Arquivo ja existe: {path}")
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8"):
                pass
        return self.connect_sqlite(path)

    def create_table(self, table_name, columns):
        if not self.current:
            raise RuntimeError("Nenhum banco conectado")
        if not table_name:
            raise ValueError("Nome da tabela vazio")
        if not columns:
            raise ValueError("Nenhuma coluna definida")
        sanitized = table_name.strip().replace(" ", "_")
        cols_sql = ", ".join(columns)
        db = self.current.database
        db.connect(reuse_if_open=True)
        db.execute_sql(f"CREATE TABLE IF NOT EXISTS {sanitized} ({cols_sql})")

    def get_tables(self):
        if not self.current:
            return []
        db = self.current.database
        db.connect(reuse_if_open=True)
        # Hide SQLite internal tables (ex.: sqlite_sequence) from the UI.
        return [name for name in db.get_tables() if not name.lower().startswith("sqlite_")]

    def get_columns(self, table):
        db = self.current.database
        db.connect(reuse_if_open=True)
        return db.get_columns(table)

    def select_all(self, table):
        db = self.current.database
        cursor = db.execute_sql(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return columns, rows

    def insert(self, table, data):
        db = self.current.database
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = list(data.values())
        db.execute_sql(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            values,
        )

    def update(self, table, pk_name, pk_value, data):
        db = self.current.database
        set_clause = ", ".join([f"{k}=?" for k in data])
        values = list(data.values())
        values.append(pk_value)
        db.execute_sql(
            f"UPDATE {table} SET {set_clause} WHERE {pk_name}=?",
            values,
        )

    def delete(self, table, pk_name, pk_value):
        db = self.current.database
        db.execute_sql(
            f"DELETE FROM {table} WHERE {pk_name}=?",
            (pk_value,),
        )

    def drop_table(self, table_name):
        if not self.current:
            raise RuntimeError("Nenhum banco conectado")
        if not table_name:
            raise ValueError("Nome da tabela vazio")
        sanitized = table_name.strip().replace(" ", "_")
        db = self.current.database
        db.connect(reuse_if_open=True)
        db.execute_sql(f"DROP TABLE IF EXISTS {sanitized}")


db_manager = DatabaseManager()
