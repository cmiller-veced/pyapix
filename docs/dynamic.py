

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



