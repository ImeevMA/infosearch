#!/usr/bin/env python
from array import array
from compression import varbyte
from docreader import DocumentStreamReader
from doc2words import extract_words
from nltk.corpus import stopwords

from base64 import b64encode

def doc_get_words(doc, doc_id, result = dict()):
   # sw = set(stopwords.words('russian')) | set(stopwords.words('english'));
    words = set(extract_words(doc.text));
    for word in words:
        result[word] = add_to_index(result.get(word, (0, array('B'))), doc_id)
    return result

def add_to_index(last, num):
    last_id, arr = last
    for byte in varbyte(num - last_id):
        arr.append(byte)
    return (num, arr)

def save_index(index):
    pos = 0
    size = 0
    fdict = open("dictionary", "w")
    findex = open("index", "w")
    for word in sorted(index.keys()):
        size = len(index[word][1])
        fdict.write(word.encode("UTF-8") + " {} {}\n".format(pos, size))
        pos += size
        index[word][1].tofile(findex)






reader = DocumentStreamReader(["/home/mergen/sphere/infosearch/hw2test/1.gz"])

result = dict()
for i, doc in enumerate(reader):
    doc_get_words(doc, i, result)

#save_index(result)
#for i, v in result.items():
#    print i.encode('UTF-8'), v
