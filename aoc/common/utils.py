import time

def is_digit(c: str) -> bool:
    return ord('0') <= ord(c) <= ord('9')

def profile(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()

        print(f"Func {func.__name__} took {(end_time - start_time) * 1000}ms")

        return res
    return wrapper