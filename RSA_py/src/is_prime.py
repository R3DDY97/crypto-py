def isprime(n):
    """
    Test if n is a prime number (True) or not (False). For n < 2^64 the
    answer is definitive; larger n values have a small probability of actually
    being pseudoprimes.
    Negative numbers (e.g. -2) are not considered prime.
    The first step is looking for trivial factors, which if found enables
    a quick return.  Next, if the sieve is large enough, use bisection search
    on the sieve.  For small numbers, a set of deterministic Miller-Rabin
    tests are performed with bases that are known to have no counterexamples
    in their range.  Finally if the number is larger than 2^64, a strong
    BPSW test is performed.  While this is a probable prime test and we
    believe counterexamples exist, there are no known counterexamples.
    Examples
    ========
    >>> from sympy.ntheory import isprime
    >>> isprime(13)
    True
    >>> isprime(15)
    False
    See Also
    ========
    sympy.ntheory.generate.primerange : Generates all primes in a given range
    sympy.ntheory.generate.primepi : Return the number of primes less than or equal to n
    sympy.ntheory.generate.prime : Return the nth prime
    References
    ==========
    - http://en.wikipedia.org/wiki/Strong_pseudoprime
    - "Lucas Pseudoprimes", Baillie and Wagstaff, 1980.
      http://mpqs.free.fr/LucasPseudoprimes.pdf
    - https://en.wikipedia.org/wiki/Baillie-PSW_primality_test
    """
    if isinstance(n, (Float, float)):
        return False
    n = int(n)

    # Step 1, do quick composite testing via trial division.  The individual
    # modulo tests benchmark faster than one or two primorial igcds for me.
    # The point here is just to speedily handle small numbers and many
    # composites.  Step 2 only requires that n <= 2 get handled here.
    if n in [2, 3, 5]:
        return True
    if n < 2 or (n % 2) == 0 or (n % 3) == 0 or (n % 5) == 0:
        return False
    if n < 49:
        return True
    if (n % 7) == 0 or (n % 11) == 0 or (n % 13) == 0 or (n % 17) == 0 or \
       (n % 19) == 0 or (n % 23) == 0 or (n % 29) == 0 or (n % 31) == 0 or \
       (n % 37) == 0 or (n % 41) == 0 or (n % 43) == 0 or (n % 47) == 0:
        return False
    if n < 2809:
        return True
    if n <= 23001:
        return pow(2, n, n) == 2 and n not in [7957, 8321, 13747, 18721, 19951]

    # bisection search on the sieve if the sieve is large enough
    from sympy.ntheory.generate import sieve as s
    if n <= s._list[-1]:
        l, u = s.search(n)
        return l == u

    # If we have GMPY2, skip straight to step 3 and do a strong BPSW test.
    # This should be a bit faster than our step 2, and for large values will
    # be a lot faster than our step 3 (C+GMP vs. Python).
    from sympy.core.compatibility import HAS_GMPY
    if HAS_GMPY == 2:
        from gmpy2 import is_strong_prp, is_strong_selfridge_prp
        return is_strong_prp(n, 2) and is_strong_selfridge_prp(n)

    # Step 2: deterministic Miller-Rabin testing for numbers < 2^64.  See:
    #    https://miller-rabin.appspot.com/
    # for lists.  We have made sure the M-R routine will successfully handle
    # bases larger than n, so we can use the minimal set.
    if n < 341531:
        return mr(n, [9345883071009581737])
    if n < 885594169:
        return mr(n, [725270293939359937, 3569819667048198375])
    if n < 350269456337:
        return mr(n, [4230279247111683200, 14694767155120705706, 16641139526367750375])
    if n < 55245642489451:
        return mr(n, [2, 141889084524735, 1199124725622454117, 11096072698276303650])
    if n < 7999252175582851:
        return mr(n, [2, 4130806001517, 149795463772692060, 186635894390467037, 3967304179347715805])
    if n < 585226005592931977:
        return mr(n, [2, 123635709730000, 9233062284813009, 43835965440333360, 761179012939631437, 1263739024124850375])
    if n < 18446744073709551616:
        return mr(n, [2, 325, 9375, 28178, 450775, 9780504, 1795265022])

    # We could do this instead at any point:
    # if n < 18446744073709551616:
    #   return mr(n, [2]) and is_extra_strong_lucas_prp(n)

    # Here are tests that are safe for MR routines that don't understand
    # large bases.
    # if n < 9080191:
    #    return mr(n, [31, 73])
    # if n < 19471033:
    #    return mr(n, [2, 299417])
    # if n < 38010307:
    #    return mr(n, [2, 9332593])
    # if n < 316349281:
    #    return mr(n, [11000544, 31481107])
    # if n < 4759123141:
    #    return mr(n, [2, 7, 61])
    # if n < 105936894253:
    #    return mr(n, [2, 1005905886, 1340600841])
    # if n < 31858317218647:
    #    return mr(n, [2, 642735, 553174392, 3046413974])
    # if n < 3071837692357849:
    #    return mr(n, [2, 75088, 642735, 203659041, 3613982119])
    # if n < 18446744073709551616:
    #    return mr(n, [2, 325, 9375, 28178, 450775, 9780504, 1795265022])

    # Step 3: BPSW.
    #
    #  Time for isprime(10**2000 + 4561), no gmpy or gmpy2 installed
    #     44.0s   old isprime using 46 bases
    #      5.3s   strong BPSW + one random base
    #      4.3s   extra strong BPSW + one random base
    #      4.1s   strong BPSW
    #      3.2s   extra strong BPSW

    # Classic BPSW from page 1401 of the paper.  See alternate ideas below.
    return mr(n, [2]) and is_strong_lucas_prp(n)

    # Using extra strong test, which is somewhat faster
    # return mr(n, [2]) and is_extra_strong_lucas_prp(n)

    # Add a random M-R base
    #import random
# return mr(n, [2, random.randint(3, n-1)]) and is_strong_lucas_prp(n)


def mr(n, bases):
    """Perform a Miller-Rabin strong pseudoprime test on n using a
    given list of bases/witnesses.
    References
    ==========
    - Richard Crandall & Carl Pomerance (2005), "Prime Numbers:
      A Computational Perspective", Springer, 2nd edition, 135-138
    A list of thresholds and the bases they require are here:
    http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants_of_the_test
    Examples
    ========
    >>> from sympy.ntheory.primetest import mr
    >>> mr(1373651, [2, 3])
    False
    >>> mr(479001599, [31, 73])
    True
    """
    from sympy.ntheory.factor_ import trailing
    from sympy.polys.domains import ZZ

    n = as_int(n)
    if n < 2:
        return False
    # remove powers of 2 from n-1 (= t * 2**s)
    s = trailing(n - 1)
    t = n >> s
    for base in bases:
        # Bases >= n are wrapped, bases < 2 are invalid
        if base >= n:
            base %= n
        if base >= 2:
            base = ZZ(base)
            if not _test(n, base, s, t):
                return False
    return True
