from PyQt4.QtSql import *

class product(QSqlTableModel):
    name=''
    goodproduct=0
    badproduct=0
    outqty=0
    inqty=0
    def __init__(self):
        pass
    def get_name(self):
        return self.name
    def getgoodproduct(self):
        return self.getgoodproduct()
    def getbadproduct(self):
        return self.badproduct
    def getoutqty(self):
        return self.outqty
    def getinqty(self):
        return self.inqty




