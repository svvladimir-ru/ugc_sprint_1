import time
import re
from functools import wraps
from uuid import UUID

from config import set_logger

logger = set_logger()


def benchmark(operation: str, sleep: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            func_result = func(*args, **kwargs)
            end_time = time.perf_counter()
            avg_time = end_time - start_time
            logger.info(f"Время операции {operation}: {avg_time}")
            if sleep:
                time.sleep(2)
            return func_result
        return wrapper
    return decorator


def parse_error(error: str) -> list:
    returned = []
    str_data = re.findall(
        r'(movie_id: UUID\(".*"\)|content_id: UUID\(".*"\))', error
    )[0]
    for values in str_data.split(','):
        key, value = values.split(':')
        returned.append(
            {key.strip(): UUID(re.findall(r'"(.*?)"', value.strip())[0])}
        )

    return returned
