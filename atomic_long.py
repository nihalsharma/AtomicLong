from datetime import datetime, date
from functools import wraps
import threading



def synchronized(function):

    def synched_function(self, *args, **kwargs):
        function._lock__ = threading.Lock()
        with function._lock__:
            return function(self, *args, **kwargs)
    return synched_function


class AtomicLong:
    def __init__(self, num):
        self._num = num

    @synchronized
    def increment_and_get(self):
        self._num += 1
        return self._num

    @synchronized
    def add_and_get(self, val):
        self._num += val
        return self._num

    @synchronized
    def set_value(self, val):
        self._num = val


class IdGenerator:
    RESET_MARKER = 101
    MAX_SEQUENCE_VALUE = 9999
    ATOMIC_LONG = AtomicLong(RESET_MARKER)

    @staticmethod
    def generate_id():
        # some random business logic to create an order id
        sequence_number = IdGenerator.ATOMIC_LONG.increment_and_get()
        first_day = date(date.today().year, 1, 1)
        today = date.today()
        diff_days = (today - first_day).days
        year = date.today().year % 100
        seconds_passed_since_midnight = int(
            (datetime.now() - datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())

        id = "{0}{1}{2}{3}{4}-{5}".format("A", "O", diff_days, year,
                                                   seconds_passed_since_midnight,
                                                   sequence_number)
        print(id)
        if sequence_number > IdGenerator.MAX_SEQUENCE_VALUE:
            IdGenerator.ATOMIC_LONG.set_value(IdGenerator.RESET_MARKER)
        return id



if __name__ == '__main__':
    id_gen = IdGenerator()
    thread1 = threading.Thread(target=id_gen.generate_id)
    thread2 = threading.Thread(target=id_gen.generate_id)
    thread3 = threading.Thread(target=id_gen.generate_id)
    thread1.start()
    thread2.start()
    thread3.start()
