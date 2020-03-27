#!/usr/bin/python
from configparser import ConfigParser
import sys

import feedparser
import db_operations
import read_content
import read_price
import persist

section_name = 'rss links'
#prepare database
db = db_operations.db_operations()
if not db.connect():
    print('error opening database')
    exit(2)
print('rss read and database connected')
#read rss links from config file
config_parser = ConfigParser()
config_parser.read(db_operations.CONFIG_FILE_PATH)
if(config_parser.has_section(section_name)):
    links = config_parser.items(section_name)

for rss_link in links[0][1].split(','):
    feed = feedparser.parse(rss_link)
    if len(feed.entries) ==0:
        continue
    for post in feed.entries:
        title = post.title
        link = post.link
        if(not db.found_duplicate(link, title)):
            db.insert(rss_link, title, link)
            print(title)

read_content.read_content()                
persist.persist()
read_price.read_persist_price()
print('done!')

