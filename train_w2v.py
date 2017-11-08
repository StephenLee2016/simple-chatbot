# -*- coding:utf-8 -*-
# __author__ = 'jrlimingyang'

import logging
import os.path
import sys
import multiprocessing

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence



def train(corpus_path):
    path = './'
    program = os.path.basename(path + 'train_w2v.py')
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    inp, outp1, outp2 = corpus_path, path + 'model/all.zh.text.model', path + 'model/all.zh.text.vector'
    model = Word2Vec(LineSentence(inp), size=200, window=5, min_count=2,
                     workers=multiprocessing.cpu_count())
    model.save(outp1)
    model.wv.save_word2vec_format(outp2, binary=False)

    return model

