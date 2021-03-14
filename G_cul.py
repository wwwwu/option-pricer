#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:56:47 2020

@author: leixiaojing
"""

import sys
from PyQt5.QtWidgets import *
from Geometricuiui import Ui_Form
from GeoAsianOption import *
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
        n = float(self.lineEdit_4.text())
        T = float(self.lineEdit_5.text())
        K = float(self.lineEdit_6.text())
        typ = self.lineEdit_7.text()
        op = GeoAsianOption(typ,s0, sigma, r, T, K,
                 n)
        answer = op.calc()
        self.textBrowser.setText("The answer is: \n" + str(answer))
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    
