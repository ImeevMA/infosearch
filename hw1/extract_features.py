
# coding: utf-8

# In[75]:

import sys
import re
import random
from operator import itemgetter

SEG_LEN = 1
SEG_IND_NAME = 41
SEG_IND_FIGS = 42
SEG_IND_SUBSTR = 43
SEG_IND_EXT = 44
SEG_IND_SUBSTR_EXT = 45
SEG_IND_LEN = 46

IS_FIGS = re.compile(r'^\d+$')
IS_SUBSTR = re.compile(r'^\D*\d+\D*$')
IS_SUBSTR_EXT = re.compile(r'^\D*\d+\D*\.\w+$')
IS_EXT = re.compile(r'^.+\.\w+$')

GET_EXT = re.compile(r'\.(\w+)$')


def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):

    features = dict()
    for line in INPUT_FILE_1:
        segments, params = parted(line)
        for item, value in get_seg_info(segments).items():
            features[item] = features.get(item, 0) + value

    i = 0
    for w in sorted(features, key=features.get, reverse=True):
        print w, features[w]
        i += 1
        if (i > 20):
            break

def parted(str):
    segments = list()
    params = list()
    parts = str.strip().split('?')
    if len(parts) > 0:
        segments = [x for x in parts[0].strip().split('/')[3:] if x != '']
    if len(parts) > 1:
        params = parts[1].strip().split('&')
    return segments, params

def get_seg_info(segments):
    fseg = dict()
    fname = create_name(SEG_LEN, {'len': len(segments)})
    fseg[fname] = fseg.get(fname, 0) + 1
    for n, name in enumerate(segments):
        fname = create_name(SEG_IND_NAME, {'index': n, 'name': name})
        fseg[fname] = fseg.get(fname, 0) + 1

        fname = create_name(SEG_IND_LEN, {'index': n, 'len': len(name)})
        fseg[fname] = fseg.get(fname, 0) + 1

        name_parsed = parse_name(name)
        if (name_parsed is not None):
            name_parsed['params']['index'] = n
            fseg[fname] = fseg.get(create_name(**name_parsed), 0) + 1
    return fseg

def parse_name(str):
    if (IS_FIGS.match(str)):
        return {'ftype': SEG_IND_FIGS, 'params': dict()}
    if (IS_SUBSTR.match(str)):
        return {'ftype': SEG_IND_SUBSTR, 'params': dict()}
    if (IS_EXT.match(str)):
        ext = GET_EXT.search(str).group(1)
        return {'ftype': SEG_IND_EXT, 'params': {'ext': ext}}
    if (IS_SUBSTR_EXT.match(str)):
        ext = GET_EXT.search(str).group(1)
        return {'ftype': SEG_IND_SUBSTR_EXT, 'params': {'ext': ext}}
    return None

def create_name(ftype, params):

    if ftype == SEG_LEN:
        return "segments:{}".format(params['len'])

    if ftype == SEG_IND_NAME:
        return "segment_name_{}:{}".format(params['index'], params['name'])

    if ftype == SEG_IND_FIGS:
        return "segment_[0-9]_{}:1".format(params['index'])

    if ftype == SEG_IND_SUBSTR:
        return "segment_ext_{}:1".format(params['index'])

    if ftype == SEG_IND_EXT:
        return "segment_substr[0-9]_{}:{}".format(params['index'], params['ext'])

    if ftype == SEG_IND_SUBSTR_EXT:
        return "segment_ext_substr[0-9]{}:{}".format(params['index'], params['ext'])

    if ftype == SEG_IND_LEN:
        return "segment_len_{}:{}".format(params['index'], params['len'])

extract_features(open("./data/urls.lenta.examined"), 1, 1)