# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

import codecs
import re

class CorpusParser:
    def __init__(self, filename):
        self.filename = filename
        self.regex = re.compile('^#\s*\d+')
        self.corpus = dict()

    def parse(self):
        with codecs.open(self.filename, 'r') as f:
            s = ''.join(f.readlines())
        blobs = s.split('#')[1:]
        for x in blobs:
            text = x.split()
            docid = text.pop(0)
            self.corpus[docid] = text

    def get_corpus(self):
        return self.corpus

class QueryParser:
    def __init__(self, filename):
        self.filename = filename
        self.queries = []

    def parse(self):
        with codecs.open(self.filename, 'r' ) as f:
            lines = ''.join(f.readlines())
        self.queries = [x.rstrip().split() for x in lines.split('\n')[:-1]]

    def get_queries(self):
        return self.queries

if __name__ == '__main__':
    qp = QueryParser('./data/queries.txt')
    print qp.get_queries()