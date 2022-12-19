from functools import wraps
import logging

# =====================================================decorators======================================================================

def exception_logger(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @wraps(function) # this is to allow stacking of decorators
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.error("{} | {} | {} \n {}".format(function.__qualname__, e,type(e),traceback.format_exc()))
            raise
    return wrapper



def successful_query(request):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @wraps(function) # this is to allow stacking of decorators
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.error("{} | {} | {} \n {}".format(function.__qualname__, e,type(e),traceback.format_exc()))
            raise
    return wrapper