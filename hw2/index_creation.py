#!/usr/bin/env python
from docreader import DocumentStreamReader
from doc2words import extract_words

import argparse
import document_pb2
import struct
import gzip
import sys

def get_index(doc, index='index.txt'):
    words = extract_words(doc.text)
    fd = open(index, "w")
    for word in words:
        fd.write(word.encode("UTF-8") + '\n')
    fd.close()

def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()

if __name__ == '__main__':
    reader = DocumentStreamReader(parse_command_line().files)
    for doc in reader:
        get_index(doc);
        print "%s\t%d bytes" % (doc.url, len(doc.text))
        break
