#!/usr/bin/python
import csv, sys, re, pg



class DBconnect:
  

  def __init__(self, dbname, host, port, user, passwd):
      self.dbname = dbname
      self.host = host
      self.port = port
      self.user = user
      self.passwd = passwd

  def connect(self):
      db = pg.connect(dbname = self.dbname, host= self.host, port = self.port, user= self.user, passwd = self.passwd)
      #print "success!"
      return db
class Csv2pgsql:

    def __init__(self, csvfile):
        self.csvfile = csvfile
        ifile =open(csvfile, 'rb')
        self.reader = csv.reader(ifile, delimiter='|')
        
    def column_info(self, rows=[]):
        self.rows = rows
        for row in self.reader:
             rows.append(row)
             self.columnnames = self.rows[0]
             self.numcols = len(self.columnnames)   
             self.numrows = len(self.rows)         
        for a in rows:
              if len(a) <> self.numcols:
                  print "Row ", a, "Has a wrong number of columns ", len(a)
                  sys.exit("There are mismatched rows")
        self.columnlist = []
        for y in range(self.numcols):
            self.checklist = []

            for x in range(self.numrows):
                self.cell = rows[x][y]
                self.checklist.append(self.cell)
            self.columnlist.append(self.checklist)

        self.columntype = []
      
       
        for y in range(self.numcols):
        #for y in range(100):
                self.columnname = self.columnlist[y][0]
                self.templist = [self.columnname]
               
                for s in self.columnlist[y][1:]:
                     
                     try: 
                        float(s)        
                        self.templist.append('float') 
                       # print s, "is a float"
                     except:
                     #   print s, "is not a float"
                        
                        pass
                        
		     try: 
		        int(s) 
		        self.templist.append('integer')
                       #  print s,"is a int"
		     except: 	
                      #  print s,"is not a int"
		        pass
		     try: 
		         str(s) 
		         self.templist.append('string')
                      #   print s,"is a string"	
		     except:
                      #   print s, "is not a string"
		         pass
		   
		self.stringcount =  self.templist.count('string')
		self.integercount =  self.templist.count('integer')
		self.floatcount =   self.templist.count('float')      
		datatype = ' '
                   
                #print self.stringcount, self.integercount, self.floatcount
		
		if self.stringcount > self.integercount and self.floatcount > self.integercount:
	          # print "The datatype is FLOAT"
		   datatype = 'double precision'
		elif self.stringcount > self.floatcount and self.stringcount > self.integercount:   
	           # print "the datatype is STRING"
		    datatype = 'character varying'
		elif self.integercount == self.stringcount and self.integercount == self.floatcount:
	         #  print 'the datatype is INTEGER'
		   datatype = 'integer'
		else:
		   print "the datatype is unknown"
	    
		self.coltype = [self.columnlist[y][0], datatype]  
        
        	self.columntype.append(self.coltype) 
        columndict = {}

        for k in self.columntype:
            columndict[k[0]] = k[1]   
        print columndict  

        fields = ' '
        for i in self.columntype: 
	    a = i[0]
	    a = a.lower()
	    a = a.replace(" ","_")
	    a = a.replace("'","") 
    
            fields = fields+'"'+a+'"'+' '+columndict[i[0]]+', '
        fields = fields[:-2]

 
	createtablesql = "CREATE TABLE test ("+fields+" )"

	'''Insert SQL'''
	insertsql = ' '
	insertpre = 'INSERT INTO test VALUES('
	insertdata = ' '

	for n in rows[1:]:
	   
	    insertdata = ' '
	    for o in n:
      
	       if len(o) == 0:
		   o = '\' \''
		   #o.replace('"', '') 
		    
	       insertdata = insertdata+' '+o+', '
	      
	    insertdata = insertpre+insertdata[:-2]+'); '
	    insertsql = insertsql+insertdata
	    
	insertsql = insertsql[:-2]
        droptable = "DROP TABLE test"
       # conn.query(droptable)
        conn.query(createtablesql)
        conn.query(insertsql)
        

  
if __name__ == '__main__':
    
    dbname = 'postgis_scratch'
    host =  'postgresql'
    port =   5432 
    user = 'gisteam' 
    passwd = 'gisDB1'      
    conn = DBconnect(dbname, host, port,user,passwd).connect()
    csvfile = '/home/mtafel/Dropbox/data/todprojects.csv'
   
    getcsvinfo = Csv2pgsql(csvfile).column_info()
    #print getcsvinfo
   

