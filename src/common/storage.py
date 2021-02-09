from os import path

class Storage:
    def __init__(self, store_in):
        self.store_in = store_in
    
    def create_operation_filename(self, op_id):
        file_storage = self.store_in + op_id

        i = 1

        while (path.exists(file_storage)):
            file_storage = self.store_in + op_id + "_part_" + str(i)

        return file_storage
