import inspect
from functools import wraps


def autowire(*args, **kwargs):
    def decorator_autowire(init):
        @wraps(init)
        def wrapper_decorator(*init_args, **init_kwargs):
            instance = init(*init_args, **init_kwargs)
            return instance
        return wrapper_decorator
    return decorator_autowire


def testing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = func(*args, **kwargs)
        return instance
    return wrapper
