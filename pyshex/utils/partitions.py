"""
Partition utilities -
taken from `Stack Overflow <https://stackoverflow.com/questions/19368375/set-partitions-in-python>`_
"""
from typing import List, Iterator, Tuple

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph


"""
taken from `Stack Overflow <https://codereview.stackexchange.com/questions/1526/finding-all-k-subset-partitions>`_

A python implementation of Knuth's algorithm.
"""


def algorithm_u(ns, m):
    def visit(nv, av):
        ps = [[] for _ in range(m)]
        for jv in range(nv):
            ps[av[jv + 1]].append(ns[jv])
        return ps

    def f(mu, nu, sigma, n, a):
        if mu == 2:
            yield visit(n, a)
        else:
            for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v
        if nu == mu + 1:
            a[mu] = mu - 1
            yield visit(n, a)
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                yield visit(n, a)
        elif nu > mu + 1:
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = mu - 1
            else:
                a[mu] = mu - 1
            if (a[nu] + sigma) % 2 == 1:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] > 0:
                a[nu] = a[nu] - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v

    def b(mu, nu, sigma, n, a):
        if nu == mu + 1:
            while a[nu] < mu - 1:
                yield visit(n, a)
                a[nu] = a[nu] + 1
            yield visit(n, a)
            a[mu] = 0
        elif nu > mu + 1:
            if (a[nu] + sigma) % 2 == 1:
                for v in f(mu, nu - 1, 0, n, a):
                    yield v
            else:
                for v in b(mu, nu - 1, 0, n, a):
                    yield v
            while a[nu] < mu - 1:
                a[nu] = a[nu] + 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
            if (mu + sigma) % 2 == 1:
                a[nu - 1] = 0
            else:
                a[mu] = 0
        if mu == 2:
            yield visit(n, a)
        else:
            for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                yield v

    ng = len(ns)
    ag = [0] * (ng + 1)
    for j in range(1, m + 1):
        ag[ng - m + j] = j - 1
    return f(m, ng, 0, ng, ag) if m > 1 else [[ns]]


def integer_partition(size: int, nparts: int) -> Iterator[List[List[int]]]:
    # Note: can't cache a generator (!)
    # If we've got fewer elements that the minimum number of parts, all bets are off
    for part in algorithm_u(range(size), nparts):
        yield part


def partition_t(T: RDFGraph, nparts: int) -> Iterator[List[RDFGraph]]:
    """
    Partition T into all possible partitions of T of size nparts
    :param T: Set of RDF triples to be partitioned
    :param nparts: number of partitions (e.g. 2 means return all possible 2 set partitions
    :return: Iterator that returns partitions

    We don't actually partition the triples directly -- instead, we partition a set of integers that
    reference elements in the (ordered) set and return those
    """
    t_list = sorted(list(T))        # Sorted not strictly necessary, but aids testing
    return map(lambda element: [RDFGraph([t_list[e] for e in part]) for part in element],
               integer_partition(len(T), nparts))


def partition_2(T: RDFGraph) -> List[Tuple[RDFGraph, RDFGraph]]:
    """
    Partition T into all possible combinations of two subsets
    :param T: RDF Graph to partition
    :return:
    """
    if len(T) == 0:
        yield (RDFGraph(), RDFGraph())
    elif len(T) == 1:
        yield (T, RDFGraph())
        yield (RDFGraph(), T)
    else:
        yield (T, RDFGraph())
        for e in partition_t(T, 2):
            yield (e[0], e[1])
            yield (e[1], e[0])
        yield (RDFGraph(), T)
