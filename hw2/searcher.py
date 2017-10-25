from os import stat
from array import array
from struct import unpack
from mmhash import get_hash
from compression import varbyte

class Searcher:
    def __init__(
            self,
            dict_name="dictionary",
            index_name="index",
            link_name="links",
            toc_links_name="toc_links"
            ):
        self.get_dict(dict_name)
        self.get_toc_links(toc_links_name)
        self.index = open(index_name, "rb")
        self.links = open(link_name, "rb")

    def get_dict(self, filename):
        self.dictionary = dict()
        dictionary = open(filename, "rb")
        tmp = dictionary.read(24)
        while(tmp):
            unpacked = unpack("qqq", tmp)
            self.dictionary[unpacked[0]] = unpacked[1:]
            tmp = dictionary.read(24)

    def get_toc_links(self, filename):
        self.toc_links = list()
        toc_links = open(filename, "rb")
        tmp = toc_links.read(8)
        while tmp:
            self.toc_links.append(unpack("q", tmp)[0])
            tmp = toc_links.read(8)

    def get_links(self, link_ids):
        links = list()
        for link in link_ids:
            self.links.seek(self.toc_links[link])
            links.append(self.links.readline().strip())
        return links

    def search_word(self, word):
        word_hash = get_hash(word)
        pos, size = self.dictionary.get(word_hash, (0, 0))
        if size == 0:
            return set()
        self.index.seek(pos)
        return set(varbyte(array('B', self.index.read(size)), True))
