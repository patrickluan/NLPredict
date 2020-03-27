import os
import numpy
import sys
from datetime import date, timedelta 
#import NLPredict.datafeeder.db_operations
sys.path.insert(0, 'c:\\python\\NLPredict')
from datafeeder import db_operations

DECREASE = 0
INCREASE = 1
def get_file_list():
    #loop in the director for file names:
    dir= 'datafeeder\\data'
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if(name =='feed.txt'):
                r.append(os.path.join(root, name))
    #the latest file might not have a price indicator yet
    r.sort()
    r.pop(-1)
    r.pop(-1)
    return r

def get_target_values(file_names):
    #use regexpress to extract the date
    #call database to get the target values
    dates = []
    for file_name in file_names:
        ele = file_name.split('\\')
        ymd = ele[2].split('_')
        dates.append(date(int(ymd[0]), int(ymd[1]), int(ymd[2])))
    return get_target(dates)

def get_target(dates):
    target_values = []
    db =  db_operations.db_operations() 
    if not db.connect():
        print('error opening database')
        pass
    for rss_date in dates:
        price_today = db.get_price(rss_date)
        price_tomorrow = db.get_price(rss_date + timedelta(days=1))
        if(price_tomorrow != -1 and price_today != -1):
            # 1: increase 0: decrease
            target_values.append((INCREASE,DECREASE)[price_today > price_tomorrow])
    return target_values

if __name__ == "__main__":
    get_target_values(get_file_list())