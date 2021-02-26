from os import path, remove, makedirs
from utils.atomic_writer import AtomicWriter

class Storage:
    def __init__(self, store_in, state_file, tmp_folder):
        makedirs(store_in, exist_ok=True)
        makedirs(tmp_folder, exist_ok=True)

        self.store_in = store_in
        self.tmp_folder = tmp_folder
        self.state_file = state_file
        self.writer = AtomicWriter()

    def define_operation_filename(self, task_code):
        filename = task_code

        i = 1

        while (path.exists(self.store_in + filename)):
            filename = task_code + "_part_" + str(i)

        return filename

    def operation_filename(self, task_code):
        file_storage = self.store_in + self.define_operation_filename(task_code)

        return file_storage 

    def operation_filename_tmp(self, task_code):
        tmp_path = self.tmp_folder + self.define_operation_filename(task_code)

        return tmp_path

    def operation_filename(self, task_code):
        return self.store_in + task_code

    def mark_task_finished(self, task):
        try:
            self.writer.move(
                self.operation_filename_tmp(task.code),
                self.operation_filename(task.code)
            )
        except:
            # In this case, the dst file already exists, which means
            # the client crashed (Or the server (?)) while the operation
            # was being marked as FINISHED, it's okay to pass because it contains
            # the results of a previus operation and new results are not needed
            pass

    def remove_task(self, task_code):
        try:
            remove(self.store_in + task_code)
        except:
            pass

    def save_operations_state(self, state):
        self.writer.write(self.state_file, state)

    def read_operations_state(self):
        return self.writer.read(self.state_file)
