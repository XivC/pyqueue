import sqlite3
import pickle
import datetime
import os
import threading
import time

from . import settings


class Storage:
    def __init__(self, queue, name):
        self.name = name
        self._connection = sqlite3.connect("pyqueue_default", check_same_thread=False)
        self._create_table()
        self._queue = queue
        threading.Thread(target=self._commit).start()

    def _commit(self):
        try:
            self._connection.commit()
        except sqlite3.OperationalError:
            return

    def _execute(self, operation, bind=()):
        cursor = self._connection.cursor()
        dir_path = os.path.dirname(__file__)
        path = os.path.join(dir_path, 'sql', operation + '.sql')
        with open(path) as file:
            statement = file.read()
            statement = statement.replace('$name$', self.name)
            cursor.execute(statement, bind)
        return cursor

    def _create_table(self):
        self._execute('create', ())
        self._commit()
        self._execute('delete_corrupted')
        self._commit()

    def add_task(self, task):
        task = pickle.dumps(task)
        now = datetime.datetime.utcnow()
        cursor = self._execute('new_task', (now, settings.TASK_QUEUED, task,))
        self._commit()
        task_id = cursor.fetchone()[0]

        return task_id

    def update_state(self, task_id, state):
        now = datetime.datetime.utcnow()
        self._execute('update_state', (now, state, task_id,))
        self._commit()

    def next_task(self):
        cursor = self._execute('next_task', ())
        mb_task = cursor.fetchone()
        if not mb_task:
            return None, None
        task_id = mb_task[0]
        task = pickle.loads(mb_task[1])
        return task_id, task
