import pyqueue
import time

from pyqueue import task


class TestTask(pyqueue.Task):
    def __init__(self, n):
        self.n = n

    def execute(self):
        print(f'task {self.n} started')
        time.sleep(5)
        print(f'task {self.n} done')


q = pyqueue.Queue()

q.start_daemon()

tasks = []
for i in range(10):
    q.push_task(TestTask(i))

time.sleep(20)
