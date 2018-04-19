from bisect import bisect
from array import array as _array


def _arange(a, b):
    ar = _array('l', [0] * (b - a))
    for i, e in enumerate(range(a, b)):
        ar[i] = e
    return ar


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


class Sieve:
    """An infinite list of prime numbers, implemented as a dynamically
    growing sieve of Eratosthenes. When a lookup is requested involving
    an odd number that has not been sieved, the sieve is automatically
    extended up to that number.
    Examples
    ========
    >>> from sympy import sieve
    >>> sieve._reset() # this line for doctest only
    >>> 25 in sieve
    False
    >>> sieve._list
    array('l', [2, 3, 5, 7, 11, 13, 17, 19, 23])
    """

    # data shared (and updated) by all Sieve instances
    _list = _array('l', [2, 3, 5, 7, 11, 13])

    def __repr__(self):
        return "<Sieve with %i primes sieved: 2, 3, 5, ... %i, %i>" % \
            (len(self._list), self._list[-2], self._list[-1])

    def _reset(self):
        """Return sieve to its initial state for testing purposes.
        """
        self._list = self._list[:6]

    def extend(self, n):
        """Grow the sieve to cover all primes <= n (a real number).
        Examples
        ========
        >>> from sympy import sieve
        >>> sieve._reset() # this line for doctest only
        >>> sieve.extend(30)
        >>> sieve[10] == 29
        True
        """
        n = int(n)
        if n <= self._list[-1]:
            return

        # We need to sieve against all bases up to sqrt(n).
        # This is a recursive call that will do nothing if there are enough
        # known bases already.
        maxbase = int(n**0.5) + 1
        self.extend(maxbase)

        # Create a new sieve starting from sqrt(n)
        begin = self._list[-1] + 1
        newsieve = _arange(begin, n + 1)

        # Now eliminate all multiples of primes in [2, sqrt(n)]
        for p in self.primerange(2, maxbase):
            # Start counting at a multiple of p, offsetting
            # the index to account for the new sieve's base index
            startindex = (-begin) % p
            for i in range(startindex, len(newsieve), p):
                newsieve[i] = 0

        # Merge the sieves
        self._list += _array('l', [x for x in newsieve if x])

    def extend_to_no(self, i):
        """Extend to include the ith prime number.
        i must be an integer.
        The list is extended by 50% if it is too short, so it is
        likely that it will be longer than requested.
        Examples
        ========
        >>> from sympy import sieve
        >>> sieve._reset() # this line for doctest only
        >>> sieve.extend_to_no(9)
        >>> sieve._list
        array('l', [2, 3, 5, 7, 11, 13, 17, 19, 23])
        """
        i = as_int(i)
        while len(self._list) < i:
            self.extend(int(self._list[-1] * 1.5))

    def primerange(self, a, b):
        """Generate all prime numbers in the range [a, b).
        Examples
        ========
        >>> from sympy import sieve
        >>> print([i for i in sieve.primerange(7, 18)])
        [7, 11, 13, 17]
        """
        from sympy.functions.elementary.integers import ceiling

        # wrapping ceiling in int will raise an error if there was a problem
        # determining whether the expression was exactly an integer or not
        a = max(2, int(ceiling(a)))
        b = int(ceiling(b))
        if a >= b:
            return
        self.extend(b)
        i = self.search(a)[1]
        maxi = len(self._list) + 1
        while i < maxi:
            p = self._list[i - 1]
            if p < b:
                yield p
                i += 1
            else:
                return

    def search(self, n):
        """Return the indices i, j of the primes that bound n.
        If n is prime then i == j.
        Although n can be an expression, if ceiling cannot convert
        it to an integer then an n error will be raised.
        Examples
        ========
        >>> from sympy import sieve
        >>> sieve.search(25)
        (9, 10)
        >>> sieve.search(23)
        (9, 9)
        """
        from sympy.functions.elementary.integers import ceiling

        # wrapping ceiling in int will raise an error if there was a problem
        # determining whether the expression was exactly an integer or not
        test = int(ceiling(n))
        n = int(n)
        if n < 2:
            raise ValueError("n should be >= 2 but got: %s" % n)
        if n > self._list[-1]:
            self.extend(n)
        b = bisect(self._list, n)
        if self._list[b - 1] == test:
            return b, b
        else:
            return b, b + 1

    def __contains__(self, n):
        try:
            n = as_int(n)
            assert n >= 2
        except (ValueError, AssertionError):
            return False
        if n % 2 == 0:
            return n == 2
        a, b = self.search(n)
        return a == b

    def __getitem__(self, n):
        """Return the nth prime number"""
        if isinstance(n, slice):
            self.extend_to_no(n.stop)
            return self._list[n.start - 1:n.stop - 1:n.step]
        else:
            n = as_int(n)
            self.extend_to_no(n)
            return self._list[n - 1]


# Generate a global object for repeated use in trial division etc
sieve = Sieve()
