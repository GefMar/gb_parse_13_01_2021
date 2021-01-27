import datetime


def log_deco(funk):
    def wrap(*args, **kwargs):
        print(f"{datetime.datetime.now()}: {funk.__name__}: args: {args}, kwargs: {kwargs}")
        result = funk(*args, **kwargs)
        return result

    return wrap

@log_deco
def my_summ(a, b):
    return a + b

@log_deco
def my_mul(a, b):
    return a * b

# my_summ = log_deco(my_summ)

my_summ(1, 3)

