from types import FunctionType


# TODO: set it to True in submission

MASK_ERRORS = False


def failsafe(default=None):
    assert not isinstance(default, FunctionType) 
    # to prevent accidental
    # @failsafe
    # def f():
    #     ...
     
    def decorator(f):
        if MASK_ERRORS:
            def safe_f(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except:
                    return default
            return safe_f
        else:
            return f
    return decorator



if __name__ == '__main__':
    
    @failsafe(default=42)
    def f():
        return 0/0
    
    print f()