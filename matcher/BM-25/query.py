# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

from invdx import build_data_structures
from rank import score_BM25
import operator


class QueryProcessor:
    def __init__(self, queries, corpus):
        self.queries = queries
        self.index, self.dlt = build_data_structures(corpus)

    def run(self):
        results = []
        for query in self.queries:
            results.append(self.run_query(query))
        #results.append(self.run_query(self.queries))
        return results

    def run_query(self, query):
        query_result = dict()
        for term in query:
            if term in self.index:
                doc_dict = self.index[term]
                for docid, freq in doc_dict.iteritems():
                    score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
                                       dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length())
                    if docid in query_result:
                        query_result[docid] += score
                    else:
                        query_result[docid] = score
        return query_result