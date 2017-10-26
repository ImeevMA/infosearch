#!/usr/bin/env python
from compression import varbyte, simple9, VARBYTE, SIMPLE9
from docreader import DocumentStreamReader
from doc2words import extract_words
from mmhash import get_hash
from struct import pack, calcsize

class Indexer:

    def __init__(
            self,
            compression=VARBYTE,
            dict_name="dictionary",
            index_name="index",
            link_name="links",
            toc_links_name="toc_links"
            ):
        self.compression = compression
        self.index = dict()
        self.links = list()
        self.dict_name = dict_name
        self.index_name = index_name
        self.link_name = link_name
        self.tocl_name = toc_links_name

    def handle_doc(self, doc, doc_id):
        self.links.append(doc.url)
        words = set(extract_words(doc.text));
        for word in words:
            word_hash = get_hash(word.encode("UTF-8"))
            last_id, arr = self.index.get(word_hash, (0, list()))
            arr.append(doc_id - last_id)
            self.index[word_hash] = (doc_id, arr)

    def save_index(self):
        pos = 0
        size = 0
        fdict = open(self.dict_name, "wb")
        findex = open(self.index_name, "wb")
        flinks = open(self.link_name, "wb")
        ftoclinks = open(self.tocl_name, "wb")
        fdict.write(pack("b", self.compression))
        if (self.compression == SIMPLE9):
            compression = simple9
        else:
            compression = varbyte
        for word_hash in sorted(self.index.keys()):
            arr = compression(self.index[word_hash][1])
            size = len(arr) * arr.itemsize
            arr.tofile(findex)
            fdict.write(pack("qqq", word_hash, pos, size))
            pos += size
        for link in self.links:
            ftoclinks.write(pack("q", flinks.tell()))
            flinks.write(link.encode("UTF-8") + "\n")
