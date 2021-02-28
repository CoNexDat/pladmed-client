from atomicwrites import atomic_write, move_atomic
import pickle
import os

class AtomicWriter:
    def write(self, where, content):
        with atomic_write(path=where, overwrite=True, mode='wb') as f:
            f.write(pickle.dumps(content))

    def read(self, from_where):
        try:
            with open(from_where, 'rb') as f:
                content = f.read()

                return pickle.loads(content)
        except:
            return {}

    def move(self, from_where, to_where):
        move_atomic(from_where, to_where)
