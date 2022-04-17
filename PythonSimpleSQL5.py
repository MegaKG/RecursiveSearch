#!/usr/bin/env python3
try:
 import mysql.connector as mc
except Exception as E:
    print(E)
    mc = None

import datetime


"""
Data type 	Description
CHAR(size) 	A FIXED length string (can contain letters, numbers, and special characters). The size parameter specifies the column length in characters - can be from 0 to 255. Default is 1
VARCHAR(size) 	A VARIABLE length string (can contain letters, numbers, and special characters). The size parameter specifies the maximum column length in characters - can be from 0 to 65535
BINARY(size) 	Equal to CHAR(), but stores binary byte strings. The size parameter specifies the column length in bytes. Default is 1
VARBINARY(size) 	Equal to VARCHAR(), but stores binary byte strings. The size parameter specifies the maximum column length in bytes.
TINYBLOB 	For BLOBs (Binary Large OBjects). Max length: 255 bytes
TINYTEXT 	Holds a string with a maximum length of 255 characters
TEXT(size) 	Holds a string with a maximum length of 65,535 bytes
BLOB(size) 	For BLOBs (Binary Large OBjects). Holds up to 65,535 bytes of data
MEDIUMTEXT 	Holds a string with a maximum length of 16,777,215 characters
MEDIUMBLOB 	For BLOBs (Binary Large OBjects). Holds up to 16,777,215 bytes of data
LONGTEXT 	Holds a string with a maximum length of 4,294,967,295 characters
LONGBLOB 	For BLOBs (Binary Large OBjects). Holds up to 4,294,967,295 bytes of data
ENUM(val1, val2, val3, ...) 	A string object that can have only one value, chosen from a list of possible values. You can list up to 65535 values in an ENUM list. If a value is inserted that is not in the list, a blank value will be inserted. The values are sorted in the order you enter them
SET(val1, val2, val3, ...) 	A string object that can have 0 or more values, chosen from a list of possible values. You can list up to 64 values in a SET list

BIT(size) 	A bit-value type. The number of bits per value is specified in size. The size parameter can hold a value from 1 to 64. The default value for size is 1.
TINYINT(size) 	A very small integer. Signed range is from -128 to 127. Unsigned range is from 0 to 255. The size parameter specifies the maximum display width (which is 255)
BOOL 	Zero is considered as false, nonzero values are considered as true.
BOOLEAN 	Equal to BOOL
SMALLINT(size) 	A small integer. Signed range is from -32768 to 32767. Unsigned range is from 0 to 65535. The size parameter specifies the maximum display width (which is 255)
MEDIUMINT(size) 	A medium integer. Signed range is from -8388608 to 8388607. Unsigned range is from 0 to 16777215. The size parameter specifies the maximum display width (which is 255)
INT(size) 	A medium integer. Signed range is from -2147483648 to 2147483647. Unsigned range is from 0 to 4294967295. The size parameter specifies the maximum display width (which is 255)
INTEGER(size) 	Equal to INT(size)
BIGINT(size) 	A large integer. Signed range is from -9223372036854775808 to 9223372036854775807. Unsigned range is from 0 to 18446744073709551615. The size parameter specifies the maximum display width (which is 255)
FLOAT(size, d) 	A floating point number. The total number of digits is specified in size. The number of digits after the decimal point is specified in the d parameter. This syntax is deprecated in MySQL 8.0.17, and it will be removed in future MySQL versions
FLOAT(p) 	A floating point number. MySQL uses the p value to determine whether to use FLOAT or DOUBLE for the resulting data type. If p is from 0 to 24, the data type becomes FLOAT(). If p is from 25 to 53, the data type becomes DOUBLE()
DOUBLE(size, d) 	A normal-size floating point number. The total number of digits is specified in size. The number of digits after the decimal point is specified in the d parameter
DOUBLE PRECISION(size, d) 	 
DECIMAL(size, d) 	An exact fixed-point number. The total number of digits is specified in size. The number of digits after the decimal point is specified in the d parameter. The maximum number for size is 65. The maximum number for d is 30. The default value for size is 10. The default value for d is 0.
DEC(size, d) 	Equal to DECIMAL(size,d)

DATE 	A date. Format: YYYY-MM-DD. The supported range is from '1000-01-01' to '9999-12-31'
DATETIME(fsp) 	A date and time combination. Format: YYYY-MM-DD hh:mm:ss. The supported range is from '1000-01-01 00:00:00' to '9999-12-31 23:59:59'. Adding DEFAULT and ON UPDATE in the column definition to get automatic initialization and updating to the current date and time
TIMESTAMP(fsp) 	A timestamp. TIMESTAMP values are stored as the number of seconds since the Unix epoch ('1970-01-01 00:00:00' UTC). Format: YYYY-MM-DD hh:mm:ss. The supported range is from '1970-01-01 00:00:01' UTC to '2038-01-09 03:14:07' UTC. Automatic initialization and updating to the current date and time can be specified using DEFAULT CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP in the column definition
TIME(fsp) 	A time. Format: hh:mm:ss. The supported range is from '-838:59:59' to '838:59:59'
YEAR 	A year in four-digit format. Values allowed in four-digit format: 1901 to 2155, and 0000.
MySQL 8.0 does not support year in two-digit format.

"""


typeconv = {
    int: 'INT(255)',
    bool: 'BOOL',
    float: 'FLOAT(26)',
    str: 'VARCHAR(255)',
    bin: 'BINARY(64)',
    datetime.datetime: 'DATETIME(DEFAULT)'
    
    }

class mysqlcon:
    def __init__(self,host,user,passwd,db=None,dport=3306):
        if db != None:
            self.db = mc.connect(
                host = host,
                user = user,
                passwd = passwd,
                database = db,
                port = dport
            )
        else:
            self.db = mc.connect(
                host = host,
                user = user,
                passwd = passwd,
                port = dport
            )
        self.cursor = self.db.cursor()
            
    def showdbs(self):
        self.cursor.execute("SHOW DATABASES")
        DBS = self.cursor.fetchall()
        OUT = []
        for i in DBS:
            OUT.append(i[0])
        return OUT
    
    def showtables(self):
        self.cursor.execute("SHOW TABLES")
        TABLES = self.cursor.fetchall()
        OUT = []
        for i in TABLES:
            OUT.append(i[0])
        return OUT
    
    def selectdb(self,db):
        self.cursor.execute("USE " + db)
    
    def makedb(self,name):
        self.cursor.execute('CREATE DATABASE ' + name)
        self.db.commit()
    
    def maketable(self,name,Fields={'field1':'VARCHAR(255)'}):
        FIELDS = ''
        for i in list(Fields.keys()):

            FIELDS += i
            FIELDS += ' '
            FIELDS += Fields[i]
            FIELDS += ', '
        FIELDS = FIELDS[:-2]
        
        
        self.cursor.execute("CREATE TABLE " + name + " (id INT AUTO_INCREMENT PRIMARY KEY, " + FIELDS + ")")
        self.db.commit()

    def makepytable(self,name,Fields={'field1':str}):
        FIELDS = ''
        for i in list(Fields.keys()):

            FIELDS += i
            FIELDS += ' '
            FIELDS += typeconv[Fields[i]]
            FIELDS += ', '
        FIELDS = FIELDS[:-2]
        
        
        self.cursor.execute("CREATE TABLE " + name + " (id INT AUTO_INCREMENT PRIMARY KEY, " + FIELDS + ")")
        self.db.commit()
        
    def insert(self,table,FIELDS,VALUES):
        O = "INSERT INTO " + str(table) + " ("
        for i in FIELDS:
            O += str(i) + ','
        O = O[:-1]
        O += ') VALUES ('

        for i in VALUES:
            if type(i) == int:
                O += '%i,'
            elif type(i) == float:
                O += '%f,'
            else:
                O += '%s,'
        O = O[:-1]
        O += ')'
        #print(O)
        self.cursor.execute(O,VALUES)
        self.db.commit()
        
    def deltable(self,name):
        self.cursor.execute('DROP TABLE ' + name)
        self.db.commit()
        
    def deldb(self,name):
        self.cursor.execute('DROP DATABASE ' + name)
        self.db.commit()

    def readheaders(self,name):
        self.cursor.execute('DESCRIBE ' + name)
        HEAD = self.cursor.fetchall()
        OUT = {}
        for field in HEAD:
            OUT[field[0]] = field[1]
        return OUT

    def enable_full_text(self,name,Column):
        self.cursor.execute('Alter table ' + name + ' ADD FULLTEXT (' + Column + ');')
        self.db.commit()

    def readpyheaders(self,name):
        D = self.readheaders(name)
        #Invert Lookup
        INV = {}
        for key in list(typeconv.keys()):
            INV[ typeconv[key] ] = key

        for key in list(D.keys()):
            D[key] = INV[D[key]]

        return D
        
    def read(self,table,fields=[],amm=-1,criteria={}):
        sql = "SELECT "
        
        if fields == []:
            sql += '* '
        else:
            columns = ''
            for i in fields:
                columns += i
                columns += ','
            sql += columns[:-1] + ' '
            
        sql += 'FROM ' + table
        
        
        crits = []
        if criteria != {}:
            sql += ' WHERE '
            for i in list(criteria.keys()):
                if type(criteria[i]) == int:
                    sql += i + ' LIKE %i AND '
                elif type(criteria[i]) == float:
                    sql += i + ' LIKE %f AND '
                else:
                    sql += i + ' LIKE %s AND '
                
                crits.append(criteria[i])
            sql = sql[:-4]

        if amm == -1:
            pass
        else:
            sql += ' LIMIT ' + str(amm)
            
        #print(sql)
        #print(sql)
        
        self.cursor.execute(sql,crits)
        return self.cursor.fetchall()

    def readasdict(self,name,fields=[],amm=-1,criteria={},fts=False):
        if not fts:
            D = self.read(name,fields,amm,criteria)
        else:
            D = self.full_text_search(name,fields,amm,criteria)

        if fields != []:
            HEAD = fields
        else:
            HEAD = list(self.readheaders(name).keys())

        OUT = {}
        count = 0

        for i in HEAD:
            OUT[i] = []
            for a in D:
                OUT[i].append(a[count])
            count += 1
        return OUT

        
    def full_text_search(self,table,fields=[],amm=-1,criteria={'field1':'is'}):
        if fields == []:
            selv = '*'
        else:
            selv = ''
            for i in fields:
                selv += i + ','
            selv = selv[:-1]

        matchst = ''
        crits = []
        for key in criteria:
            matchst += 'match(' + key + ') against(%s) or '
            crits.append(criteria[key])
        matchst = matchst[:-4]

        if amm > 0:
            lim = 'limit ' + str(amm) + ';'
        else:
            lim = ';'

        if matchst == '':
            SQL = 'select ' + selv + ' from ' + table + ' ' + lim
        else:
            SQL = 'select ' + selv + ' from ' + table + ' where ' + matchst + lim
        self.cursor.execute(SQL,crits)
        DATA = self.cursor.fetchall()
        return DATA

    
    def delete(self,table,criteria={'field1':'is'}):
        sql = 'DELETE FROM ' + table + ' WHERE '
        crits = []
        for i in list(criteria.keys()):
            if type(criteria[i]) == int:
                sql += i + '=%i AND '
            elif type(criteria[i]) == float:
                sql += i + '=%f AND '
            else:
                sql += i + '=%s AND '
            crits.append(criteria[i])
        sql = sql[:-4]

        #print(sql)
        self.cursor.execute(sql,crits)
        self.db.commit()
        
    def raw(self,SQL):
        self.cursor.execute(SQL)
        #self.db.commit()
        return self.cursor.fetchall()

    def getrawfields(self,table):
        self.cursor.execute('SHOW COLUMNS FROM ' + table)
        return self.cursor.fetchall()

    def writefromdict(self,table,DICT={ 'field1':['a','b','c'], 'field2':['1','2','3'] }):
        FIELDS = list(DICT.keys())

        DATA = []
        for i in range(len(DICT[FIELDS[0]])):
            T = []
            for a in FIELDS:
                T.append(DICT[a][i])
            DATA.append(T)

        for i in range(len(DATA)):
            self.insert(table,FIELDS,DATA[i])



class simpletable:
    def __init__(self,HOST,U,P,DATABASE):
        M = mysqlcon(HOST,U,P)
        if DATABASE in M.showdbs():
            self.c = mysqlcon(HOST,U,P,DATABASE)
        else:
            M.makedb(DATABASE)
            self.c = mysqlcon(HOST,U,P,DATABASE)

    def read(self,TNAME):
        return self.c.readasdict(TNAME)

    def tables(self):
        return self.c.showtables()

    def columns(self,NAME):
        return self.c.readheaders(NAME)

    def write(self,DAT,NAME):
        if NAME not in self.c.showtables():
            HEADERS = list(DAT.keys())
            #Get Datatypes
            DTYPES = []
            for i in HEADERS:
                DTYPES.append( type(DAT[i][0]) )  

            FIELDS = {}
            count = 0
            for y in HEADERS:
                FIELDS[HEADERS[count]] = DTYPES[count]
                count += 1
            
            self.c.makepytable(NAME,FIELDS)
        self.c.writefromdict(NAME,DAT)

if __name__ == '__main__':
    if mc == None:
        print("Installing Libraries:")
        input('Press Enter to Continue')
        import os
        os.system('sudo apt install python3-pip mariadb-server')
        os.system('sudo pip3 install mysql-connector-python')
    else:
        print("Ready")
