import sqlite3
import pickle
import datetime
import os

from . import settings


class Storage:
    def __init__(self, name):
        self.name = name
        self._connection = sqlite3.connect("pyqueue_default")
        self._cursor = self._connection.cursor()
        self._create_table()

    def _execute(self, operation, bind=()):
        dir_path = os.path.dirname(__file__)
        path = os.path.join(dir_path, 'sql', operation + '.sql')
        with open(path) as file:
            statement = file.read()
            statement = statement.replace('$name$', self.name)
            self._cursor.execute(statement, *bind)

    def _create_table(self):
        self._execute('create', ())
        self._connection.commit()

    def add_task(self, task):
        task = pickle.dumps(task)
        now = datetime.datetime.utcnow()
        self._execute('new_task', (now, settings.TASK_QUEUED, task))
        self._connection.commit()
        task_id = self._cursor.fetchone()[0]
        return task_id

    def update_state(self, task_id, state):
        now = datetime.datetime.utcnow()
        self._execute('update_state', (task_id, now, state))
        self._connection.commit()

    def next_task(self):
        self._execute('next_task', ())
        mb_task = self._cursor.fetchone()
        if not mb_task:
            return None
        task = pickle.loads(mb_task[0])
        return task

