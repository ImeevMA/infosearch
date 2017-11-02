#!/usr/bin/env python

"""
This just a draft for homework 'near-duplicates'
Use MinshinglesCounter to make result closer to checker
"""

import sys
import re
import mmh3
from docreader import DocumentStreamReader
from itertools import permutations

LIMIT = 17
POWER = 20

class MinshinglesCounter:
    SPLIT_RGX = re.compile(r'\w+', re.U)

    def __init__(self, window=5, n=20):
        self.window = window
        self.n = n

    def count(self, text):
        words = MinshinglesCounter._extract_words(text)
        shs = self._count_shingles(words)
        mshs = self._select_minshingles(shs)

        if len(mshs) == self.n:
            return mshs

        if len(shs) >= self.n:
            return sorted(shs)[0:self.n]

        return None

    def _select_minshingles(self, shs):
        buckets = [None]*self.n
        for x in shs:
            bkt = x % self.n
            buckets[bkt] = x if buckets[bkt] is None else min(buckets[bkt], x)

        return filter(lambda a: a is not None, buckets)

    def _count_shingles(self, words):
        shingles = []
        for i in xrange(len(words) - self.window):
            h = mmh3.hash(' '.join(words[i:i+self.window]).encode('utf-8'))
            shingles.append(h)
        return sorted(shingles)

    @staticmethod
    def _extract_words(text):
        words = re.findall(MinshinglesCounter.SPLIT_RGX, text)
        return words


def main():
    mhc = MinshinglesCounter()

    """
    You may examine content of given files this way (as example):

    for path in sys.argv[1:]:
        for doc in DocumentStreamReader(path):
            print "%s (text length: %d, minhashes: %s)" % (doc.url, len(doc.text), mhc.count(doc.text))
    """
    
    """
    Write your actual code here.
    Good luck!
    """
    urls = list()
    mshs = dict()
    i = 0
    for path in sys.argv[1:]:
        for doc in DocumentStreamReader(path):
            if doc.url not in urls:
                mshs_loc = mhc.count(doc.text)
                if mshs_loc:
                    urls.append(doc.url)
                    for j_msh in mshs_loc:
                        mshs[j_msh] = mshs.get(j_msh, list())
                        mshs[j_msh].append(i)
                    i += 1
    counter = dict()
    for item in (x for x in mshs.values() if len(x) > 1):
        for pair in (x for x in permutations(item, 2) if x[0] < x[1]):
            counter[pair] = counter.get(pair, 0) + 1
    for item, value in counter.items():
        if value > LIMIT:
            print urls[item[0]], urls[item[1]], float(value) / float(POWER)


if __name__ == '__main__':
    main()
