import sqlite3


class ProblemsDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS problems
                            (id INTEGER PRIMARY KEY,
                            name TEXT,
                            body TEXT,
                            tests_path TEXT,
                            answers_path TEXT)"""
        )
        self.conn.commit()

    def add_problem(self, name, body, tests_path, answers_path):
        self.c.execute(
            "INSERT INTO problems VALUES (NULL, ?, ?, ?, ?)",
            (name, body, tests_path, answers_path),
        )
        self.conn.commit()

    def get_all_problems(self):
        self.c.execute("SELECT * FROM problems")
        return self.c.fetchall()

    def get_problem(self, id):
        self.c.execute("SELECT * FROM problems WHERE id = ?", (id,))
        return self.c.fetchone()

    def delete_problem(self, id):
        self.c.execute("DELETE FROM problems WHERE id = ?", (id,))
        self.conn.commit()

    def update_problem(self, id, name, body, tests_path, answers_path):
        self.c.execute(
            "UPDATE problems SET name = ?, body = ?, tests_path = ?, answers_path = ? WHERE id = ?",
            (name, body, tests_path, answers_path, id),
        )
        self.conn.commit()

    def close_connection(self):
        self.conn.close()


class UsersDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY,
                             username TEXT,
                             password TEXT,
                             email TEXT,
                             solved TEXT,
                             is_admin INTEGER)"""
        )
        self.conn.commit()

    def add_user(self, username, password, email, solved, is_admin):
        self.c.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)",
            (username, password, email, solved, is_admin),
        )
        self.conn.commit()

    def get_all_users(self):
        self.c.execute("SELECT * FROM users")
        return self.c.fetchall()

    def get_user(self, id):
        self.c.execute("SELECT * FROM users WHERE id = ?", (id,))
        return self.c.fetchone()

    def get_user_by_username(self, username):
        self.c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.c.fetchone()

    def get_user_by_email(self, email):
        self.c.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.c.fetchone()

    def delete_user(self, id):
        self.c.execute("DELETE FROM users WHERE id = ?", (id,))
        self.conn.commit()

    def update_user(self, id, username, password, email, solved, is_admin):
        self.c.execute(
            "UPDATE users SET username = ?, password = ?, email = ?, solved = ?, is_admin = ? WHERE id = ?",
            (username, password, email, solved, is_admin, id),
        )
        self.conn.commit()

    def solve(self, id, prbid):
        user = self.get_user(id)
        solved = user[4]
        solved_set = set(solved)
        solved_set.add(str(prbid))
        self.update_user(id, user[1], user[2], user[3], "".join(solved_set), user[5])

    def close_connection(self):
        self.conn.close()
