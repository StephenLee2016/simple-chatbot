# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

import numpy as np
import json
import random
import jieba
import pandas as pd # 这里选择pandas存储矩阵，numpy无法解决索引问题，后续解决
from matcher import aimlMatcher
from matcher import vectorMatcher
from matcher import levenshteinMatcher
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger('chat.py')


# 获得问题回答
def get_response(response_frame, inputs_str):
    '''
    for index in list(response_index):
        yield id2sent[str(index)]
    '''

    if response_frame is None:
        return u'这句话我还无法回答...'
    else:
        lm = levenshteinMatcher
        response_frame['leven'] = response_frame[1].apply(lambda x: lm.levenstein_ratio(inputs_str, str(x)))

        # 这里用levenshtein ratio进行过滤，只选大于0.8的匹配度的问题
        response_frame = response_frame[response_frame['leven'] > 0.6]
        try:
            response_frame = response_frame.sort_values(by='cosine',ascending=False)
            if response_frame.shape[0] > 3:
                i = random.randint(0,3)

                if '_RBT_NAME_' in response_frame.iloc[i,0]:
                    return response_frame.iloc[i,0].replace('_RBT_NAME_', '小京灵')
                else:
                    return response_frame.iloc[i,0]
            else:
                if '_RBT_NAME_' in response_frame.iloc[0,0]:
                    return response_frame.iloc[0,0].replace('_RBT_NAME_', '小京灵')
                else:
                    return response_frame.iloc[0,0]
        except:
            return u'这个问题我不知道如何回答哦~~'


if __name__ == '__main__':

    sent_vec = pd.read_csv('./cache/sentence2vec.csv', header=None, sep='|', error_bad_lines=True)
    vec_model = vectorMatcher.load_w2vModel()
    mybot = aimlMatcher.get_rules()
    T = jieba.initialize()
    jieba.load_userdict('./userdict/user_dict.csv')

    while True:
        # 获取用户的输入
        inputs_str = raw_input(u'me > ')
        inputs_seg = ' '.join(jieba.cut(inputs_str))
        # cosine 相似度
        cosine_sim = vectorMatcher.match(inputs_seg, sent_vec, vec_model)
        sent_vec['cosine'] = cosine_sim
        # print sent_vec.head()

        try:
            # 保留余弦相似度top10
            response_frame = sent_vec.sort_values(by='cosine', ascending=False)[:10]
            # print response_frame
        except:
            response_frame = None

        # 获得回答
        if '#NoMatchingTemplate' not in  aimlMatcher.match(inputs_seg, mybot):
            response = aimlMatcher.match(inputs_seg, mybot)
        else:
            print '模板无结果，从相似匹配获得结果'
            response = get_response(response_frame, inputs_str)
        print (u'小京灵 > %s'%response)

        # 需要把之前计算的概率值去掉，要不然计算相似度时候维度不同
        sent_vec = sent_vec.iloc[:, 0:202]