from multiprocessing import Lock


class Sender:
    def __init__(self, sio):
        self.sio = sio
        self.lock = Lock()

    def emit(self, to, data, callback=None):
        self.lock.acquire()

        try:
            self.sio.emit(
                to,
                data,
                namespace='',
                callback=callback
            )
        except Exception as e:
            # TODO: Lock? Retry?
            pass

        self.lock.release()
