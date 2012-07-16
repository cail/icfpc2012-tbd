import traceback

from types import FunctionType
import logging

# TODO: set it to True in submission

MASK_ERRORS = False


def failsafe(default=None):
    assert not isinstance(default, FunctionType) 
    # to prevent accidental
    # @failsafe
    # def f():
    #     ...
     
    def decorator(f):
        def decorated_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                logging.warning('Error masked in {}'.format(f))
                if not MASK_ERRORS:
                    raise
                return default
        return decorated_f
    return decorator



if __name__ == '__main__':
    
    @failsafe(default=42)
    def f():
        return 0/0
    
    print f()