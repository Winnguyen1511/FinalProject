
import psycopg2

def rfidValid(rfid):
    return True
def parkingLotIDValid(parkingLotID):
    return True

class Table:
    def __init__(self, tableName, connectionDb, cursorDB):
        #Init Table:
        
        self.connectionDb = connectionDb
        self.cursorDB = cursorDB
        if connectionDb is None:
            print('> Error: Invalid Connection')
            return None
        if cursorDB is None:
            print('> Error: Invalid cursor')
            return None
        try:
            cursorDB.execute('Select 1')
        except psycopg2.OperationalError:
            print('> Error: Connection closed table <%s>'%(tableName))
            return None
        SQLQuery = 'Select * from '+tableName
        try:
            cursorDB.execute(SQLQuery)
        except psycopg2.OperationalError:
            print('> Error: Table not exist <%s>'%(tableName))
            return None
        self.tableName = tableName

    def getName(self):
        print('> Table: ', self.tableName)
        
    def drop(self):
        print('> Drop table ', self.tableName)
        SQLQuery = 'DROP TABLE '+self.tableName
        self.cursorDB.execute(SQLQuery)
    
    def select(self, columns='*', conditions=''):
        records = []
        SQLQuery='Select '+columns+' from '+self.tableName+' '+conditions
        try:
            self.cursorDB.execute(SQLQuery)
            records = self.cursorDB.fetchall()
        except psycopg2.OperationalError:
            print('> Error select <%s>'%self.tableName)
        return records

    # def selectAll(self):
    #     print('> SelectAll table ', self.tableName)
    #     SQLQuery = 'Select * from '+self.tableName
    #     self.cursorDB.execute(SQLQuery)
    #     #Fetch all records:
    #     records = self.cursorDB.fetchall()
    #     return records
    
    def truncate(self):
        print('> Truncate table ', self.tableName)
        try:
            SQLQuery = 'Truncate table '+self.tableName
            self.cursorDB.execute(SQLQuery)
        except psycopg2.OperationalError:
            print('> Error: truncate failed')
        # print('> Truncated')
    def fetchall(self):
        records = []
        try:
            records = self.cursorDB.fetchall()
        except psycopg2.OperationalError:
            print('> Error fetchall')
        return records


class ParkingTable(Table):
    def __init__(self, connectionDb, cursorDB):
        self.tableName = 'parking'
        super().__init__(self.tableName, connectionDb, cursorDB)
    def insert(self, RFID, ParkingLotID, PlateNumber='', PlateImgURL='', CheckInTime=''):
        if not rfidValid(RFID):
            print('> Error: Invalid RFID <%s>', self.tableName)
            return False
        if not parkingLotIDValid(ParkingLotID):
            print('> Error: Invalid parkingLotID <%s>'%(self.tableName))
            return False
        if CheckInTime == '':
            print('> Warning: take default checkInTime <%s>'%(self.tableName))
            try:
                self.cursorDB.execute('insert into %s (rfid, parkinglotid, platenumber, plateimgurl)\
                                values (%s, %s, %s, %s)', (self.tableName,RFID, ParkingLotID, PlateNumber, PlateImgURL,))
            except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
                print('> Error: insert <%s>'%(self.tableName))
                self.cursorDB.execute('rollback')
                return False
        else:
            try:
                self.cur.execute('insert into %s (rfid, parkinglotid, platenumber, plateimgurl, checkintime)\
                                values (%s, %s, %s, %s, %s)', (self.tableName, RFID, ParkingLotID, PlateNumber, PlateImgURL, CheckInTime,))
            except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
                self.cursorDB.execute('rollback')
                print('> Error: insert <%s>'%(self.tableName))
                return False
        self.cursorDB.execute('commit')
        return True

listTableName = {
                'parking': ParkingTable,
                'history':None,
                'parkinglist': None,
                'stafflist': None,
                'cameralist': None
                }