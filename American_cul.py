#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:56:57 2020

@author: leixiaojing
"""

import sys
from PyQt5.QtWidgets import *
from Americanui import Ui_Form
from BiTree import *
class Main(QWidget,Ui_Form):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)        
        self.pushButton.clicked.connect(self.cul)
        self.pushButton_2.clicked.connect(self.close)
    def cul(self):
        s0 = float(self.lineEdit.text())
        sigma = float(self.lineEdit_2.text())
        r = float(self.lineEdit_3.text())
        n = int(self.lineEdit_4.text())
        t = float(self.lineEdit_5.text())
        k = float(self.lineEdit_6.text())
        typ = self.lineEdit_7.text()
        op = BiTree(typ,s0,sigma,r,t,k,n)
        answer = op.calc()                      
        show = ("The answer is: \n" + str(answer))
                                
        self.textBrowser.setText(show)
        
        

if __name__ =="__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
