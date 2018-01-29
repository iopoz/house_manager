import os
import re
import sqlite3 as db_driver
import time
from datetime import datetime, timedelta
import datetime as dt_class


def connect():
    db_path = os.path.join(os.path.abspath(''), "db.sqlite3")
    db = db_driver.connect(db_path)
    return db

def terminate(db):
    try:
        if db:
            db.close()
    except db_driver.Error as e:
        print('Error %s:' % e.args[0])

def add_rent(values):
    db = connect()
    cur = db.cursor()
    cur.execute('Insert into HouseManage_moneyreport '
                '(name_service, plan_date, type_service_id, user_id, current_date, money) '
                'VALUES (?, ?, ?, ?, ?, ?)', (values[0], values[1], values[2], values[3], values[4], values[5]))
    db.commit()
    terminate(db)

start_date  = '2016-11-28'
st_pos = 11
end_date = '2017-09-28'
mm = 10
rent = 550
flat = 40
while True:
    if start_date != end_date:
        if st_pos <= 12:
            year = '2016'
            mm += 1
        else:
            year = '2017'
            mm = st_pos - 12
        if len(str(mm)) == 1:
            mm = '0' + str(mm)
        date_add = '-'.join([year, str(mm), '28'])
        dm = '.'.join([str(mm), year[2:]])
        values = ('Квартплата %s' %dm, date_add, 1, flat, date_add, rent)
        add_rent(values)
        st_pos += 1
        start_date = date_add
    else:
        break