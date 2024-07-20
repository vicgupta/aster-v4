import sqlite3


class SQLModel:
    def __init__(self, db_name: str = None):

        if db_name == None or db_name == "":
            raise ValueError("Please provide a database name")

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        Creates a new table in the database.

        Args:
            table_name (str): The name of the table to create.
            columns (dict): A dictionary of column names and data types.
                            Example: {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'age': 'INTEGER'}
        """
        column_defs = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})")
        self.conn.commit()

    def insert(self, table_name, data):
        """
        Inserts a new row into a table.

        Args:
            table_name (str): The name of the table.
            data (dict): A dictionary of column names and values to insert.
                        Example: {'name': 'John Doe', 'age': 30}

        Returns:
            int: The ID of the newly inserted row.
        """
        placeholders = ", ".join(["?"] * len(data))
        columns = ", ".join(data.keys())
        values = tuple(data.values())
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def select(self, table_name, columns=None, where=None):
        """
        Selects rows from a table.

        Args:
            table_name (str): The name of the table.
            columns (list, optional): A list of column names to select.
                                      If None, all columns are selected.
            where (str, optional): A WHERE clause for filtering rows.

        Returns:
            list: A list of dictionaries, where each dictionary represents a row.
        """
        query = f"SELECT {' , '.join(columns) if columns else '*'} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [
            dict(zip([column[0] for column in self.cursor.description], row))
            for row in rows
        ]

    def update(self, table_name, data, where):
        """
        Updates rows in a table.

        Args:
            table_name (str): The name of the table.
            data (dict): A dictionary of column names and new values.
            where (str): A WHERE clause for specifying which rows to update.
        """
        set_clause = ", ".join(f"{name} = ?" for name in data)
        values = tuple(data.values())
        self.cursor.execute(
            f"UPDATE {table_name} SET {set_clause} WHERE {where}", values
        )
        self.conn.commit()

    def delete(self, table_name, where):
        """
        Deletes rows from a table.

        Args:
            table_name (str): The name of the table.
            where (str): A WHERE clause for specifying which rows to delete.
        """
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {where}")
        self.conn.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()


# db = SQLModel(db_name='books.db')
# db.create_table('books', {'id': 'INTEGER PRIMARY KEY', 'title': 'TEXT', 'outline': 'TEXT', 'content': 'TEXT'})
# db.insert('users', {'name': 'John Doe', 'age': 10})
# users = db.select('users', where='age > 20')
# users = db.select("users", columns=["name", "age"], where="age < 20")
# print(users)
