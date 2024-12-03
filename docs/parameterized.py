import sys
import time


def log_to(destination):
    def _log_to(func):
        def __log_to(*pos, **kw):
            value = func(*pos, **kw)
            with open(destination, 'a') as fh:
                fh.write(f'{func.__name__} {int(time.time())}, args: {pos},  kw: {kw},  value={value}\n')
            return value
        return __log_to
    return _log_to

log_file1 = 'log1.txt'
log_file2 = 'log2.txt'


@log_to(log_file1)
def some_fun(msg):
    return msg


@log_to(log_file2)
def other_fun(msg):
    return msg*22


some_fun('x')
some_fun('y')

other_fun('x')
other_fun('y')

# Let's see what got logged and where.

print('='*33)
print(f'contents of {log_file1}')
with open(log_file1) as fh:
    print(fh.read())

print()
print('='*33)
print(f'contents of {log_file2}')
with open(log_file2) as fh:
    print(fh.read())


