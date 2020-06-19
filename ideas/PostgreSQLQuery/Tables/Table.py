
import psycopg2

def rfidValid(rfid):
    return True
def parkingLotIDValid(parkingLotID):
    return True
def staffIDValid(staffID):
    return True

def cameraIDValid(cameraID):
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

    def execute(self,query=''):
        print(query)
        try:
            self.cursorDB.execute(query)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print('> Error execute <%s>'%(self.tableName))
            self.cursorDB.execute('rollback')
        self.cursorDB.execute('commit')

    def drop(self):
        print('> Drop table ', self.tableName)
        SQLQuery = 'DROP TABLE '+self.tableName
        try:
            self.cursorDB.execute(SQLQuery)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            self.cursorDB.execute('rollback')
            return False
            print('Error: drop')
        self.cursorDB.execute('commit')
        return True
    
    def select(self, columns='*', conditions=''):
        records = []
        SQLQuery='Select '+columns+' from '+self.tableName+' '+conditions
        try:
            self.cursorDB.execute(SQLQuery)
            records = self.cursorDB.fetchall()
        except psycopg2.OperationalError:
            print('> Error select <%s>'%self.tableName)
        return records

    def insert_manual(self, records={}):
        SQLQuery = 'insert into '+self.tableName+' ('
        valuesQuery = 'values('
        recordsTuple = []
        for key in records:
            SQLQuery += key+','
            valuesQuery+='%s,'
            recordsTuple.append(records[key])
        SQLQuery = SQLQuery.rstrip(',')
        valuesQuery = valuesQuery.rstrip(',')
        SQLQuery +=') '+valuesQuery+')'
        recordsTuple = tuple(recordsTuple)
        try: 
            self.cursorDB.execute(SQLQuery,recordsTuple)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            self.cursorDB.execute('rollback')
            print(Error)
            print('> Error: insert error <%s>'%(self.tableName))
            return False
        self.cursorDB.execute('commit')
        return True



    def delete_manual(self,where=''):
        SQLQuery = 'delete from '+self.tableName
        if where == '':
            print('> Error: delete_manual')
            return False
        try:
            self.cursorDB.execute(SQLQuery)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            self.cursorDB.execute('rollback')
            print(Error)
            print('> Error: delete <%s>'%(self.tableName))
            return False
        return True
    
    def update_manual(self, updates={}, where=''):
        SQLQuery = 'update '+self.tableName+ ' set '
        updatesTuple = []
        for key in updates:
            SQLQuery += key+'=%s,'
            updatesTuple.append(updates[key])
        SQLQuery = SQLQuery.rstrip(',')
        SQLQuery += ' where '+ where
        updatesTuple =tuple(updatesTuple)
        
        try:
            self.cursorDB.execute(SQLQuery, updatesTuple)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print(Error)
            print('Error: update_manual <%s>' %(self.tableName))
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True

    def truncate(self):
        print('> Truncate table ', self.tableName)
        try:
            SQLQuery = 'Truncate table '+self.tableName
            self.cursorDB.execute(SQLQuery)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print('> Error: truncate failed')
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True
        # print('> Truncated')
    def fetchall(self):
        records = []
        try:
            records = self.cursorDB.fetchall()
        except psycopg2.OperationalError:
            print('> Error fetchall')
        return records

###################################################################################
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
                SQLQuery = 'insert into '+self.tableName+ ' (rfid, parkinglotid, platenumber, plateimgurl)\
                                values (%s, %s, %s, %s)'
                self.cursorDB.execute(SQLQuery, (RFID, ParkingLotID, PlateNumber, PlateImgURL,))
            except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
                print('> Error: insert <%s>'%(self.tableName))
                self.cursorDB.execute('rollback')
                return False
        else:
            try:
                SQLQuery = 'insert into '+self.tableName+ ' (rfid, parkinglotid, platenumber, plateimgurl, checkintime)\
                                values (%s, %s, %s, %s, %s)'
                self.cursorDB.execute(SQLQuery, (RFID, ParkingLotID, PlateNumber, PlateImgURL, CheckInTime,))
            except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
                self.cursorDB.execute('rollback')
                print('> Error: insert <%s>'%(self.tableName))
                return False
        self.cursorDB.execute('commit')
        return True


    def delete(self, RFID, ParkingLotID):
        if not rfidValid(RFID):
            print('> Error: Invalid RFID <%s>', self.tableName)
            return False
        if not parkingLotIDValid(ParkingLotID):
            print('> Error: Invalid parkingLotID <%s>'%(self.tableName))
            return False
        SQLQuery = 'delete from '+self.tableName+' where rfid=%s and parkinglotid=%s'
        try:
            self.cursorDB.execute(SQLQuery, (RFID, ParkingLotID))
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            self.cursorDB.execute('rollback')
            print(Error)
            print('Error: delete <%s>'%(self.tableName))
            return False
        self.cursorDB.execute('commit')
        return True
    
    def update(self,RFID, ParkingLotID, updates= {}):
        if not rfidValid(RFID):
            print('> Error: Invalid RFID <%s>', self.tableName)
            return False
        if not parkingLotIDValid(ParkingLotID):
            print('> Error: Invalid parkingLotID <%s>'%(self.tableName))
            return False
        SQLQuery = 'update '+self.tableName +' set '
        updatesTuple = []
        for key in updates:
            SQLQuery += key+'=%s,'
            updatesTuple.append(updates[key])
        SQLQuery = SQLQuery.rstrip(',')
        SQLQuery += ' where rfid=%s and parkinglotid=%s'
        updatesTuple.extend([RFID, ParkingLotID])
        updatesTuple = tuple(updatesTuple)


        try:
            self.cursorDB.execute(SQLQuery, updatesTuple)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print(Error)
            print('> Error update <%s>'%(self.tableName))
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True
############################################################################
class HistoryTable(Table):
    def __init__(self, connectionDb, cursorDB):
        self.tableName = 'history'
        super().__init__(self.tableName, connectionDb, cursorDB)
    
    def insert(self,RFID='', ParkingLotID='', PlateNumber='', PlateImgURL='',StaffID='',\
                CameraID='', InOrOut=True, CheckTime=''):
        if not rfidValid(RFID):
            print('> Error: Invalid RFID <%s>', self.tableName)
            return False
        if not parkingLotIDValid(ParkingLotID):
            print('> Error: Invalid parkingLotID <%s>'%(self.tableName))
            return False
        if not cameraIDValid(CameraID):
            print('> Error: Invalid cameraID <%s>'%(self.tableName))
            return False
        if not staffIDValid(staffIDValid):
            print('> Error: Invalid staffID <%s>'%(self.tableName))
            return False
        try:
            SQLQuery = 'insert into '+self.tableName+ ' (rfid, parkinglotid, platenumber, plateimgurl,\
                        staffid, cameraid, inorout, checktime) \
                        values(%s, %s, %s, %s, %s, %s, %s, %s)'
            insertTuple = (RFID, ParkingLotID, PlateNumber, PlateImgURL,StaffID,CameraID,InOrOut,CheckTime,)
            self.cursorDB.execute(SQLQuery, insertTuple)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print(Error)
            print('> Error: insert error <%s>'%(self.tableName))
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True

    def update(self, parkingID, updates={}):
        SQLQuery = 'update '+self.tableName +' set '
        updatesTuple = []
        for key in updates:
            SQLQuery += key+'=%s,'
            updatesTuple.append(updates[key])
        SQLQuery = SQLQuery.rstrip(',')
        SQLQuery += ' where parkingid=%s'
        updatesTuple.extend([parkingID])
        updatesTuple = tuple(updatesTuple)
        try:
            self.cursorDB.execute(SQLQuery, updatesTuple)
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print(Error)
            print('Error: update error <%s>'%(self.tableName))
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True


    def delete(self, parkingID):
        SQLQuery = 'delete from '+self.tableName+' where parkingID=%s'
        try:
            self.cursorDB.execute(SQLQuery, (parkingID,))
        except (psycopg2.OperationalError, psycopg2.IntegrityError,
                    psycopg2.DatabaseError, psycopg2.DataError) as Error:
            print(Error)
            print('> Error: delete error <%s>'%(self.tableName))
            self.cursorDB.execute('rollback')
            return False
        self.cursorDB.execute('commit')
        return True





############################################################################
listTableName = {
                'parking': ParkingTable,
                'history':None,
                'parkinglist': None,
                'stafflist': None,
                'cameralist': None
                }