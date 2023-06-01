import time
from concurrent.futures import ThreadPoolExecutor
import redis


class RedisLock:

    lock_key = 'lock'

    def __init__(self):
        self.r = redis.Redis()
        self.lock = self.r.lock(self.lock_key)

    def __enter__(self):
        print('enter start')
        self.lock.acquire(blocking=True)
        print('enter stop')

    def __exit__(self, exc_type, exc_value, exc_tb):
        print('exit')
        self.lock.release()


mu = RedisLock()
result = 0


def function():
    with mu:
        print('to mutex')
        global result
        r = result
        time.sleep(1)
        result = r + 1
        print('from mutex')


def main():

    with ThreadPoolExecutor(max_workers=2) as executor:
        for _ in range(10):
            executor.submit(function)
    print(result)  # хотим получить в итоге 10


main()
