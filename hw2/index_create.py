#!/usr/bin/env python
import argparse
import document_pb2
import struct
import gzip
import sys

from indexer import Indexer
from compression import VARBYTE, SIMPLE9
from docreader import DocumentStreamReader

def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('args', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_command_line().args
    compression = args.pop(0)
    reader = DocumentStreamReader(args)
    if compression == "simple9":
        compression = SIMPLE9
    else:
        compression = VARBYTE
    indexer = Indexer(compression)
    for doc_id, doc in enumerate(reader):
        indexer.handle_doc(doc, doc_id)
    indexer.save_index()
