# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

from parse import *
from query import QueryProcessor
import operator

def main():
    qp = QueryParser(filename='C:\\Users\\jrlimingyang\\PycharmProjects\\chatbot-version2\\cache\\query.txt')
    cp = CorpusParser(filename='C:\\Users\\jrlimingyang\\PycharmProjects\\chatbot-version2\\cache\\corpus.txt')
    qp.parse()
    queries = qp.get_queries()
    cp.parse()
    corpus = cp.get_corpus()
    proc = QueryProcessor(queries, corpus)
    results = proc.run()
    qid = 0
    for result in results:
        sorted_x = sorted(result.iteritems(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        for i in sorted_x[:10]:
            tmp = (qid, qid, i[0], index, i[1])
            print '{:>1}\tQ{:>1}\t{:>4}\t{:>2}\t{:>12}\tL-BM25'.format(*tmp)
            index += 1
        qid  += 1

if __name__ == '__main__':
    main()
