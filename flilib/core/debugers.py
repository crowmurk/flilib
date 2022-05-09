import functools
import time

from django.db import connection, reset_queries

from .logger import log_debug as log

def query_debugger(*, show_sql=False, cut_lines=False):
    """ Декоратор для оценки SQL запросов
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.debug(f"Function : {func.__name__}")

            reset_queries()

            start_queries = len(connection.queries)

            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()

            end_queries = len(connection.queries)

            if show_sql:
                for query in connection.queries:
                    query_sql, query_time = query['sql'], query['time']
                    log.debug(
                        f"sql: {query_sql[:100] if cut_lines else query_sql} time: {query_time}"
                    )

            log.debug(f"Number of queries : {end_queries - start_queries}")
            log.debug(f"Finished in : {(end - start):.2f}s")
            return result
        return wrapper
    return decorator

def performance_debugger(func):
    """ Декоратор для оценки времени выполнения
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(f"Function : {func.__name__}")

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        log.debug(f"Finished in : {(end - start):.2f}s")

        return result

    return wrapper
