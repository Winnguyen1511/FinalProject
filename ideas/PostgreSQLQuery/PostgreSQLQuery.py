import psycopg2
import argparse
from Tables.Table import *

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '5432'
DEFAULT_USERNAME = 'winnguyen'
DEFAULT_PASSWORD = 'khoanguyen1511dn..'
DEFAULT_DATABASE = 'parkinglotdatabase'
def login(database, username, password, host, port):
    conn = psycopg2.connect(database=database, user=username,
                            password=password, host=host, port=port)
    cur = conn.cursor()
    cur.execute('Select version()')
    version = cur.fetchone()
    print('> PostgreSQL version: ',version)
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

    ret, conn, cur = login(database, username, password, host, port)
    if ret:
        print('> Logged in successful to <%s>'%(username))
    else:
        print('> Error: Log in error to <%s>'%(username))
    
    table = Table('parking', conn, cur)
    table.getName()
    records = table.selectAll()
    # print(records)
    for rec in records:
        print(rec)
    # records = table.fetchall()
    # print('1',records)
    # records = table.fetchall()
    # print('2',records)

if __name__ == '__main__':
    main()