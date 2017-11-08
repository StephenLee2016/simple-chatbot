## 基于相似问法的闲聊场景对话机器人（Version 2）

1、getQA.py获得所需的运行文件
2、chat.py进行问答测试
3、matcher 匹配算法实现
- vectorMatcher 句子词向量加权表示的余弦相似度
- levenshteinMatcher 编辑距离匹配
- BM-25 相似匹配

---

<-old version->

#### 与Version 1的不同

- 扩充了机器人的语料库（闲谈逸致,文理类,生活相关,职场职业,城市问题,教育类,情感类,旅游景点,电影,考试相关,名人巨星,生活常识,歌曲歌词,国家相关）

---

> 2017/09/07 <-new version->
> 将相似匹配算法移到了matcher
> 增加了BM-25匹配算法
