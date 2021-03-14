#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 19:07:23 2020

@author: leixiaojing
"""

import sys
from PyQt5.QtWidgets import *
from mainwindow import Ui_Form
import Europeancul, IV_cul,G_cul,Artih_cul,American_cul


class MainWindow(QWidget,Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)        
        self.pushButton.clicked.connect(self.Eur)
        self.pushButton_2.clicked.connect(self.IV)
        self.pushButton_3.clicked.connect(self.American)
        self.pushButton_4.clicked.connect(self.Geo)
        self.pushButton_5.clicked.connect(self.Arith)
        self.pushButton_6.clicked.connect(self.close)
    def Eur(self):       
        self.newDialog = Europeancul.Main()
        self.newDialog.show()
    def IV(self):
        self.newDialog = IV_cul.Main()
        self.newDialog.show()
    def American(self):
        self.newDialog = American_cul.Main()
        self.newDialog.show()
    def Geo(self):
        self.newDialog = G_cul.Main()
        self.newDialog.show()
    def Arith(self):
        self.newDialog = Artih_cul.Main()
        self.newDialog.show()
                

if __name__ =="__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

        