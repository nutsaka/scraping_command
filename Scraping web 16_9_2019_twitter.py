import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import pandas as pd
import numpy as np

stopwords = set(STOPWORDS)


def show_wordcloud(data, title=None):
    wordcloud = WordCloud(
        font_path="B:\Pythone\THSarabunNew.ttf",
        relative_scaling=1.0,
        min_font_size=12,
        background_color="white",
        width=1024,
        height=768,
        scale=3,
        font_step=1,
        collocations=False,
        regexp=r"[\u0E00-\u0E7Fa-zA-Z']+",
        margin=2).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.title(title)
    plt.show()


option = webdriver.ChromeOptions()
option.add_argument("— incognito")

browser = webdriver.Chrome(executable_path='C:\chromedriver', chrome_options=option)
browser.get(
    'https://twitter.com/search?q=%23%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%A2%E0%B8%B8%E0%B8%97%E0%B8%98%E0%B9%8C&src=trend_click')

time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 25

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

twitter_elm = browser.find_elements_by_class_name("tweet")

data = list()
texts = list()

for post in twitter_elm:
    username = post.find_element_by_class_name("fullname")
    tweet = post.find_element_by_class_name("js-tweet-text")
    texts.append(tweet.text)
    print(username.text, tweet.text)

    data.append([username.text, tweet.text])

show_wordcloud(texts, '')

# df = pd.DataFrame(data, columns = ['username', 'tweet'])
# df.to_csv('./data/bomb-tweet-8-2-2019.csv', index=False)

# print(df.sample(10))
# pretty_csv.pretty_file("./data/bomb-tweet-8-2-2019.csv", header=False, border=False, delimiter=",")
browser.quit()