import pymongo
import time
from pymongo import MongoClient
from myLogger import LOG
import config

class MongoConnection:

    def __init__(self,):
        self.conn = None
        self.host = config.host
        self.usr_name = config.userName
        self.pwd = config.password

    def getmongoconnection(self):
        try:
            self.conn = MongoClient(self.host)
            LOG.info("connected to the server successfully")
            self.conn.databasename.authenticate(self.usr_name, self.pwd) #give the databaseName
        except (pymongo.errors.PyMongoError)as e:
            LOG.error(" Could not connect to server:{0} ".format(e))
            return None
        return self.conn

    def checkmongoconnection(self,):
        if self.getmongoconnection():
            pass
        else:
            while 1:
                time.sleep(10)
                if self.getmongoconnection():
                    break


    def uploaddata(self, col_name, listobjs):
        try:
            self.checkmongoconnection()
            db = self.conn.databasename             #give the databasename
            col = db[col_name]
            LOG.info("collection name is :%s" % col)
            self.sortedlist = sorted(listobjs, key=lambda obj: (obj["key"])) # any key name which is exists in the all documets to sorting
            while(self.sortedlist):
                try:
                    evalid=col.insert_one(self.sortedlist[0]).inserted_id
                    del  self.sortedlist[0]
                except Exception as  e:
                    LOG.error("ERROR OCCUERRED IN INSERTION :%s"%e)
                    del self.sortedlist[0]
            self.conn.close()
            LOG.info("*****************ALL DOCUMENTS ARE UPLOADED INTO MONGODB**************************")
        except Exception as e:
           LOG.info("EXCEPTION occurred while inserting the documents:%s " % e)
