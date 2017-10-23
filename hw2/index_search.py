from array import array
from compression import varbyte

def search(words):
    dictionary = open("dictionary")
    index = open("index", "rb")
    for word in words:
        dictionary.seek(0)
        arr = search_word(word, dictionary, index)
        print arr
        if arr:
            print varbyte(arr, True)

def search_word(word, dictionary, index):
    for line in dictionary:
        if word in line.split():
            pos = int(line.split()[1])
            size = int(line.split()[2])
            index.seek(pos)
            return array('B', index.read(size))
    return None

search(["ali", "al", "cat"])
