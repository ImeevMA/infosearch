from bs4 import BeautifulSoup


def get_shuffles (text):
    print text
    return set(text[x:x+8] for x in xrange(len(text) - 8))

tabl = dict()
for i in xrange(1, 13):
    file = open("data/{}.html".format(i))
    soup = BeautifulSoup(file, "html5lib")
    for word in get_shuffles(soup.get_text()):
        tabl[word] = tabl.get(word, []) + [i]
    file.close()

for x in tabl.keys():
    print x,

for i in xrange(1, 12):
    for j in xrange(i+1, 13):
        a = 0
        b = 0
        for l in tabl.values():
            if i in l or j in l:
                a += 1
            if i in l and j in l:
                b += 1
        if (4 * b  > 3 * a):
            print "{}.html {}.html".format(i, j)

