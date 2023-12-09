import time
from typing import Callable



def time_check(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[TIME_CHECK] {func.__name__}_duration_time_sec = {end_time - start_time}")
        return result
    return wrapper
