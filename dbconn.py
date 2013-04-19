import sqlite3
# -*- coding: utf-8 -*-
def conCreate():
    db=sqlite3.connect('kcgl.db')
    print 'db connect!'
    #db.execute('''insert into productrecord values('2','激光打印机','2013-04-06',20,10,30,'',4)''')
    quer=db.execute('select * from productrecord')

    db.close()
    return quer

def getprono():
    db=sqlite3.connect('kcgl.db')
    #print 'db connect!'
    #db.execute('''insert into productrecord values('2','激光打印机','2013-04-06',20,10,30,'',4)''')
    quer=db.execute('select * from productlist')
    prolist=quer.fetchall()
    pplist=[]
    for i in prolist:
        pplist.append(i[0])
    db.close()
    return pplist

def getpronamebyno(prono):
    db=sqlite3.connect('kcgl.db')
    #print 'db connect!'
    #db.execute('''insert into productrecord values('2','激光打印机','2013-04-06',20,10,30,'',4)''')
    quer=db.execute("select * from productlist where prodcutno= '%s'"%prono)
    prolist=quer.fetchall()
    #print prolist[0][1]
    db.close()
    #print prolist
    try:
        return prolist[0][1]
    except:
        return

def insertdata(sqlstr):
    ss=tuple(sqlstr)
    sql=("insert into record(prodctuno,time,prodtype,qty,mark,recordman,place) values('%s','%s','%s',%d,'%s','%s','%s')" % ss)
    db=sqlite3.connect('kcgl.db')
    quer=db.execute(sql)
    db.commit()
    #print 'commit!'
def outdata(sqlstr):
    ss=tuple(sqlstr)
    sql=("insert into outrecord(prodctuno,time,prodtype,qty,mark,recordman,lingyongman,place) \
        values('%s','%s','%s',%d,'%s','%s','%s','%s')" % ss)
    db=sqlite3.connect('kcgl.db')
    quer=db.execute(sql)
    db.commit()
    #print 'commit!'

def insertdataproduct(sqlstr):
    ss=tuple(sqlstr)
    sql=("insert into productlist(prodcutno,productname) values('%s','%s')" % ss)
    db=sqlite3.connect('kcgl.db')
    try :
        #print sql
        quer=db.execute(sql)
        db.commit()
        #print 'commit!'
        return 1
    except:
        return 0
    finally:
        db.close()
def updatedataproduct(sqlstr):
    ss=tuple(sqlstr)
    sql=("update productlist set prodcutno='%s',productname='%s' where prodcutno='%s'" % ss)
    db=sqlite3.connect('kcgl.db')
    try :
        #print sql
        quer=db.execute(sql)
        db.commit()
        #print 'commit!'
        return 1
    except:
        return 0
    finally:
        db.close()
def deldataproduct(sqlstr):
    ss=tuple(sqlstr)
    sql=''
    sql=("delete from productlist where prodcutno='%s'" % ss)
    db=sqlite3.connect('kcgl.db')
    try :
        #print sql
        quer=db.execute(sql)
        db.commit()
        #print 'commit!'
        return 1
    except:
        return 0
    finally:
        db.close()
def quer(productno,prodtype):
    sql="select * from record where prodctuno='%s' and prodtype=%d" %(productno,prodtype)
    db=sqlite3.connect('kcgl.db')
    #try:
    print sql
    q=db.execute(sql)
    return q.fetchall()
    #except:
        #print Exception


if __name__=='__main__':
    print "hello"
    print getpronamebyno('bmdyj')

