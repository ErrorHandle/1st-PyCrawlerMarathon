import jieba.analyse
import json
from collections import defaultdict
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import seaborn as sns
import matplotlib.pyplot as plt


json_path = 'data.json'
# with open(json_path) as f:
#     posts = json.load(f)
# jieba.load_userdict('dict.txt')
# jieba.analyse.set_stop_words('stop_word.txt')
# reset = 0
# d = defaultdict()
# fword = ''
# for post in posts:
#     tags = jieba.analyse.extract_tags(post['content'], topK=50, withWeight=False, allowPOS=())
#     fword += '/'.join(tags)
#
# print(fword)
# fword_result = jieba.analyse.extract_tags(fword, 1000)
# print(fword_result)

# def words_frequency_analysis(wordlist):
#     count
#     for word in wordlist:

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
    return total_comments, total_pushes, total_hates

def show_distributions(counts, pushes, hates):
    sorted_cnts = [t[0] for t in sorted(counts.items(), key=lambda x: -x[1])][:20]
    y = [counts[u] for u in sorted_cnts]
    y_pushes = [pushes[u] for u in sorted_cnts]
    y_hates = [hates[u] for u in sorted_cnts]
    x = range(len(y))

    f,ax = plt.subplots(figsize=(10, 6))
    sns.set_color_codes('pastel')
    plt.plot(x, y, label='Total {}'.format('comments'), color='blue')
    plt.plot(x, y_pushes, label='Total {}'.format('pushes'), color='green')
    plt.plot(x, y_hates, label='Total {}'.format('hates'), color='red')

    ax.legend(ncol=2, loc='upper right', frameon=True)
    ax.set(ylabel='counts',
           xlabel='',
           title='Total comments')
    sns.despine(left=True, bottom=True)

    plt.show(f)
x, y, z = push_analyse(json_path)
show_distributions(x, y, z)
#     print()
# print(push_analyse(json_path))
