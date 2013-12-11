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

def filter(str):
    return re.sub(r'[^a-zA-Z0-9\[\]\'\"\,\.\-\:\;\#\@\!\*\&\%\$]',' ', str)

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
            source = title[n+1: ]
            title = title[:n]
            
            try:  summary = SummarizeUrl(link)
            except:  
                summary = []
                print 'BAD LINK' + link        

            if summary != None and len(summary) > 2:
                s=''
                count += 1
                #s += '◦ ' + summary[0]
                for k in summary[1:]:
                    s += '\n\n'+ k

                print "#%d :%d items  in summary"%(count , len(summary) )
                #title = u'\u00BB ' + title
                arr.append({ 'title': title, 'link':link ,'summary':s,'category': i[1],'date':j['published'],'source':source })           
            else:
                print 'BAD LINK '+ link
        url =  url[:url.rfind('&ned')]     # removing country code and topic code from url
    
    
    arr.insert( 0 , "%d items last updated on %s"%(count , strftime("%Y-%m-%d %H:%M:%S") ) )

    with open("../public_html/summary.txt", "w") as f:
        dict['categories'] = ['India','World','Entertainment','Technology','Business','Science','Sports','Health']
        dict['summary'] = arr
        f.write(json.dumps(dict))

if __name__ == '__main__':
    main()
