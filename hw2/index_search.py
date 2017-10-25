#!/usr/bin/env python
import sys

from searcher import Searcher

search = Searcher()
while True:
    words = sys.stdin.readline()
    if not words:
        break
    print words,
    words = [x.strip() for x in words.decode("UTF-8").lower().split("&")]
    result = search.search_word(words.pop())
    for word in words:
        result &= search.search_word(word)
    print len(result)
    for link in search.get_links(sorted(result)):
        print link
