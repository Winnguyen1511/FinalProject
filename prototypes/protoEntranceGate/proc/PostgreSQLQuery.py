import psycopg2
import argparse
from Tables.Table import *
from datetime import datetime as DT
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '5432'
DEFAULT_USERNAME = 'winnguyen'
DEFAULT_PASSWORD = 'khoanguyen1511dn..'
DEFAULT_DATABASE = 'parkinglotdatabase'

def login_database_Default():
    try:
        conn = psycopg2.connect(database=DEFAULT_DATABASE, user=DEFAULT_USERNAME,
                                password=DEFAULT_PASSWORD, host=DEFAULT_HOST, port=DEFAULT_PORT)
        cur = conn.cursor()
        cur.execute('Select version()')
        version = cur.fetchone()
        print('> PostgreSQL version: ',version)
    except Exception as e:
        print('> Error...')
        return e, None, None
    return True, conn, cur

def login_database(database, username, password, host, port):
    try: 
        conn = psycopg2.connect(database=database, user=username,
                                password=password, host=host, port=port)
        cur = conn.cursor()
        cur.execute('Select version()')
        version = cur.fetchone()
        print('> PostgreSQL version: ',version)
    except Exception as e:
        print('Error')
        return e, None, None
    return True, conn, cur

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', help='Enter database!')
    parser.add_argument('-U', '--username', help='Enter username!')
    parser.add_argument('-W', '--password', help='Enter password!')
    parser.add_argument('-p', '--port', help='Enter port!')
    parser.add_argument('-H', '--host', help='Enter hostname!')
    args = parser.parse_args()
    if args.database:
        database = args.database
    else:
        database = DEFAULT_DATABASE
    
    if args.username:
        username = args.username
    else:
        username = DEFAULT_USERNAME

    if args.password:
        password = args.password
    else:
        password = DEFAULT_PASSWORD
    
    if args.port:
        port = args.port
    else:
        port = DEFAULT_PORT
    
    if args.host:
        host = args.host
    else:
        host = DEFAULT_HOST

    ret, conn, cur = login_database(database, username, password, host, port)
    if ret:
        print('> Logged in successful to <%s>'%(username))
    else:
        print('> Error: Log in error to <%s>'%(username))
    
    # table = Table('parking', conn, cur)
    # table.getName()
    # records = table.selectAll()
    # # print(records)
    # for rec in records:
    #     print(rec)
    # records = table.fetchall()
    # print('1',records)
    # records = table.fetchall()
    # print('2',records)
    park = ParkingTable(conn,cur)
    # # records = park.select(columns='*', conditions="where rfid like '123%'")
    # records = park.select()
    # for rec in records:
    #     print(rec)
    park.insert('1211eq','PKL012')
    print('> After insert...')
    records = park.select()
    for rec in records:
        print(rec)
    park.insert('1111','PKL011','43A00967', '/home/khoa/Download', DT.now())
    print('> After insert...')
    records = park.select()
    for rec in records:
        print(rec)

    park.delete('12','123')
    print('> After delete...')
    records = park.select()
    for rec in records:
        print(rec)
    
    park.update('12','123',{'foo':123})
    print('> After update...')
    records = park.select()
    for rec in records:
        print(rec)
    # park.insert('1112','PKL011','92A0099', '/home/khoa/Download')
    # print('> After insert...')
    # records = park.select()
    # for rec in records:
    #     print(rec)
    # park.insert_manual(columns='rfid, parkinglotid',values='1234, PLK100')
    # print('> After insert...')
    # records = park.select()
    # for rec in records:
    #     print(rec)
    # park.delete('1112', 'PKL011')
    # print('> After delete...')
    # records = park.select()
    # for rec in records:
    #     print(rec)

    # park.update('12', '123', {'rfid':'abcsd', 'parkinglotid':'PKL001', 'platenumber':'43A00969'})
    # print('> After update...')
    # records = park.select()
    # for rec in records:
    #     print(rec)

    # park.update_manual(updates={'plateimgurl':'/home/khoa/tmp'}, where="rfid='abcsd'")
    # print('> After update...')
    # records = park.select()
    # for rec in records:
    #     print(rec)
    # his = HistoryTable(conn, cur)
    # his.insert('asdas12', 'PKL011', '43A00969', '/home/khoa/Download','STF001', 'CMR007', False,DT.now())
    # print('> After update...')
    # records = his.select()
    # for rec in records:
    #     print(rec)

    # his.insert_manual({'rfid': 'aaaaa', 'checktime':DT.now(), 'inorout':True})
    # print('> After update...')
    # records = his.select()
    # for rec in records:
    #     print(rec)
    # his.truncate()



# if __name__ == '__main__':
#     main()