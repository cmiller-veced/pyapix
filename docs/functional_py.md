# Functional programming in Python

Functional programming makes some fundamentally different choices from how
things are done in object oriented (OO) programming.  Niether paradigm is
inherently superior, each has strengths and weaknesses.  Each tends to work
better for certain types of problems.  (Give examples.)

One way to think of the difference is that OO can be thought of as bringing the
data to the code, while the functional approach can be thought of as bring the
code to the data.

Another way of thinking of it is to think of expressing business logic in data.
(link to Swizek).


## List Processing

Functional programming began with the Lisp programming language in the 1950's.
'Lisp' stands for 'list processing' and the concept remains relevant today.
Lots of programming problems can be conveniently expressed as operations on
lists of objects.
The obvious way is with `for` loops.

    for thing in list_of_things:
        do_something_with(thing)

The less obvious way is with a list comprehension.

    [do_something_with(thing) for thing in list_of_things]

The second way is more compact and more aligned with the functional paradigm.

### List Comprehensions

To make it more real we contrive an illustrative example.  Let's say we have
a list of lowercase strings and want to capitalize every word.
Assume for the moment that we are unaware of the easy way to do this.

    >>> s = 'here is a message'
    >>> s.title()
    'Here Is A Message'

First we split the string into a list of words.

    >>> word_list = s.split()
    >>> word_list
    ['here', 'is', 'a', 'message']

Now capitalize with a `for` loop.

    >>> s2 = ''
    >>> for word in word_list:
    ...     s2 += word.title() + ' '
    ...     
    >>> s2
    'Here Is A Message'

Now the same using a list comprehension.

    >>> ' '.join([word.title() for word in word_list])
    'Here Is A Message'

The list comprehension is shorter and arguably more 'pythonic'.  But the real
power comes when we pass in a function.  

    >>> word_list = 'this is an important incomimng message'.split()
    >>> good_one = lambda s: s.startswith('i')
    >>> [good_one(s) for s in word_list]
    [False, True, False, True, True, False]
    >>> [s for s in word_list if good_one(s)]
    ['is', 'important', 'incomimng']

    >>> good_one = lambda s: len(s) > 4
    >>> [s for s in word_list if good_one(s)]
    ['important', 'incomimng', 'message']
    >>> [s for s in word_list if not good_one(s)]
    ['this', 'is', 'an']


List comprehensions allow us to leave the data in its original state.  We bring
code to the data.



#### Lambda functions

A lambda function is a shorthand for defining a function consiting of solely
a return statement.  Both of the following statements define the same function.

    >>> def squared(x):
    ...     return x**2
    ...     

    >>> squared = lambda x: x**2

The function can then be called like any other.

    >>> squared(10)
    100
    >>> [squared(x) for x in range(5)]
    [0, 1, 4, 9, 16]


## Decorators
A decorator is a function that takes a function as its sole argument and
returns a function.

It can be the same function.

    def flagged(fun):
        fun.flag = True
        return fun


    @flagged
    def f1():
        return

    def f2():
        return

    """
    >>> f1
    <function f1 at 0x10415b1f0>
    >>> f2
    <function f2 at 0x10415b310>
    >>> f1.flag
    True
    >>> f2.flag
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'function' object has no attribute 'flag'
    """



## Parameterized Decorators

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
        return msg*2

    @log_to(log_file2)
    def other_fun(msg):
        return msg*4

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

Will print something like this...

    =================================
    contents of log1.txt
    some_fun 1732646222, args: ('x',),  kw: {},  value=x
    some_fun 1732646222, args: ('y',),  kw: {},  value=y


    =================================
    contents of log2.txt
    other_fun 1732646222, args: ('x',),  kw: {},  value=xxxxxxxxxxxxxxxxxxxxxx
    other_fun 1732646222, args: ('y',),  kw: {},  value=yyyyyyyyyyyyyyyyyyyyyy



## Dynamic functions

Dynamic functions are like parameterized decorators but without some of the
constraints.

    def pow(n):
        """Return a function that raises input `x` to the `n` power.
        """
        def _pow(x):
            return x**n
        return _pow

    squared = pow(2)
    cubed = pow(3)

    for x in [0, 1]:
        assert squared(x) == x
        assert cubed(x) == x

    for x in [2, 3, 100]:
        assert squared(x) == x**2
        assert cubed(x) == x**3


## Generic Functions

A generic function accepts arguments of differing types.  The `singledispatch`
decorator is a convenient way to implement generic functions in Python.

    from functools import singledispatch
    import pytest

    @singledispatch
    def floor(x):
        raise NotImplementedError(f'bad type: {type(x)}')

    @floor.register(float)
    def _(x):
        return int(x)

    @floor.register(int)
    def _(x):
        return x

    def test_floor():
        bad_things = [{}, [], (), '', 'a']
        for thing in bad_things:
            with pytest.raises(NotImplementedError):
                floor(thing)
        assert floor(1) == 1
        assert floor(1.1) == 1

    test_floor()


------------------------------------------

## Rules of Thumb

### Do not alter data

Unless there is a compelling business justification.

### Do not get creative

Use business concepts.

#### Make the code boring and obvious

Clear and concise.  Fewest possible indentations.

#### Use the language of the business problem

Not programmer jargon.

### Do not solve irrelevant problems

- eg translation from json -> DAO


### xxxxxxxxxx

Python has almost all functional programming features of Lisp, except macros.

To get a handle on functional programming in Python, decorators are a good
starting point.  The coder who has a solid understanding of decorators is well
on the way to having a good grounding in functional programming in Python.
There are several things to consider.


### Advice

Put the logic into data.  

Bring the code to the data.




