# -*- coding: utf-8 -*-

import sys
from maindiag import *
from PyQt4 import QtGui,QtCore,QtSql
from PyQt4.QtGui import QMessageBox
import dbconn

def createConnection():
    db=QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('kcgl.db')
    db.open()
    print "db ok!"
    print (db.lastError().text())
    return True

class myApp(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.model=QtSql.QSqlTableModel(self)
        self.model.setTable('productlist')
        self.model.setHeaderData(0,QtCore.Qt.Horizontal,u"编号")
        self.model.setHeaderData(1,QtCore.Qt.Horizontal,u"名称")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.ui.tableView.setModel(self.model)

        model1=QtSql.QSqlQueryModel(self)
        sql=u'''
           select prodctuno as 编号,time as 时间,prodtype as 良否,qty as 数量,\
           place as 库位,recordman as 记录人, mark as 备注 from record
        '''
        model1.setQuery(sql)
        self.ui.tableView_2.setModel(model1)

        model=QtSql.QSqlQueryModel()
        sql=u'''
            select prodctuno as 编号,time as 时间,prodtype as 良否,qty as 数量,\
            lingyongman as 领用人,
            place as 库位,recordman as 记录人, mark as 备注 from outrecord
            '''
        model.setQuery(sql)
        self.ui.tableView_5.setModel(model)

        self.ui.radioButton.setChecked(True)
        self.ui.radioButton_4.setChecked(True)
        self.ui.radioButton_5.setChecked(True)

        self.inall()
        self.outall()
        self.curall()

        plist=dbconn.getprono()
        self.ui.prono.addItems(plist)
        self.ui.comboBox.addItems(plist)
        self.ui.comboBox_2.addItems(plist)
        pname=dbconn.getpronamebyno(self.ui.prono.currentText())
        self.ui.lineEdit.setText(pname)
        self.ui.lineEdit_3.setText(pname)
        self.ui.lineEdit_11.setText(pname)

        self.connect(self.ui.prono,QtCore.SIGNAL('currentIndexChanged(QString)'),self.updatelineedit)
        self.connect(self.ui.comboBox,QtCore.SIGNAL('currentIndexChanged(QString)'),self.updateoutlineedit)
        self.connect(self.ui.comboBox_2,QtCore.SIGNAL('currentIndexChanged(QString)'),self.querlineedit)
        self.connect(self.ui.pushButton,QtCore.SIGNAL('clicked()'),self.insertdata)
        self.connect(self.ui.pushButton_3,QtCore.SIGNAL('clicked()'),self.outdata)
        self.connect(self.ui.lineEdit_2,QtCore.SIGNAL('textChanged(QString)'),self.checkint)
        self.connect(self.ui.lineEdit_6,QtCore.SIGNAL('textChanged(QString)'),self.checkint)
        #self.connect(self.ui.addButton,QtCore.SIGNAL("click()"),self.addinfo)
        #self.connect(self.ui.cancelButton,QtCore.SIGNAL("click()"),QtCore.SLOT('close()'))
        self.connect(self.ui.pushButton_2,QtCore.SIGNAL('clicked()'),self.cancledate)
        self.connect(self.ui.pushButton_5,QtCore.SIGNAL('clicked()'),self.addproduct)
        self.connect(self.ui.pushButton_6,QtCore.SIGNAL('clicked()'),self.updateproduct)
        self.connect(self.ui.pushButton_7,QtCore.SIGNAL('clicked()'),self.delproduct)
        self.connect(self.ui.pushButton_8,QtCore.SIGNAL('clicked()'),self.querproduct)
        self.connect(self.ui.tableView,QtCore.SIGNAL('clicked(QModelIndex)'),self.selproductno)
        self.connect(self.ui.tabWidget,QtCore.SIGNAL('currentChanged(int)'),self.tabchange)
        self.connect(self.ui.pushButton_9,QtCore.SIGNAL('clicked()'),self.inall)
        self.connect(self.ui.pushButton_10,QtCore.SIGNAL('clicked()'),self.outall)
        self.connect(self.ui.pushButton_11,QtCore.SIGNAL('clicked()'),self.curall)
    def inall(self):
        self.model=QtSql.QSqlQueryModel(self)
        sql=u'''
        select record.prodctuno as 编号,productlist.productname as 物品名称,\
        sum(record.qty) as 总数
        from record,productlist
        where record.prodctuno=productlist.prodcutno
        group by
        record.prodctuno
        '''
        self.model.setQuery(sql)
        self.ui.tableView_6.setModel(self.model)
    def outall(self):
        self.model=QtSql.QSqlQueryModel(self)
        sql=u'''
        select outrecord.prodctuno as 编号,productlist.productname as 物品名称,\
        -sum(outrecord.qty) as 总数
        from outrecord,productlist
        where outrecord.prodctuno=productlist.prodcutno
        group by
        outrecord.prodctuno
        '''
        self.model.setQuery(sql)
        self.ui.tableView_7.setModel(self.model)
    def curall(self):
        model=QtSql.QSqlQueryModel(self)
        sql=u'''
            select total_all.prodctuno as 编号,productlist.productname as 名称,\
            total_all.total as 总数,total_all.ok as 良品,total_all.bad as 不良 from total_all,productlist
            where total_all.prodctuno=productlist.prodcutno;
        '''
        model.setQuery(sql)

        self.ui.tableView_8.setModel(model)

        #cur=inall-outal
        #self.ui.tableView_8.setModel(inall)


    def querproduct(self):
        self.ui.label_21.setText('')
        self.ui.label_22.setText('')
        self.ui.label_24.setText('')
        self.ui.label_26.setText('')
        self.ui.label_28.setText('')

        productno=self.ui.comboBox_2.currentText()
        prodtype=0
        if self.ui.radioButton_5.isChecked():
            prodtype=u'良'
        if self.ui.radioButton_6.isChecked():
            prodtype=u'不良'
        #rs=dbconn.quer(productno,prodtype)
        #print rs
        model=QtSql.QSqlQueryModel()
        sql=u"select prodctuno 编号,time as 时间,prodtype as 良否,qty as 数量,mark as 备注,\
         recordman as 记录人,place as 库位 from record \
         where prodctuno='%s' and prodtype='%s'" %(productno,prodtype)
        model.setQuery(sql)
        self.ui.tableView_3.setModel(model)

        model2=QtSql.QSqlQueryModel()
        sql="select sum(qty) from record where prodctuno='%s' and prodtype='%s'" %(productno,prodtype)
        sql1="select sum(qty) from record where prodctuno='%s'" %(productno)
        sql2="select sum(qty) from outrecord where prodctuno='%s' and prodtype='%s'" %(productno,prodtype)
        sql3="select sum(qty) from outrecord where prodctuno='%s'" %(productno)
        model2.setQuery(sql)
        record=model2.record(0)
        self.ui.label_21.setText(record.value('sum(qty)').toString())

        model2.setQuery(sql1)
        record=model2.record(0)
        self.ui.label_24.setText(record.value('sum(qty)').toString())

        model2.setQuery(sql3)
        record=model2.record(0)
        self.ui.label_22.setText(record.value('sum(qty)').toString())

        model2.setQuery(sql2)
        record=model2.record(0)
        self.ui.label_26.setText(record.value('sum(qty)').toString())

        model1=QtSql.QSqlQueryModel()
        sql=u"select prodctuno as 编号,time as 时间,prodtype as 良否,-qty as 数量,mark as 备注,\
        recordman as 记录人,lingyongman as 领用人,place as 库位 \
        from outrecord where prodctuno='%s' and prodtype='%s'" %(productno,prodtype)
        model1.setQuery(sql)
        self.ui.tableView_4.setModel(model1)
        if self.ui.label_21.text()!='' and self.ui.label_26.text()!='':
            self.ui.label_28.setText(str(int(self.ui.label_21.text())-int(self.ui.label_26.text())))
        elif self.ui.label_21.text()!='' and self.ui.label_26.text()=='':
            self.ui.label_28.setText(str(int(self.ui.label_21.text())))




    def outdata(self):
        import time
        prodtype=0
        qty=0
        if self.ui.radioButton_4.isChecked():
            prodtype=u'良'
        if self.ui.radioButton_3.isChecked():
            prodtype=u'不良'
        if prodtype==0:
            QMessageBox.information(self,'Waring',u'请选择良品或者不良品！！！')
            return
        bh=str(self.ui.comboBox.currentText())
        if self.ui.lineEdit_6.text()=='':
            QMessageBox.information(self,'Waring',u'出库数量不能为空请重新输入！！！')
            return
        else:
            qty=int(self.ui.lineEdit_6.text())
        recordman=str(self.ui.lineEdit_5.text().toUtf8())
        lingyongman=str(self.ui.lineEdit_7.text().toUtf8())
        mark=str(self.ui.lineEdit_21.text().toUtf8())
        #print bh,qty,recordman,mark,prodtype
        kw=str(self.ui.lineEdit_13.text().toUtf8())
        sqlstr=[bh,time.strftime('%Y-%m-%d'),prodtype,qty,mark,recordman,lingyongman,kw]
        # print sqlstr
        self.ui.textEdit.append(u"编号："+bh+u"...时间:"+time.strftime('%Y-%m-%d')+
                            u"...类型:"+prodtype+u"....数量："+
                            str(qty)+u"...备注："+mark+u"...记录人："+
                            recordman+u"....领用人:"+lingyongman+
                            u"....库位："+kw+u"...........数据更新成功！！")
        #dbconn.outdata(sqlstr)
        print sqlstr
        ss=tuple(sqlstr)
        sql1=("insert into outrecord(prodctuno,time,prodtype,qty,mark,recordman,lingyongman,place) \
            values('%s','%s','%s',%d,'%s','%s','%s','%s')" % ss)
        model=QtSql.QSqlQueryModel()
        model.setQuery(sql1)
        print model.submit()
        sql=u'''
            select prodctuno as 编号,time as 时间,prodtype as 良否,qty as 数量,\
            lingyongman as 领用人,
            place as 库位,recordman as 记录人, mark as 备注 from outrecord
            '''
        model.setQuery(sql)
        self.ui.tableView_5.setModel(model)
        self.ui.lineEdit_6.setText('')
        self.ui.lineEdit_7.setText('')
        self.ui.lineEdit_5.setText('')
        self.ui.lineEdit_21.setText('')
        self.ui.lineEdit_13.setText('')


    def tabchange(self):
        self.ui.prono.clear()
        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        plist=dbconn.getprono()
        self.ui.prono.addItems(plist)
        self.ui.comboBox.addItems(plist)
        self.ui.comboBox_2.addItems(plist)

    def selproductno(self):
        index=self.ui.tableView.currentIndex()
        #print index.internalPointer()
    def delproduct(self):
        if self.ui.lineEdit_9.text()=='':
            QMessageBox.information(self,'Waring',u'请输入编号和名称')
        else:
            sqlstr=[self.ui.lineEdit_9.text()]
            name=dbconn.getpronamebyno(self.ui.lineEdit_9.text())
            if dbconn.deldataproduct(sqlstr,)==0:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+name+u"...........数据删除失败，请检查编号和名称是否正确!!!")
            else:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+name+u"...........数据删除成功！！")
        self.model=QtSql.QSqlQueryModel(self)
        sql=u'''
           select prodcutno as 编号,productname as 名称 from productlist
        '''
        self.model.setQuery(sql)
        self.ui.tableView.setModel(self.model)
        self.ui.lineEdit_10.setText('')
        self.ui.lineEdit_9.setText('')

    def addproduct(self):
        if self.ui.lineEdit_9.text()=='' or  self.ui.lineEdit_10.text()=='':
            QMessageBox.information(self,'Waring',u'请输入编号和名称')
        else:
            sqlstr=[self.ui.lineEdit_9.text(),self.ui.lineEdit_10.text()]
            #print sqlstr
            if dbconn.insertdataproduct(sqlstr)==0:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+sqlstr[1]+u"...........数据插入失败，请检查编号和名称是否正确!!!")
            else:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+sqlstr[1]+u"...........数据插入成功！！")
        self.model=QtSql.QSqlQueryModel(self)
        sql=u'''
           select prodcutno as 编号,productname as 名称 from productlist
        '''
        self.model.setQuery(sql)
        self.ui.tableView.setModel(self.model)
        self.ui.lineEdit_10.setText('')
        self.ui.lineEdit_9.setText('')


    def updateproduct(self):
        if self.ui.lineEdit_9.text()=='' or  self.ui.lineEdit_10.text()=='':
            QMessageBox.information(self,'Waring',u'请输入编号和名称')
        else:
            sqlstr=[self.ui.lineEdit_9.text(),str(self.ui.lineEdit_10.text().toUtf8()),self.ui.lineEdit_9.text()]
            if dbconn.updatedataproduct(sqlstr)==0:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+sqlstr[1]+u"...........数据更新失败，请检查编号和名称是否正确!!!")
            else:
                self.ui.textEdit.append(u"编号:"+sqlstr[0]+u".......名称:"+sqlstr[1]+u"...........数据更新成功！！")
        self.model=QtSql.QSqlQueryModel(self)
        sql=u'''
           select prodcutno as 编号,productname as 名称 from productlist
        '''
        self.model.setQuery(sql)
        self.ui.tableView.setModel(self.model)
        self.ui.lineEdit_10.setText('')
        self.ui.lineEdit_9.setText('')

    def cancledate(self):
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_8.setText('')
        self.ui.radioButton.setChecked(True)

    def checkint(self):
        if self.ui.lineEdit_2.text()!='':
            if not str(self.ui.lineEdit_2.text()).isdigit():
                QMessageBox.information(self,'Waring',u'入库数量必须为数字，请输入数字：')
                self.ui.lineEdit_2.setText('')

        if self.ui.lineEdit_6.text()!='':
            if not str(self.ui.lineEdit_6.text()).isdigit():
                QMessageBox.information(self,'Waring',u'出库数量必须为数字，请输入数字：')
                self.ui.lineEdit_6.setText('')

    def updatelineedit(self):
        pname=dbconn.getpronamebyno(self.ui.prono.currentText())
        #print pname
        if pname!=None:
            self.ui.lineEdit.setText(pname)
        else:
            self.ui.lineEdit.setText('')
    def querlineedit(self):
        pname=dbconn.getpronamebyno(self.ui.comboBox_2.currentText())
        #print pname
        if pname!=None:
            self.ui.lineEdit_11.setText(pname)
        else:
            self.ui.lineEdit_11.setText('')

    def updateoutlineedit(self):
        pname=dbconn.getpronamebyno(self.ui.comboBox.currentText())
        #print pname
        if pname!=None:
            self.ui.lineEdit_3.setText(pname)
        else:
            self.ui.lineEdit_3.setText('')

    def insertdata(self):
        #print 'insertdata'
        import time
        prodtype=0
        qty=0
        if self.ui.radioButton.isChecked():
            prodtype=u'良'
        if self.ui.radioButton_2.isChecked():
            prodtype=u'不良'
        if prodtype==0:
            QMessageBox.information(self,'Waring',u'请选择良品或者不良品！！！')
            return
        bh=str(self.ui.prono.currentText())
        if self.ui.lineEdit_2.text()=='':
            QMessageBox.information(self,'Waring',u'入库数量不能为空请重新输入！！！')
            return
        else:
            qty=int(self.ui.lineEdit_2.text())
        kw=str(self.ui.lineEdit_12.text().toUtf8())
        recordman=str(self.ui.lineEdit_4.text().toUtf8())
        mark=str(self.ui.lineEdit_8.text().toUtf8())
        #print bh,qty,recordman,mark,prodtype
        sqlstr=[bh,time.strftime('%Y-%m-%d'),prodtype,qty,mark,recordman,kw]
        #print sqlstr
        self.ui.textEdit.append(u"编号："+bh+u"...时间:"+time.strftime('%Y-%m-%d')+
                                u"...类型:"+prodtype+u"....数量："+
                                str(qty)+u"...备注："+mark+u"...记录人："+
                                recordman+u"...库位:"+kw+u"...........数据更新成功！！")
        #dbconn.insertdata(sqlstr)
        model=QtSql.QSqlQueryModel(self)
        ss=tuple(sqlstr)
        sql1=("insert into record(prodctuno,time,prodtype,qty,mark,recordman,place) \
            values('%s','%s','%s',%d,'%s','%s','%s')" % ss)
        model.setQuery(sql1)
        model.submit()


        sql=u'''
           select prodctuno as 编号,time as 时间,prodtype as 良否,qty as 数量,\
           place as 库位,recordman as 记录人, mark as 备注 from record
        '''
        model.setQuery(sql)
        self.ui.tableView_2.setModel(model)
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_8.setText('')
        self.ui.lineEdit_12.setText('')

    def addinfo(self):
        pass
    #def cancelinfo(self):
        #pass
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    createConnection()
    myapp = myApp()
    myapp.show()
    sys.exit(app.exec_())