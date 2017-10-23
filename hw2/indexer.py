#!/usr/bin/env python
from array import array
from compression import varbyte
from docreader import DocumentStreamReader
from doc2words import extract_words
from nltk.corpus import stopwords

from base64 import b64encode

class Indexer:

    def __init__(self, dict_name="dictionary", index_name="index"):
        self.index = dict()
        self.links = list()
        self.dict_name = dict_name
        self.index_name = index_name

    def handle_doc(self, doc, doc_id):
        self.links.append(doc.url)
        words = set(extract_words(doc.text));
        for word in words:
            last_id, arr = self.index.get(word, (0, array('B')))
            for byte in varbyte(doc_id - last_id):
                arr.append(byte)
            self.index[word] = (doc_id, arr)
    
    def save_index(self):
        pos = 0
        size = 0
        fdict = open(self.dict_name, "w")
        findex = open(self.index_name, "wb")
        flinks = open(self.links, "w")
        for word in sorted(self.index.keys()):
            size = len(self.index[word][1])
            fdict.write(word.encode("UTF-8") + " {} {}\n".format(pos, size))
            pos += size
            self.index[word][1].tofile(findex)
        for link in self.links:
            flinks.write(link.encode("UTF-8") + "\n")


#reader = DocumentStreamReader(["/home/mergen/sphere/infosearch/hw2test/1.gz"])
#index = Index()
#for i, doc in enumerate(reader):
#    index.handle_doc(doc, i)
#index.save_index()
