import psycopg2
from configparser import ConfigParser
import time
import sys
#constants
CONFIG_FILE_PATH = 'c:\\python\\NLPredict\\datafeeder\\conn.config'
section_name = 'postgresql_conn_data'

class db_operations:
    def __init__(self):
        
        return
    def connect(self):
        self.get_connection_by_config()
        return self._conn.status == psycopg2.extensions.STATUS_READY

    def disconnect(self):
        self._conn.close()
 
    def get_connection_by_config(self):
        config_parser = ConfigParser()
        config_parser.read(CONFIG_FILE_PATH)
        if(config_parser.has_section(section_name)):
            config_params = config_parser.items(section_name)
            db_conn_dict = {}
            for config_param in config_params:
                key = config_param[0]
                value = config_param[1]
                db_conn_dict[key] = value
            conn = psycopg2.connect(**db_conn_dict)
        self._conn = conn
        
    def found_duplicate(self, rss_url, title):
        cursor = self._conn.cursor()
        postgres_select_query = """ SELECT count(*)
            FROM public.daily_logs
            where url = %s
            and title = %s;"""
        record_to_search = (rss_url, title)
        cursor.execute(postgres_select_query, record_to_search)
        res = cursor.fetchone()
        cursor.close()
        return res[0] > 0
        
    
    def insert(self, rss, title, link ):
        cursor = self._conn.cursor()
        
        postgres_insert_query ="""INSERT INTO public.daily_logs
        (rss_source, time_stamp, title, url, status, extra_note)
        VALUES (%s, %s, %s, %s, %s, %s);"""
        record_to_insert = (rss, time.asctime(), title, link, 'new', '')
        cursor.execute(postgres_insert_query, record_to_insert)
        self._conn.commit()
        cursor.close()   
        return 
        
    def get_content_urls(self):
        cursor = self._conn.cursor()
        postgres_select_query = """ SELECT log_id, url
            FROM public.daily_logs
            where status = 'new';"""
        cursor.execute(postgres_select_query)
        res = cursor.fetchall()
        cursor.close()
        return res

    def insert_content(self, log_id, content):
            #insert the real data from url.
        cursor = self._conn.cursor()
        postgres_insert_query = """ INSERT INTO public.content(log_id, content)
            VALUES(%s, %s);
            """
        record_to_insert = (log_id, content)
        cursor.execute(postgres_insert_query, record_to_insert)
        self._conn.commit()
        #upate the daily log table to set the flag
        cursor = self._conn.cursor()
        postgres_update_query = "UPDATE public.daily_logs SET status= 'retrieved'  WHERE log_id = {};"
        postgres_update_query = postgres_update_query.format(log_id)
        cursor.execute(postgres_update_query)
        self._conn.commit() 
        cursor.close()   
        return 

    def set_log_persisted(self, log_id):
        #upate the daily log table to set the flag as persisted
        cursor = self._conn.cursor()
        postgres_update_query = "UPDATE public.daily_logs SET status = 'persisted'  WHERE log_id = {};"
        postgres_update_query = postgres_update_query.format(log_id)
        cursor.execute(postgres_update_query)
        self._conn.commit() 
        cursor.close()   
        return 

    def read_content(self, log_id):
        #read content by log_id
        cursor = self._conn.cursor()
        postgres_select_query = str.format("""select content from public.content
            where log_id = {}
            limit(1);
            """, log_id)
        cursor.execute(postgres_select_query)
        self._conn.commit()
        res = cursor.fetchone()
        cursor.close
        return res[0]

    def last_price_update(self):
        cursor = self._conn.cursor()
        postgres_select_query = """ SELECT max(time_stamp) FROM public.price_logs;"""
        cursor.execute(postgres_select_query)
        self._conn.commit()
        res = cursor.fetchone()
        cursor.close
        return res[0]

    def insert_data_point(self, index_date, index_value):
        cursor = self._conn.cursor()
        postgres_insert_query = """ INSERT INTO public.price_logs(
	        currency_name, price, time_stamp)
	        VALUES ('BPI', %s, %s);
            """
        record_to_insert = (index_value, index_date)
        cursor.execute(postgres_insert_query, record_to_insert)
        self._conn.commit()
        cursor.close()

    # read logs and return tuple of (log id, time_stamp, title)
    def get_next_date(self):
        cursor = self._conn.cursor()
        postgres_select_query = """ SELECT log_id, time_stamp, title
	            FROM public.daily_logs
	            where status = 'retrieved';
                """
        cursor.execute(postgres_select_query)
        self._conn.commit()
        result = cursor.fetchall()
        cursor.close()
        return (result)

    def get_price(self, price_date):
        cursor = self._conn.cursor()
        query = 'SELECT  price FROM public.price_logs where time_stamp =\'{}-{}-{}\'; '
        postgres_select_query = str.format(query, price_date.year, price_date.month, price_date.day )
        cursor.execute(postgres_select_query)
        self._conn.commit()
        result = cursor.fetchone()
        cursor.close()
        if(result != None):
            return result[0]
        else:
            return -1



if __name__ == "__main__":
    url = 'https://www.newsbtc.com/feed/'
    title =  'Is The Crypto Market Bottom In? This News Headline Suggests It’s Near'
    db = db_operations()
    db.connect()
    res = db.found_duplicate(url, title)
    print (res)