# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

import os
import gensim
import jieba
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def load_w2vModel():
    '''
        加载 pre-trained 词向量模型
        用来将句子向量化
    '''
    assert os.path.exists('./model/all.zh.text.vector')
    logging.info(u'开始加载 pre-trained 向量模型...')
    vec_model = gensim.models.KeyedVectors.load_word2vec_format('./model/all.zh.text.vector')
    logging.info(u'模型加载完毕')
    return vec_model

def input2vec(inputs_str, vec_model):
    '''
        用户输入转化为向量表示
    '''
    sent_vec = np.zeros((1,200))

    vocab_num = 0
    for word in inputs_str.split(' '):
        try:
            vocab_num += 1
            sent_vec += vec_model[word]
        except Exception:
            pass
    return sent_vec / float(vocab_num)

def match(inputs_str, sent_vec, vec_model):
    '''
        句子向量化的处理方式就是简单的加权平均
        可以用其他的方式继续优化
    '''
    input_vec = input2vec(inputs_str, vec_model)
    cosine = cosine_similarity(input_vec, sent_vec.iloc[:, 2::])[0]

    return cosine