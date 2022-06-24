
import pyLDAvis
# import 进度条
import os
import gensim
from gensim import corpora

import re
import pandas as pd
import numpy as np
import jieba
from tqdm import tqdm
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

def find_chinese(word,stop):
#     pattern = re.compile(r'[^\u4e00-\u9fa5]')
#     chinese = re.sub(pattern, '', file)

    # a=[re.sub('[^\u4e00-\u9fa5]','',i) for i in stop]
    chinese =word
    for i in word:
        if i in stop:
            chinese.remove(i)


    return chinese

# 读取停用词列表
def get_stopword_list(file):
    with open(file, 'r', encoding='utf-8') as f:    # 
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


# 3. 导入停止词的语料库,
# 对文本进行停止词的去除
def drop_stops(Jie_content, stop):
    clean_content = []
    # all_words = []
    for j_content in Jie_content:
        line_clean = []
        for line in j_content:
            if line in stop:
                continue
            line_clean.append(line)
        clean_content.append(line_clean)

    return clean_content
def clean(doc_complete,stop):
    #doc1 = "百度、360、谷歌搜索通过关键词，可以帮助用户查找搜索到一段时间内的互联网信息，全面掌握网络舆情。"
    #doc2 = "搜狐/网易/新浪微博搜索、微信搜一搜通过借助这类平台，可以帮助用户免费查找监测在社交网络平台上的一些与己相关的网络舆情。"
    #doc3 = "一呼百应、中搜企业搜索这类平台主要可以用来查找和监测垂直平台及B2B网站上的信息。"
    #doc4 = "网易/头条/搜狐/百度新闻搜索借助这些平台则可以帮助用户查找和监测主流网络媒体上与己相关的各类新闻信息。"
    #doc5 = "奇虎网、百度博客搜索最后这类平台则可以帮助用户免费查找和监测论坛和博客等社区上的信息。"
    # 整合文档数据
    #doc_complete = [doc1, doc2, doc3, doc4, doc5]
    

    # stopword_file = './hit_stopwords.txt'
    # stop = get_stopword_list(stopword_file)    # 获得停用词列表
    df_contents = doc_complete
    # list of list 结构
    Jie_content,skip = [], []
    for jj in tqdm(df_contents):
        # start+=1
        # 进度条.progress_bar(start, len(df_contents))

        df_content =''.join(re.findall('[\u4e00-\u9fa5]', str(jj)))
        if df_content=='':
            skip.append(df_contents.index(jj))
            continue
        split_content = jieba.lcut(df_content,cut_all=False)
        split_content = find_chinese(split_content,stop)
        Jie_content .append( split_content)
        # clean_content = drop_stops(Jie_content, ['新疆'])
        
        #print('停止词:',stop)
        #print('停止词的去除:',clean_content)
    # 4. 进行LDA主题模型
    # 使用gensim.dictionary 生成word2vec
    return Jie_content,skip
colors = ['red', 'green', 'blue', 'gray', '#88ff66',
          '#ff00ff', '#ffff00', '#8888ff', 'black',]
markers = ['v', '^', 'o', '*', 'h', 'd', 'D', '>', 'x']
def kMeans(data, n_clusters=5):
    kmeanspredictr=KMeans(n_clusters).fit(data)
    catagory=kmeanspredictr.labels_
    for label in range(n_clusters):
        clusterIndex =data[catagory==label]
        plt.scatter(clusterIndex[:, 0], clusterIndex[:, 1],
                    c=colors[label], marker=markers[label], s=100)
    plt.title("kMeans",loc="center")

    plt.savefig('kMeans图.png', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    path = "./data/article.csv"
    df=pd.read_csv(path,encoding="utf_8_sig")
    df= df.drop_duplicates(subset=['text'],keep='first')#删除重复数据
    df =df.dropna()

    followers_count=[]
    stop = get_stopword_list('hit_stopwords.txt')
    doc_complete = list(df['text'])
    clean_content,skip = clean(doc_complete)
    if skip!=[]:
        df.drop(df.iloc[skip], axis=1)
    df.to_csv(path, encoding="utf_8_sig", header=True, index=False)
    support_count = df['support_count']
    dictionary = corpora.Dictionary(clean_content)

    # 对clean_content 根据dictionary映射构造向量
    print('对clean_content根据dictionary映射构造词频向量')
    corpus = [dictionary.doc2bow(clean_c) for clean_c in tqdm(clean_content)]
    # print(corpus[0])
    print('构造映射矩阵')#映射矩阵
    corpus = [[(c,d*support_count[index]) for c,d in  i]  for index,i in tqdm(enumerate( corpus))]
    
    if os.path.isfile('lda.model'):
        lda = gensim.models.ldamodel.LdaModel.load('lda.model')
    else:
        # print(corpus[0])
        #print(corpus)#映射矩阵
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
        lda.save('lda.model')
    #print(lda.print_topics(num_topics=20, num_words=10))
    topics=[]
    for i in range(len(corpus)):
        doc_topic=dict(lda.get_document_topics(corpus[i]))
        values=list(doc_topic.values())
        keys=list(doc_topic.keys())
        topic=keys[values.index(max(values))]
        topics.append([topic,len(keys)])
        # doc_topic = lda.get_document_topics(corpus[i])
        # topics+=doc_topic
    # topics=np.array(topics)[:,[1,0]]
    topics = np.array(topics)
    kMeans(topics, n_clusters=5)
# 每一个句子 所属主题推断
#     lda.save('lda.model')
#     for e, values in enumerate(lda.inference(corpus)):###文章分布
#         print(doc_complete[e])
#         for ee, value in enumerate(values):###推断主题
#             print('\t主题%d推断值%.2f' % (ee, value))
#         break

'''    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=100000) 
1.去掉出现次数低于no_below的 
2.去掉出现次数高于no_above的。注意这个小数指的是百分数 
3.在1和2的基础上，保留出现频率前keep_n的单词'''
