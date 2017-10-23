from array import array
from compression import varbyte

class Searcher:
    def __init__(self, dict_name="dictionary", index_name="index"):
        self.dictionary = open(dict_name, "r")
        self.index = open(index_name, "rb")

    def search_word(self, word):
        self.dictionary.seek(0)
        for line in self.dictionary:
            if word in line.split():
                pos = int(line.split()[1])
                size = int(line.split()[2])
                self.index.seek(pos)
                return set(varbyte(array('B', self.index.read(size)), True))
        return set()

#words = ["ali", "al", "cat", "array"]
#searcher = Search()
#for word in words:
#    print searcher.search_word(word)
