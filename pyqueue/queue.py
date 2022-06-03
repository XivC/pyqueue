import threading
import os
from .storage import Storage


class Queue:

    def __init__(self, max_threads=5, op_timeout=60, name=None):

        self._max_threads = max_threads
        self._op_timeout = op_timeout
        self._name = name or f'q_{id(self)}'
        self.storage = Storage(self._name)


