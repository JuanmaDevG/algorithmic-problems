import functools
import signal
import sys
from collections.abc import Callable
from pathlib import Path


# TODO: fix timeout decorator to fit my needs
def timeout(seconds: int):
    def decorator(func: Callable[[tuple[object, ...]], None]):
        @functools.wraps(func)
        def wrapper(*args: tuple[object], **kwargs: dict[object, object]):
            def handler(_signum: object, _frame: object):
                raise TimeoutError(f"{func.__name__} timed out after {seconds}s")

            old = signal.signal(signal.SIGALRM, handler)
            _ = signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                return func(*args, **kwargs)
            finally:
                _ = signal.setitimer(signal.ITIMER_REAL, 0)
                _ = signal.signal(signal.SIGALRM, old)

        return wrapper

    return decorator


sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
