import sqlite3
import os

class TaskModel:
    def __init__(self, db_name="database.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', db_name)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            conn.commit()

    def get_all_tasks(self):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM tasks')
            return cursor.fetchall()

    def add_task(self, title):
        with self.get_connection() as conn:
            cursor = conn.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (title, 0))
            conn.commit()
            task_id = cursor.lastrowid
            return {'id': task_id, 'title': title, 'done': 0}

    def toggle_task(self, task_id):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT done FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            if task:
                new_status = 0 if task['done'] else 1
                conn.execute('UPDATE tasks SET done = ? WHERE id = ?', (new_status, task_id))
                conn.commit()

    def delete_task(self, task_id):
        with self.get_connection() as conn:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
