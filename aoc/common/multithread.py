from multiprocessing import Pool
from typing import Callable, List, Any, Optional, Tuple


# Simple wrapper to unwrap the arguments coming as input
class MultiWrapper:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, input: Any):
        return self.func(*input)


def execute_async(num_threads: int, func: Callable, input_list: List[Tuple[Any]], reduce_func: Optional[Callable] = None):
    result = None
    with Pool(num_threads) as p:
        result = p.map(func, input_list)
        if reduce_func is not None:
            result = reduce_func(result)

    return result


if __name__ == "__main__":
    def reduce(x: List[int]) -> int:
        return sum(x)
    
    def reduce_multi(a: int, b: int, c: int) -> int:
        return a + b + c
    
    data = [[2,3,4], [5,6,7], [7,8,9], [11, 11, 11]]
    single_thread_result = [reduce(d) for d in data]
    single_thread_result_reduced = reduce(single_thread_result)

    multi_thread_result = execute_async(4, reduce, data)
    multi_thread_result_reduce = execute_async(4, reduce, data, reduce)

    multi_thread_multi_result = execute_async(4, MultiWrapper(reduce_multi), data)
    multi_thread_multi_result_reduced = execute_async(4, MultiWrapper(reduce_multi), data, reduce)

    assert(single_thread_result == multi_thread_result)
    assert(single_thread_result_reduced == multi_thread_result_reduce)
    assert(single_thread_result == multi_thread_multi_result)
    assert(single_thread_result_reduced == multi_thread_multi_result_reduced)
