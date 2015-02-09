#!/usr/bin/python

import os
import sys

# Operates on g[I][J] graphs where each element g[i][j] is true if there is an edge between vertices i and j.

def bron_kerbosch(R, P, X, g):
    if not any((P, X)):
        yield R
    for v in P[:]:
        n = neighbor(v, g)
        R_v = R | set([v])
        P_v = P & n
        X_v = X & n
        for r in bron_kerbosch(R_v, P_v, X_v, g):
            yield r
        P.discard(v)
        X.add(v)

def neighbor(i, g):
    return set([j for j, edge in enumerate(g[i]) if edge])
