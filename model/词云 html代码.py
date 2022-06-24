# %load 词云 html代码.py
import jieba
import wordcloud
import imageio
from matplotlib import pyplot as plt
import re
import time
# 读取文件内容
# text=''
#
# f = open('metadata.txt', encoding='utf-8')
# txt = f.read()
# for i in txt:
#     each_word = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",i)
#     text+=each_word
# # print(txt)
# # jiabe 分词 分割词汇
# txt_list = jieba.lcut(txt)
# string = ' '.join(txt_list)
# string=text1
from LDA import *
import math
# import tqdm
import pyLDAvis.gensim_models as pyls
import datetime
import numpy as np
from perplexity import *
def softmax(x):
 x = np.array(x)
 x = np.exp(x/max(x))
 x.astype('float32')
 if x.ndim == 1:
  sumcol = sum(x)
  for i in range(x.size):
   x[i] = x[i]/float(sumcol)
 if x.ndim > 1:
  sumcol = x.sum(axis = 0)
  for row in x:
   for i in range(row.size):
    row[i] = row[i]/float(sumcol[i])
 return x
#测试结果
def LDA():
    path = "./data/article.csv"
    df=pd.read_csv(path,encoding="utf_8_sig")
    df= df.drop_duplicates(subset=['text'],keep='first')#删除重复数据
    df =df.dropna()
    doc_complete = list(df['text'])
    clean_content,skip = clean(doc_complete,stop)
    if skip!=[]:
        df.drop(df.iloc[skip], axis=1)
    df.to_csv(path, encoding="utf_8_sig", header=True, index=False)
    support_count = df['support_count']
    dictionary = corpora.Dictionary(clean_content)

    # 对clean_content 根据dictionary映射构造向量
    print('对clean_content根据dictionary映射构造词频向量')
    corpus = [dictionary.doc2bow(clean_c) for clean_c in tqdm(clean_content)]
    # print(corpus[0])
    # print('构造映射矩阵')#映射矩阵
    #
    # corpus = [[(c,d*support_count[index]) for c,d in  i]  for index,i in tqdm(enumerate( corpus))]
    # print(corpus[0])
    print('构造映射矩阵')#映射矩阵
    time_complete = df['time']
#     struct_time = time.strptime('2021/8/9','%Y/%m/%d')
#     end_time=int(time.mktime(struct_time)) 
    now_time = int(time.mktime(datetime.datetime.now().timetuple()))
    new_time=np.array([int(time.mktime(time.strptime(i,'%Y/%m/%d')))  for i in time_complete])
    # print(max(new_time))result+=(-x)*math.log(x,2)
    # new_time=softmax()*now_time
    follow_count = np.array(df['follow_count'])

    support_count = np.array(df['support_count'])
    follow_count=-support_count*follow_count*np.log(softmax(support_count*follow_count))*sum(support_count*follow_count)
    support_count=softmax(new_time)*now_time
    corpus_t=np.log(follow_count*support_count)
    where_are_inf = np.isinf(corpus_t)
    corpus_t[where_are_inf] = 0
    print('dealing support_count ...')
    corpus = [[(c,round(d*corpus_t[index])) for c,d in  i]  for index,i in tqdm(enumerate( corpus))]
    # print(corpus[0])
    #print(corpus)#映射矩阵
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=5)
#     print(lda.print_topics(num_topics=20, num_words=10))
    text1=''
    d = pyls.prepare(lda, corpus, dictionary)

    pyLDAvis.save_html(d, 'lda.html')
    print('保存html完毕')
    for i in lda.print_topics(num_words=10):
    #     print(i)
        for text in i[1].split('+'):
    #         print()
            text1+=int(eval(text.split('*')[0]+'*1000'))*text.split('*')[1]
    p = []
    n_max_topics = 10
    for i in tqdm(range(1, n_max_topics)):
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i)
        prep = perplexity(lda, corpus, dictionary, len(dictionary.keys()), i)
        p.append(prep)
    topic=range(1, n_max_topics, 1)
    graph_draw(topic,p)
    return text1
followers_count=[]
stop = get_stopword_list('hit_stopwords.txt')
string=LDA()
# 词云图设置
# string = ' '.join(string)
wc = wordcloud.WordCloud(
        width=1080,         # 图片的宽
        height=1080,         # 图片的高
        background_color='white',   # 图片背景颜色
        font_path='msyh.ttc',    # 词云字体
        # mask=py,     # 所使用的词云图片
        scale=15,
)

# 给词云输入文字
wc.generate(string)
# 词云图保存图片地址
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('词云图')
plt.imshow(wc)
plt.show()
wc.to_file('1.png')
print('保存词云图完毕')