
# coding: utf-8
from collections import defaultdict
import os
import re
import jieba
import codecs
import sys
import pandas as pd

"""
1. 文本切割
"""

def sent2word(sentence):
    """
    Segment a sentence to words
    Delete stopwords
    """
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)
    f = open('stopWord.txt', 'rb') 
    stopwords = f.readlines()
    newSent = []
    for word in segResult:
        if word in stopwords:
            # print "stopword: %s" % word
            continue
        else:
            newSent.append(word)

    return newSent

#print(sent2word('得到的都是侥幸啊'))

"""
2. 情感定位
"""
def classifyWords(wordDict):
    # (1) 情感词
    #with open('BosonNLP_sentiment_score.txt', 'rb') as f1:
     #   senList = f1.readlines()
        #print(type(senList))
    senDict = defaultdict()
    for s in open('BosonNLP_sentiment_score.txt', 'rb').readlines():
        #print(type(s))
        #print(str(s).encode('utf-8'))
        s = str(s.decode('utf-8'))      
        if len(s.split())<2: 
            continue 
        else: senDict[s.split()[0]] = s.split()[1]
    # (2) 否定词
    f2 = open('notDict.txt', 'rt',encoding='gb18030')
    notList1 = f2.readlines()
    notList = list()
    for ele in notList1: 
        notList.append(ele.rstrip()) 
        
    #print(notList)
    # (3) 程度副词
   
    #f3 = open('degreeDict.txt', 'rb')
    #print(f3)
    #degreeList = f3.readlines()
    degreeDict = defaultdict()
    for d in open('degreeDict.txt', 'rb').readlines():
        #d.decode('utf-8')
        #print(type(d))
        #print(d)
        d = str(str(d).encode('utf-8'))
        if len(d.split())<2: 
            continue 
        else: degreeDict[d.split()[0]] = d.split()[1]       
        
    
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    
    #count =0;
    for word in wordDict.keys():
        #count = count+1
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
        #if count == 100: break   
        if senWord.get(1) == None: return 0    
        return senWord.get(1)
    #return senWord, notWord, degreeWord
    
#print(sys.getdefaultencoding())

# lst = sent2word('无意中看到关于这个网站的报道，对这个模式很感兴趣，来体验一下。正好需要换个笔记本，如果借到钱就不犹豫直接上苹果的pro了。如果无法成功的话就将就点换个联想的了。我在招行工作，收入挺稳定的，大家可以放心。')
# dic = dict()
# for ele in lst:
#     dic[ele] =1
#     #print(ele)
# print(classifyWords(dic))

def xlsx_csv_com(output):
    # coding:utf-8
    import glob
    interesting_files = glob.glob("{}/*.csv".format(output))
    header_saved = False
    with open('{}/full_review.csv'.format(output), 'w', encoding='gb18030') as fout:
        for filename in interesting_files:
            print(filename)
            with open(filename, 'r',encoding='utf-8') as fin:
                header = next(fin)
                if not header_saved:
                    fout.write(header)
                header_saved = True
                for line in fin:
                    fout.write(line)
def sentiment(row):
    review = row['评论内容']
    lst = sent2word(str(review))
    dic = dict()
    for ele in lst:
         dic[ele] =1
         #print(ele)
    #return classifyWords(dic)
    print(classifyWords(dic))

    return pd.Series([lst,classifyWords(dic)],index=['seg','sentiment'])
def frequency(file_name):
    import re
    file_pd = pd.read_csv(file_name)
    all_lst = []
    for ele in list(file_pd['seg']):
        ele_lst = re.sub(r'\[|\]|\'','',ele)
        #print(ele_lst.split(','))
        all_lst+=ele_lst.split(',')

    stop_lst = [' ，','  ',' 。',' \\r\\n',' ','',' ！',' （',' !',' ?']
    all_lst = [ele for ele in all_lst if ele not in stop_lst]
    from collections import Counter
    result = Counter(all_lst)
    print(result)

    target_text = open('导出/词频.txt', 'w')
    target_text.write('词频'+ '\t' + '频数')
    for ele in result:
        print(ele, result[ele])
        target_text.write(ele + '\t' + str(result[ele]) + '\n')
    new_lst = [all_lst[pos]+'-'+all_lst[pos+1] for pos in range(len(all_lst)-1)]

    target_text = open('导出/关联词.txt','w')
    target_text.write('关联词'+ '\t' +'频数')
    for ele in Counter(new_lst):
        print(ele,Counter(new_lst)[ele])
        target_text.write(ele+'\t'+str(Counter(new_lst)[ele])+'\n')


if __name__ =='__main__':
    # output = '导出'
    # xlsx_csv_com(output)
    #full_review_pd = pd.read_csv('导出/full_review.csv')
    #full_review_pd[['seg','sentiment']] = full_review_pd.apply(lambda row:sentiment(row),axis=1)
    #full_review_pd.to_csv('导出/full_review_updated.csv',index=False)
    file_name = '导出/full_review_updated.csv'
    frequency(file_name)



