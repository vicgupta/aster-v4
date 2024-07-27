import sqlite3
import hashlib

class SQLModel:
    def __init__(self, db_name: str):
        if not db_name:
            raise ValueError("Please provide a database name")

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name: str, columns: dict):
        column_defs = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
        self.cursor.execute(query)
        self.conn.commit()

    def drop_table(self, table_name: str):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(query)
        self.conn.commit()

    def insert(self, table_name: str, data: dict) -> int:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def select(self, table_name: str, columns: list = None, where: str = None) -> list:
        columns_part = ", ".join(columns) if columns else "*"
        query = f"SELECT {columns_part} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in rows
        ]

    def update(self, table_name: str, data: dict, where: str):
        set_clause = ", ".join(f"{name} = ?" for name in data)
        values = tuple(data.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete(self, table_name: str, where: str):
        query = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(query)
        self.conn.commit()

    def login(self, table_name: str, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        Args:
            table_name (str): The name of the table containing user credentials.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = f"SELECT * FROM {table_name} WHERE email = ? AND password = ?"
        self.cursor.execute(query, (email, hashed_password))
        user = self.cursor.fetchone()
        return user is not None

    def signup(self, table_name: str, email: str, password: str):
        """
        Registers a new user with email and password.

        Args:
            table_name (str): The name of the table containing user credentials.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if signup is successful, False if email already exists.
        """
        # Check if the email already exists
        if self.select(table_name, where=f"email = '{email}'"):
            print("Email already exists. Please use a different email.")
            return False

        # Hash the password and insert the new user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.insert(table_name, {'email': email, 'password': hashed_password})
        print("Signup successful!")
        return True

    def close(self):
        self.conn.close()

# Example usage:
# db = SQLModel(db_name='users.db')
# db.create_table('users', {'id': 'INTEGER PRIMARY KEY', 'email': 'TEXT UNIQUE', 'password': 'TEXT'})
# db.signup('users', 'john_doe@example.com', 'password123')
# db.login('users')
# db.close()

# db = SQLModel(db_name='books.db')
# db.create_table('books', {'id': 'INTEGER PRIMARY KEY', 'title': 'TEXT', 'outline': 'TEXT', 'content': 'TEXT'})
# db.insert('users', {'name': 'John Doe', 'age': 10})
# users = db.select('users', where='age > 20')
# users = db.select("users", columns=["name", "age"], where="age < 20")
# print(users)
