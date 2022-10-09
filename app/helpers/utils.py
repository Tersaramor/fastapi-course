import time
from typing import Any, Callable, List, Type, Union

from loguru import logger


class TimeoutException(Exception):
    """Timeout waiter exception"""
    pass


class CustomDummyException(Exception):
    """A dummy not to catch any exception"""
    pass


def wait(
        method: Callable[[], Any],
        timeout: float = 5,
        interval: float = 0.1,
        err_msg: str = None,
        ignored_exceptions: Union[Type[BaseException], List[Type[BaseException]]] = None
):
    if ignored_exceptions is None:
        ignored_exceptions = CustomDummyException

    started = time.time()
    last_exception = None
    while (current_time := time.time() - started) < timeout:
        try:
            if outcome := method():
                logger.warning(f"Success of Method {method.__name__} after: {round(current_time, 3)}s from {timeout}")
                return outcome
            last_exception = f'Method {method.__name__} returned {outcome}'
            time.sleep(interval)
        except ignored_exceptions as e:
            last_exception = e

    raise TimeoutException(f'Method {method.__name__} timeout out in {timeout}sec with exception: '
                           f'{last_exception}\nerr_msg: {err_msg}')
