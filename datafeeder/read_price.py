import json
import time
from datetime import date
import json
import db_operations
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects



def get_last_update():
	db = db_operations.db_operations()
	if not db.connect():
		return 'not connected'
	update_time = db.last_price_update()
	#last update date +1 is the start date for query. otherwise it will read twice
	return date(update_time.year, update_time.month, update_time.day+1)


def insert_data_point(index_date, index_value):
	db = db_operations.db_operations()
	if not db.connect():
		return 'not connected'
	db.insert_data_point(index_date, index_value)



def read_persist_price():
	start_date =  get_last_update()
	end_date = date.today()
	if(start_date >=  end_date):
		return
	url = 'https://api.coindesk.com/v1/bpi/historical/close.json?start={0}&end={1}'
	url= str.format(url, start_date, end_date)
	session = Session()
	try:
		response = session.get(url)
		data = json.loads(response.text)
		if data.get('bpi')!= None and len(data['bpi']) >0 :
			for item in data['bpi']:
				index_date = item
				index =  data['bpi'][index_date]
				insert_data_point(index_date, index)
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
		
if __name__ == "__main__":
	read_persist_price()