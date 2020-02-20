import jieba.analyse
import json
from collections import defaultdict
import pandas as pd
import seaborn as sns
import wordcloud
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC

def open_json_file(filename):
    with open(filename, encoding='utf-8') as f:
        posts = json.load(f)
    return posts

def push_analyse(filename):
    posts = open_json_file(filename)
    total_comments = defaultdict(int)
    total_pushes = defaultdict(int)
    total_hates = defaultdict(int)
    for post in posts:
        for comment in post['comments']:
            user = comment['user']
            total_comments[user] += 1

            if comment['score'] > 0:
                total_pushes[user] += 1
            if comment['score'] < 0:
                total_hates[user] += 1
    count = 0
    for hate in total_hates:
        count += 1
        if count > 20:
            break
    return total_comments, total_pushes, total_hates

def show_distributions(total_comments, total_pushes, total_hates):
    #長條寬度
    width = 0.3
    #抓出推文top20使用者的推文數/推數/噓數
    sorted_cnts = [t[0] for t in sorted(total_comments.items(), key=lambda x: -x[1])][:20]
    y = [total_comments[u] for u in sorted_cnts]
    y_pushes = [total_pushes[u] for u in sorted_cnts]
    y_hates = [total_hates[u] for u in sorted_cnts]

    index = np.arange(len(sorted_cnts))
    plt.bar(index, y, width=width, label="comments")
    plt.bar(index+width, y_pushes, width=width, label="push")
    plt.bar(index+2*width, y_hates, width=width, label="hate")
    #設定X軸名稱、寬度、字體翻轉
    plt.xticks(index + width, sorted_cnts, rotation=90)
    plt.legend()
    plt.show()

def tfidf_analyse(filename):
    font_path = './msj.ttf'
    fword = ''
    posts = open_json_file(filename)
    jieba.load_userdict('dict.txt')
    jieba.analyse.set_stop_words('stop_word.txt')
    for post in posts:
        tags = jieba.analyse.extract_tags(post['content'], topK=50, withWeight=False, allowPOS=())
        # print(tags)
        fword += '/'.join(tags)
    fword_result = jieba.analyse.extract_tags(fword, 500)
    print(type(fword_result))
    # print(fword_result)
    # print(' '.join(fword_result))
    fword_result = ' '.join(fword_result)
    print(type(fword_result))
    wordclouds = wordcloud.WordCloud(background_color='white', font_path=font_path)
    wordclouds.generate(fword_result)
    plt.figure(figsize=(15, 15))
    plt.imshow(wordclouds)
    plt.axis("off")
    plt.show()

def content_analyse(filename):

    words = []
    scores = []
    posts = open_json_file(filename)
    jieba.load_userdict('dict.txt')
    jieba.analyse.set_stop_words('stop_word.txt')

    for post in posts:
        d = defaultdict(int)
        content = post['content']
        if post['score'] != 0:
            for word in jieba.analyse.extract_tags(content, topK=50, withWeight=False, allowPOS=()):
                d[word] += 1
            if len(d) > 0:
                words.append(d)
                scores.append(1 if post['score'] > 0 else 0)

    c_words = []
    c_scores = []

    for post in posts:
        for comment in post['comments']:
            l = comment['content'].strip()
            if l and comment['score'] != 0:
                d = defaultdict(int)
                for word in jieba.analyse.extract_tags(l, topK=50, withWeight=False, allowPOS=()):
                    d[word] += 1
                if len(d) > 0:
                    c_scores.append(1 if comment['score'] > 0 else 0)
                    c_words.append(d)


    dvec = DictVectorizer()
    tfidf = TfidfTransformer()
    X = tfidf.fit_transform(dvec.fit_transform(words))

    c_dvec = DictVectorizer()
    c_tfidf = TfidfTransformer()
    c_X = c_tfidf.fit_transform(c_dvec.fit_transform(c_words))

    svc = LinearSVC()
    svc.fit(X, scores)
    display_top_features(svc.coef_[0], dvec.get_feature_names(), 30)
    display_top_features(svc.coef_[0], dvec.get_feature_names(), 30, select=lambda x: x)
    c_svc = LinearSVC()
    c_svc.fit(c_X, c_scores)
    display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 30)
    display_top_features(c_svc.coef_[0], c_dvec.get_feature_names(), 30, select=lambda x: x)

def display_top_features(weights, names, top_n, select=abs):
    top_features = sorted(zip(weights, names), key=lambda x: select(x[0]), reverse=True)[:top_n]
    top_weights = [x[0] for x in top_features]
    top_names = [x[1] for x in top_features]
    fig, ax = plt.subplots(figsize=(10,8))
    ind = np.arange(top_n)
    bars = ax.bar(ind, top_weights, color='blue', edgecolor='black')
    for bar, w in zip(bars, top_weights):
        if w < 0:
            bar.set_facecolor('red')

    width = 0.30
    ax.set_xticks(ind + width)
    ax.set_xticklabels(top_names, rotation=45, fontsize=12)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show(fig)

def del_stop_words(filename, seg):
    with open(filename, 'r', encoding='utf-8') as f:
        stop_words = f.readlines()
    stop_words = [stop_word.strip() for stop_word in stop_words]

##################################
json_path = 'data.json'
x, y, z = push_analyse(json_path)
show_distributions(x, y, z)
tfidf_analyse(json_path)
content_analyse(json_path)
