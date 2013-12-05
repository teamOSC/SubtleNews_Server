#!/usr/bin/env python


from goose import Goose
import lxml
#import Pillow
import cssselect
#import jieba
import BeautifulSoup
import nltk

from pyteaser import SummarizeUrl

import feedparser

import json

import time

def main():
    '''
    url = 'http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2'
    g = Goose()
    article = g.extract(url=url)
    print article.meta_description
    print article.top_image.src
    '''
    url = 'http://www.huffingtonpost.com/2013/11/22/twitter-forward-secrecy_n_4326599.html'
    summaries = SummarizeUrl(url)
    print summaries

def test():
    url = 'https://news.google.com/news/feeds?cf=all&ned=in&hl=en&output=rss&topic='

    arr=[]
    arr.append(time.strftime("%c"))
    url = 'https://news.google.com/news/feeds?cf=all&ned=in&hl=en&output=rss&topic='

    p=[['s','Sports'],['w','World'],['tc','Technology'],['b','Business'],['e','Entertainment'],['snc','Science'],['m','Health'] ]
    '''
    for i in p:
        url += i[0]     #converting ...&topic=  to ...&topic=s
        print  url
        rss = feedparser.parse(url)
        for j in rss['entries']:
            link = j['link']    #removing the google stuff from the url
            link = link[link.rfind('&url=')+5:]

            title = j['title']
            n = title   .rfind('-')
            source = title[n+1: ]
            title = title[:n]
            
            summary = SummarizeUrl(link)

            if summary != None and len(summary) > 0:
                print title+'-> ' + str(len(summary))
                arr.append({ 'title': title, 'link':link ,'summary':summary,'category': i[1],'date':j['published'],'source':source })           
            else:
                print 'BAD LINK '+ link
        url = url[:url.rfind('=')+1]     # converting ...&topic=tc to ...&topic=
    
    '''

    with open("../Desktop/Dropbox/Public/summary_test.txt", "w") as f:
        f.write(json.dumps(arr))

if __name__ == '__main__':
    test()
