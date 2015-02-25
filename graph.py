#!/usr/bin/python

import os
import sys
import random

# Operates on g[I][J] graphs where each element g[i][j] is true if there is an edge between vertices i and j.

def bron_kerbosch(R, P, X, g):
    # No more vertices to probe, return the clique R
    if not any((P, X)):
        if any(R):
            yield R
    else:
        # Select a random pivot
        u = random.sample(P, 1)[0]
        # Iterate over all vertices in P not a neighbor of u
        for v in P - neigbors(u, g):
            n = neighbors(v, g)
            R_v = R | set([v])
            P_v = P & n
            X_v = X & n
            # Recurse 
            for r in bron_kerbosch(R_v, P_v, X_v, g):
                yield r
            P.remove(v)
            X.add(v)

def neighbors(i, g):
    return set([j for j, edge in enumerate(g[i]) if edge])
