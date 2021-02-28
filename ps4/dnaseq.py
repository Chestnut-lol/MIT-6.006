#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.table = {}
        for pair in pairs:
            self.put(pair[0],pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        if k in self.table:
            self.table[k].append(v)
        else:
            self.table[k] = [v]
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if not k in self.table:
            return []
        else:
            return self.table[k]

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        if not k>0 and k<len(seq):
            raise ValueError('wrong string length!')
        else:
            subseq = ''
            for i in range(k):
                subseq = subseq + next(seq)
            hasher = RollingHash(subseq)
            pos = 0
            while True:
                yield (hasher.current_hash(),(pos,subseq))
                nextitem = next(seq)
                hasher.slide(subseq[0],nextitem)
                subseq = subseq[1:] + nextitem
                pos += 1
                
            
    except StopIteration:
        return
        

    
# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        if not k>0 and k<len(seq):
            raise ValueError('wrong string length!')
        else:
            subseq = ''
            for i in range(k):
                subseq = subseq + next(seq)
            hasher = RollingHash(subseq)
            pos = 0
            while True:
                if pos % m == 0:
                    yield (hasher.current_hash(),(pos,subseq))
                nextitem = next(seq)
                hasher.slide(subseq[0],nextitem)
                subseq = subseq[1:] + nextitem
                pos += 1
                
            
    except StopIteration:
        return


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    table = Multidict()
    for t in intervalSubsequenceHashes(a,k,m):
        table.put(t[0],t[1])
    
    for t in subsequenceHashes(b,k):
        for ah in table.get(t[0]):
            yield (ah[0],t[1][0])
                        

                
            

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
