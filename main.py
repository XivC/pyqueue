import pyqueue
import time
import random
from pyqueue import task


class TestTask(pyqueue.Task):
    def __init__(self, n):
        self.n = n

    def execute(self):
        print(f'task {self.n} started')
        time.sleep(random.randint(1, 10))
        print(f'task {self.n} done')


q = pyqueue.Queue(name='test')

q.start_daemon()

tasks = []
for i in range(10):
    q.push_task(TestTask(i))

time.sleep(20)
q.stop_daemon()