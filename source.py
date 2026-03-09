"""Simple random byte source and entropy calculator."""
import os
from math import log2


def generate(n):
    """Return *n* random bytes."""
    return os.urandom(n)


def entropy(counts):
    """Shannon entropy (bits per symbol) from a list of symbol counts.

    Parameters
    ----------
    counts : list[int]
        Frequency of each symbol (zeros are ignored).

    Returns
    -------
    float
        Entropy in bits per symbol.
    """
    total = sum(counts)
    if total == 0:
        return 0.0
    ent = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            ent -= p * log2(p)
    return ent
