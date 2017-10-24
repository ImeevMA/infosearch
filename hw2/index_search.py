#!/usr/bin/env python
import argparse
import document_pb2
import struct
import gzip
import sys

from searcher import Searcher

def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('args', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line().args
    search = Searcher()
    result = search.search_word(args.pop())
    for word in args:
        if word != '&':
            result &= search.search_word(word)
    print result
