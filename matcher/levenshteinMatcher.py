# -*- coding:utf-8 -*-
__author__ = 'jrlimingyang@jd.com'

def levenstein_ratio(s1, s2):
    # 这里用两个字符串的编辑距离比
    # 用ratio可以将距离归一化
    m, n = len(s1), len(s2)
    colsize, matrix = m + 1, []
    for i in range((m + 1) * (n + 1)):
        matrix.append(0)
    for i in range(colsize):
        matrix[i] = i
    for i in range(n + 1):
        matrix[i * colsize] = i
    for i in range(n + 1)[1:n + 1]:
        for j in range(m + 1)[1:m + 1]:
            cost = 0
            if s1[j - 1] == s2[i - 1]:
                cost = 0
            else:
                cost = 2
            minValue = matrix[(i - 1) * colsize + j] + 1
            if minValue > matrix[i * colsize + j - 1] + 1:
                minValue = matrix[i * colsize + j - 1] + 1
            if minValue > matrix[(i - 1) * colsize + j - 1] + cost:
                minValue = matrix[(i - 1) * colsize + j - 1] + cost
            matrix[i * colsize + j] = minValue
    return (m + n - matrix[n * colsize + m])/float(m + n)