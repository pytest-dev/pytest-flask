import functools
import warnings


def deprecated(reason):
    """Decorator which can be used to mark function or method as deprecated.
    It will result a warning being emmitted when the function is called."""

    def decorator(func):
        @functools.wraps(func)
        def deprecated_call(*args, **kwargs):
            warnings.simplefilter("always", DeprecationWarning)
            warnings.warn(reason, DeprecationWarning, stacklevel=2)
            warnings.simplefilter("default", DeprecationWarning)
            return func(*args, **kwargs)

        return deprecated_call

    return decorator
