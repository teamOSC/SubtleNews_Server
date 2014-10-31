#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from time import strftime

import re

def get_image(desc):
    temp = desc.split('src="')[-1]
    img = temp.split('"')[0]
    if not img.startswith("https://t"):
        img = "http://i.imgur.com/KU1vsAS.png"
    print img
    return img


def filter(str):
    return re.sub(r'[^a-zA-Z0-9\[\]\'\"\,\.\-\:\;\#\@\!\*\&\%\$]',' ', str)

def clean(title,url):
    tags = ['indianexpress','rape','Rape','Big Boss']
    for i in tags:
        if i in title or i in url:
            return False
    return True


def test():
    url = 'http://www.huffingtonpost.com/2013/11/22/twitter-forward-secrecy_n_4326599.html'
    summaries = SummarizeUrl(url)
    print summaries

def main():
    count = 0
    dict={}
    arr=[]
    
    url = 'https://news.google.com/news/feeds?cf=all&hl=en&output=rss'

    p=[ ['n','India','in'],['po','India','in'],['s','Sports','us'],['s','Sports','in'],['w','World','us'],['w','World','in'],['tc','Technology','us'],['tc','Technology','in'],['b','Business','us'],['b','Business','in'],['e','Entertainment','us'],['e','Entertainment','in'],['snc','Science','us'],['snc','Science','in'],['m','Health','us'],['m','Health','in'] ]
    
    for i in p:
        url += '&ned=%s&topic=%s'%(i[2],i[0]) #adding country code and topic in url
       
        print  "/***************\n%s [%s]\n***************/"%(i[1],i[2])
        rss = feedparser.parse(url)

        for j in rss['entries']:
            link = j['link']    #removing the google stuff from the url
            link = link[link.rfind('&url=')+5:]

            title = j['title']
            n = title.rfind('-')
            image = get_image(j['description'])
            source = title[n+1: ]
            title = title[:n]

            if not clean(title,url):
                print 'Filtered dirty news: %s'%(filter(title))
                continue            

            #summary = SummarizeUrl(link)
            try:
                s = ''  
                summary = SummarizeUrl(link)
                s += summary[0]
                for k in summary[1:]:
                    s += '\n\n' + k
            except Exception as e:
                print e  
                summary = []
                print 'Summary creation error for link: ' + link
                continue        

            if summary != None and len(summary) > 2 and len(s) < 1000 and len(s) > 200:
                
                count += 1
                '''
                s += summary[0]
                for k in summary[1:]:
                    s += '\n\n'+ k
                '''
                print image
                print "#%d %s :items %d : len %d"%(count ,filter(title), len(summary) , len(s) )
                title = u'\u00BB ' + title
                arr.append({ 'image':image,'title': title, 'link':link ,'summary':s,'category': i[1],'date':j['published'],'source':source })           
            else:
                print 'UNFIT summary : '+ link
        url =  url[:url.rfind('&ned')]     # removing country code and topic code from url
    
    
    arr.insert( 0 , "%d items last updated on %s"%(count , strftime("%Y-%m-%d %H:%M:%S") ) )

    with open("/home/sauravtom/public_html/summary.txt", "w") as f:
        dict['categories'] = ['India','World','Entertainment','Technology','Business','Science','Sports','Health']
        dict['summary'] = arr
        f.write(json.dumps(dict))

if __name__ == '__main__':
    main()
