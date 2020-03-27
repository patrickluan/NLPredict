import os
import errno
import db_operations


root_folder ='datafeeder\data'
textfile = 'feed.txt'
pricefile = 'price.txt'


#content includes log title, it might significant    
def write_to_file(file_name, log_title, log_id):
    if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    with open(file_name, 'a+') as f:
        f.writelines(log_title)
        db = db_operations.db_operations()
        if not db.connect():
            print('error opening database')
            exit(2)
            # get an array of logs to persist
        content =  db.read_content(log_id)
        f.write(content)

def persist():
    db = db_operations.db_operations() 
    if not db.connect():
        print('error opening database')
        exit(2)
        # get an array of logs to persist
    r = db.get_next_date()
    
    for log in r:
        log_id = log[0]
        log_date = str.format('{}_{:02d}_{:02d}', log[1].year,  log[1].month, log[1].day)
        log_title = log[2]
        folder = root_folder +'\\' + log_date +'\\'
        file_name = folder + textfile
        write_to_file(file_name, log_title, log_id)
        db.set_log_persisted(log_id)
    print (str.format('saved to file: {}', len(r)))


if __name__ == "__main__":
    persist()