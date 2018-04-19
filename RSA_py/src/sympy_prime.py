import random


def as_int(n):
    """
    Convert the argument to a builtin integer.
    The return value is guaranteed to be equal to the input. ValueError is
    raised if the input has a non-integral value.
    Examples
    ========
    >>> from sympy.core.compatibility import as_int
    >>> from sympy import sqrt
    >>> 3.0
    3.0
    >>> as_int(3.0) # convert to int and test for equality
    3
    >>> int(sqrt(10))
    3
    >>> as_int(sqrt(10))
    Traceback (most recent call last):
    ...
    ValueError: ... is not an integer
    """
    try:
        result = int(n)
        if result != n:
            raise TypeError
    except TypeError:
        raise ValueError('%s is not an integer' % (n,))
    return result


def randprime(a, b):
    """ Return a random prime number in the range [a, b).
        Bertrand's postulate assures that
        randprime(a, 2*a) will always succeed for a > 1.
        References
        ==========
        - http://en.wikipedia.org/wiki/Bertrand's_postulate
        Examples
        ========
        >>> from sympy import randprime, isprime
        >>> randprime(1, 30) #doctest: +SKIP
        13
        >>> isprime(randprime(1, 30))
        True
        See Also
        ========
        primerange : Generate all primes in a given range
    """
    if a >= b:
        return
    a, b = map(int, (a, b))
    n = random.randint(a - 1, b)
    p = nextprime(n)
    if p >= b:
        p = prevprime(b)
    if p < a:
        raise ValueError("no primes exist in the specified range")
    return p


def nextprime(n, ith=1):
    """ Return the ith prime greater than n.
        i must be an integer.
        Notes
        =====
        Potential primes are located at 6*j +/- 1. This
        property is used during searching.
        >>> from sympy import nextprime
        >>> [(i, nextprime(i)) for i in range(10, 15)]
        [(10, 11), (11, 13), (12, 13), (13, 17), (14, 17)]
        >>> nextprime(2, ith=2) # the 2nd prime after 2
        5
        See Also
        ========
        prevprime : Return the largest prime smaller than n
        primerange : Generate all primes in a given range
    """
    n = int(n)
    i = as_int(ith)
    if i > 1:
        pr = n
        j = 1
        while 1:
            pr = nextprime(pr)
            j += 1
            if j > i:
                break
        return pr

    if n < 2:
        return 2
    if n < 7:
        return {2: 3, 3: 5, 4: 5, 5: 7, 6: 7}[n]
    if n <= sieve._list[-2]:
        l, u = sieve.search(n)
        if l == u:
            return sieve[u + 1]
        else:
            return sieve[u]
    nn = 6 * (n // 6)
    if nn == n:
        n += 1
        if isprime(n):
            return n
        n += 4
    elif n - nn == 5:
        n += 2
        if isprime(n):
            return n
        n += 4
    else:
        n = nn + 5
    while 1:
        if isprime(n):
            return n
        n += 2
        if isprime(n):
            return n
        n += 4


def prevprime(n):
    """ Return the largest prime smaller than n.
        Notes
        =====
        Potential primes are located at 6*j +/- 1. This
        property is used during searching.
        >>> from sympy import prevprime
        >>> [(i, prevprime(i)) for i in range(10, 15)]
        [(10, 7), (11, 7), (12, 11), (13, 11), (14, 13)]
        See Also
        ========
        nextprime : Return the ith prime greater than n
        primerange : Generates all primes in a given range
    """
    from sympy.functions.elementary.integers import ceiling

    # wrapping ceiling in int will raise an error if there was a problem
    # determining whether the expression was exactly an integer or not
    n = int(ceiling(n))
    if n < 3:
        raise ValueError("no preceding primes")
    if n < 8:
        return {3: 2, 4: 3, 5: 3, 6: 5, 7: 5}[n]
    if n <= sieve._list[-1]:
        l, u = sieve.search(n)
        if l == u:
            return sieve[l - 1]
        else:
            return sieve[l]
    nn = 6 * (n // 6)
    if n - nn <= 1:
        n = nn - 1
        if isprime(n):
            return n
        n -= 4
    else:
        n = nn + 1
    while 1:
        if isprime(n):
            return n
        n -= 2
        if isprime(n):
            return n
        n -= 4
