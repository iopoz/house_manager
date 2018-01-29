import os
import sqlite3 as db_driver
import datetime


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


def input_data():
    start_date = '2017-10-28'
    st_pos = 10
    end_date = '2018-01-28'
    mm = 9
    rent = 4000
    flat = 8
    while True:
        if start_date != end_date:
            if st_pos <= 12:
                year = '2017'
                mm += 1
            else:
                year = '2018'
                mm = st_pos - 12
            if len(str(mm)) == 1:
                mm = '0' + str(mm)
            date_add = '-'.join([year, str(mm), '28'])
            dm = '.'.join([str(mm), year[2:]])
            values = ('Уборка %s' %dm, date_add, 2, flat, date_add, rent)
            add_rent(values)
            st_pos += 1
            start_date = date_add
        else:
            break

def fix_date_in_data():
    db = connect()
    cur = db.cursor()
    data_rows = cur.execute('SELECT id, plan_date, HouseManage_moneyreport.current_date, name_service from HouseManage_moneyreport')
    rows = data_rows.fetchall()
    for row in rows:
        date_plane_value = row[1]
        date_cur_value = row[2]
        if type(date_plane_value) == int:
            date_plane_value = datetime.datetime.fromtimestamp(date_plane_value / 1000).strftime('%Y-%m-%d')
        if type(date_cur_value) == int:
            date_cur_value = datetime.datetime.fromtimestamp(date_cur_value / 1000).strftime('%Y-%m-%d')
        cur.execute('UPDATE HouseManage_moneyreport SET plan_date = ?, current_date = ? WHERE id =?',
                    (date_plane_value, date_cur_value, row[0]))
    db.commit()
    terminate(db)

fix_date_in_data()