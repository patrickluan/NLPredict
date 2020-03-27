import os
import numpy
import sys
from datetime import date, timedelta 
#import NLPredict.datafeeder.db_operations
sys.path.insert(0, 'c:\\python\\NLPredict')
from datafeeder import db_operations

def get_file_list():
    #loop in the director for file names:
    dir= 'datafeeder\\data'
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if(name =='feed.txt'):
                r.append(os.path.join(root, name))
    return r

def get_target_values(file_names):
    #use regexpress to extract the date
    #call database to get the target values
    dates = []
    for file_name in file_names:
        ele = file_name.split('\\')
        ymd = ele[2].split('_')
        dates.append(date(int(ymd[0]), int(ymd[1]), int(ymd[2])))
    return dates

def get_target(dates):
    target_values = []
    db =  db_operations.db_operations() 
    if not db.connect():
        print('error opening database')
        pass
    for rss_date in dates:
        price_today = db.get_price(rss_date)[0]
        price_tomorrow = db.get_price(rss_date + timedelta(days=1))[0]
        price_diff =  price_tomorrow - price_today
        target_values.append((0,1)[price_today<price_tomorrow])
    return target_values

if __name__ == "__main__":
    get_target(get_target_values(get_file_list()))