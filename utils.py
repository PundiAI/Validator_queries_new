# from web3 import Web3
import logging
import traceback
from functools import wraps
import random

def convert_to_lower_case(string:str)->str:
    return string.lower()

def convert_pair_id_to_chain_id(pair_id:str)->str:
    chain_id = convert_to_lower_case(pair_id.split(":")[0])
    return chain_id


# def fromWei(value):
#     return Web3.fromWei(value, 'ether')

def from3dp(value):
    return value * 10**(-3)

def to3dp(value):
    return value * 10**(3)

def convert_to_int(number:str):
    try:
        int_num=int(number)
        return int_num
    except ValueError as ve:
        print('"%s" cannot be converted to an int: %s' % (number, ve))


def convert_to_human_readable(number):
    if isinstance(number,str):
        int_num=convert_to_int(number)
        number=float(int(int_num)*10**-18)
    else:
        number=float(int(number)*10**-18)
    return number

def convert_to_bc_readable(number):
    if isinstance(number,str):
        int_num=convert_to_int(number)
        number=float(int(int_num)*10**18)
    else:
        number=float(int(number)*10**18)
    return number

def reformat_date(timestamp:str):
    index=timestamp.find('T')
    date=timestamp[0:index]
    return date


def reformat_time(timestamp:str):
    index=timestamp.find('T')
    time=timestamp[(index+1):-1]
    return time


def randomizer(base,multiplier):
    random_out=base+multiplier*random.random()
    return (random_out)

def rand_amt(number):
    numb=number*random.random()
    return numb

def add_rand_amts(neg,pos):
    amt=int(rand_amt(neg)+rand_amt(pos))
    return amt


def pick_a_random_element(arr):
    return random.choice(arr)

def rand_int_within_bounds(min,max):
    number = random.randint(min,max)
    return number

def initialise_logging(filename):
    logging.basicConfig(filename=filename,level=logging.INFO,format='%(asctime)s,%(levelname)s,%(message)s',datefmt='%m/%d/%Y %I:%M:%S')

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