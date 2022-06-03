import threading
from .storage import Storage
import time

from .task import Task
from . import settings


class Queue:
    def __init__(self, max_threads=5, name=None):
        self._max_threads = max_threads
        self._name = name or f'q_{id(self)}'
        self._storage = Storage(self._name)
        self._daemon = threading.Thread(target=self._runtime)
        self._tasks_threads = []
        self._is_working = False

    def _remove_done_tasks(self):
        alive_threads = []
        for task_id, thread in self._tasks_threads:
            if thread.is_alive():
                alive_threads.append((task_id, thread))
            else:
                self._storage.update_state(task_id, settings.TASK_DONE)
        self._tasks_threads = alive_threads


    def _next_task(self):
        task_id, task = self._storage.next_task()
        if not task:
            return
        task_thread = threading.Thread(target=task._execute)
        self._storage.update_state(task_id, settings.TASK_EXECUTING)
        self._tasks_threads.append((task_id, task_thread))
        task_thread.start()

    def _runtime(self):
        while self._is_working:
            time.sleep(0.1)
            self._remove_done_tasks()
            if len(self._tasks_threads) < self._max_threads:
                self._next_task()

    def start_daemon(self):
        self._is_working = True
        self._daemon.start()

    def stop_daemon(self):
        self._is_working = False
        print('Daemon stopped')

    def push_task(self, task: Task):
        self._storage.add_task(task)
