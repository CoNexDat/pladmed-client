from os import path, remove, makedirs, listdir
from utils.atomic_writer import AtomicWriter

class Storage:
    def __init__(self, store_in, state_file, tmp_folder):
        makedirs(store_in, exist_ok=True)
        makedirs(tmp_folder, exist_ok=True)

        self.store_in = store_in
        self.tmp_folder = tmp_folder
        self.state_file = state_file
        self.writer = AtomicWriter()

    def clean_tmp_folder(self):
        for file_ in listdir(self.tmp_folder):
            remove(self.tmp_folder + file_)
    
    def remove_tmp_file(self, task):
        try:
            remove(self.tmp_folder + task.code)
        except:
            # File doesn't exist
            pass

    def operation_filename(self, task):
        file_storage = self.store_in + task.code

        return file_storage 

    def operation_filename_tmp(self, task):
        tmp_path = self.tmp_folder + task.code

        return tmp_path

    def mark_task_finished(self, task):
        try:
            self.writer.move(
                self.operation_filename_tmp(task),
                self.operation_filename(task)
            )
        except:
            # In this case, the dst file already exists, which means
            # the client crashed (Or the server (?)) while the operation
            # was being marked as FINISHED, it's okay to pass because it contains
            # the results of a previus operation and new results are not needed
            pass

    def remove_task(self, task):
        try:
            remove(self.store_in + task.code)
        except:
            pass

    def save_operations_state(self, state):
        self.writer.write(self.state_file, state)

    def read_operations_state(self):
        return self.writer.read(self.state_file)
