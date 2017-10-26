#!/usr/bin/env python
import sys

from searcher import Searcher
from query_analysis import Query

search = Searcher()
query = Query(search)
while True:
    words = sys.stdin.readline()
    if not words:
        break
    print words,
    result = query.handle_query(words.decode("UTF-8").lower())
    # result = query.handle_query(words)
    print len(result)
    for link in search.get_links(sorted(result)):
        print link
