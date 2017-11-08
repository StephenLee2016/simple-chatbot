# -*- coding:utf-8 -*-
# __author__=='jrlimingyang@jd.com'
import os
import re
import jieba
import codecs
import numpy as np
import pandas as pd
from train_w2v import train
from gensim.models import KeyedVectors

import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
1.将对话数据拆成question、answer两个文件
2.将question转换成sentence vector
3.获得训练vector model的数据
'''

def get_qa(file_path):
    '''
    :param file_path:原始语料路径
    :return: question 和 answer
    '''
    corpus = pd.read_csv(file_path, error_bad_lines=True)
    # domain = ['闲谈逸致','文理类','生活相关','职场职业','城市问题','教育类','情感类','旅游景点','电影','考试相关','名人巨星','生活常识','歌曲歌词','国家相关']
    # corpus = corpus[corpus[3].isin(domain)]
    # corpus = corpus[[10,0]]
    # corpus.columns = ['question','answer']
    corpus['question_seg'] = corpus['question'].apply(lambda x: _remove_stopwords(' '.join(jieba.cut(str(x)))))
    corpus.index = range(0,corpus.shape[0])

    return corpus


def sentence2vec(corpus, vec_model):
    '''
    :param sentence:
    :param vec_model: 训练好的词向量模型
    :return: 句子的向量化表示
    '''
    vecFrame = pd.DataFrame(np.zeros((corpus.shape[0],200)))
    corpus['sent2vec'] = corpus['question'].apply(lambda x: ' '.join(jieba.cut(str(x))))

    for index, row in corpus.iterrows():
        sentVec = np.zeros((1, 200))
        if (index+1) % 1000 == 0:
            logging.info(u'%s lines complete'%(index+1))
        word_count = 0

        for word in row['sent2vec'].split(' '):
            try:
                word_count += 1
                sentVec += vec_model[word]
            except Exception:
                pass

        vecFrame.iloc[index,:] = sentVec[0]/float(word_count)
    with open(os.path.join(os.getcwd(),'cache/corpus.txt'), 'w') as f:
        for index, row in corpus.iterrows():
            f.write('# '+ str(index))
            f.write('\n')
            f.write(row[2])
            f.write('\n')
    del corpus['sent2vec']
    corpus = pd.concat([corpus,vecFrame], axis=1)
    return corpus


def _remove_stopwords(segwords):
    stopwords = [stopword for stopword in codecs.open(os.path.join(os.getcwd(), 'stopwords/stopwords.txt'), 'r', 'utf-8').read()]
    wordlist = ''
    for word in segwords.split(' '):
        if word not in stopwords:
            wordlist += word + ' '
    return wordlist

def get_vector_data(corpus):
    '''
    :param file_path: 原始语料路径
    :return: 分词后的预料数据，用于vector model训练
    '''
    #corpus = pd.read_csv(file_path, header=None, error_bad_lines=True)

    vec_data = corpus['question'] + corpus['answer']
    vec_data = vec_data.apply(lambda x: _remove_stopwords(' '.join(jieba.cut(str(x)))))
    return vec_data

def main():
    # 训练闲聊模型需要的数据问题件路径
    corpus_path = './corpus/corpus_1509417971.2.csv'
    # 需要保存的向量数据路径
    vector_path = './corpus/vec_data.csv'

    corpus = get_qa(corpus_path)
    # 如果vector model 存在则直接载入
    # 这里有一点小trick，如果语料发生了变化，那么词向量是否需要重新训练其实是需要看效果而定
    # 假如需要重新训练词向量模型，只需要将model文件夹下的四个文件删除，然后重新运行程序就行
    if os.path.exists('./model/all.zh.text.vector'):
        vec_model = KeyedVectors.load_word2vec_format('./model/all.zh.text.vector')
    else:
        vec_data = get_vector_data(corpus)
        vec_data.to_csv(vector_path, index=None, header=None, encoding='utf-8')
        vec_model = train(vector_path)


    sent2vec = sentence2vec(corpus, vec_model)
    del sent2vec['question_seg']
    # 存储转化好的sentence向量
    sent2vec.to_csv('./cache/sentence2vec.csv', index=None, sep='|', header=None)


if __name__ == '__main__':
    main()