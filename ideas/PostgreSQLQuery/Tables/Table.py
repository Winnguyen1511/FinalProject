

class Table:
    def __init__(self, tableName, connectionDb, cursorDB):
        #Init Table:
        import psycopg2
        self.connectionDb = connectionDb
        self.cursorDB = cursorDB
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
    
    def selectAll(self):
        print('> SelectAll table ', self.tableName)
        SQLQuery = 'Select * from '+self.tableName
        self.cursorDB.execute(SQLQuery)
        #Fetch all records:
        records = self.cursorDB.fetchall()
        return records
    def truncate(self):
        print('> Truncate table ', self.tableName)
        SQLQuery = 'Truncate table '+self.tableName
        self.cursorDB.execute(SQLQuery)
        # print('> Truncated')
    def fetchall(self):
        return self.cursorDB.fetchall()

