#!/usr/bin/python

import os
import sys
import math
from collections import defaultdict

def hamming(s1, s2):
    #Return the Hamming distance between equal-length sequences
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

def levenshtein(a,b):
    #Calculates the Levenshtein distance between a and b.
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]

def cosine(vec1, vec2):
     # vec1 and vec2 are arrays of 2-tuples where vec[i][0] is a unique key and vec[i][1] is a frequency
     numerator = 0
     d = defaultdict(int)
     for p1 in vec1:
	d[p1[0]] = p1[1]
     for p2 in vec2:
	numerator += d[p2[0]]*p2[1]

     sum1 = sum([vec1[x][1]**2 for x in range(len(vec1))])
     sum2 = sum([vec2[x][1]**2 for x in range(len(vec2))])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def jaccard(vec1, vec2):
     s1 = set([vec1[x][0] for x in range(len(vec1))])
     s2 = set([vec2[x][0] for x in range(len(vec2))])
     return float(len(s1 & s2)) / float(len(s1 | s2))

