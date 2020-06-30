# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alpr_in_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(942, 529)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbEntranceImg = QtWidgets.QLabel(self.centralwidget)
        self.lbEntranceImg.setGeometry(QtCore.QRect(20, 50, 301, 401))
        self.lbEntranceImg.setStyleSheet("padding: 6px;\n"
"background-color: rgba(37, 41, 52, 0.9);")
        self.lbEntranceImg.setText("")
        # self.lbEntranceImg.setPixmap(QtGui.QPixmap("0.jpg"))
        self.lbEntranceImg.setPixmap(QtGui.QPixmap(""))
        self.lbEntranceImg.setScaledContents(True)
        self.lbEntranceImg.setObjectName("lbEntranceImg")
        self.lbEntranceTxt = QtWidgets.QLabel(self.centralwidget)
        self.lbEntranceTxt.setGeometry(QtCore.QRect(20, 10, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lbEntranceTxt.setFont(font)
        self.lbEntranceTxt.setStyleSheet("background-color: #45567d;\n"
"color: #f5f5f5;\n"
"padding: 3px;\n"
"border-radius: 1px;\n"
"")
        self.lbEntranceTxt.setAlignment(QtCore.Qt.AlignCenter)
        self.lbEntranceTxt.setObjectName("lbEntranceTxt")
        self.lbInformation = QtWidgets.QLabel(self.centralwidget)
        self.lbInformation.setGeometry(QtCore.QRect(660, 10, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.lbInformation.setFont(font)
        self.lbInformation.setStyleSheet("background-color: #45567d;\n"
"color: #f5f5f5;\n"
"padding: 3px;\n"
"border-radius: 1px;\n"
"")
        self.lbInformation.setAlignment(QtCore.Qt.AlignCenter)
        self.lbInformation.setObjectName("lbInformation")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(660, 50, 251, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.hLayStaff = QtWidgets.QHBoxLayout()
        self.hLayStaff.setObjectName("hLayStaff")
        self.hLayParkingLot = QtWidgets.QHBoxLayout()
        self.hLayParkingLot.setObjectName("hLayParkingLot")
        self.hLayCamera = QtWidgets.QHBoxLayout()
        self.hLayCamera.setObjectName("hLayCamera")
        self.hLayRFID = QtWidgets.QHBoxLayout()
        self.hLayRFID.setObjectName("hLayRFID")
        self.hLayPlateNumber = QtWidgets.QHBoxLayout()
        self.hLayPlateNumber.setObjectName("hLayPlateNumber")
        self.hLayNotification = QtWidgets.QHBoxLayout()
        self.hLayNotification.setObjectName("hLayNotification")

        self.verticalLayout.addLayout(self.hLayStaff)
        self.verticalLayout.addLayout(self.hLayParkingLot)
        self.verticalLayout.addLayout(self.hLayCamera)
        self.verticalLayout.addLayout(self.hLayRFID)
        self.verticalLayout.addLayout(self.hLayPlateNumber)
        self.verticalLayout.addLayout(self.hLayNotification)
        #Add Label to Information Horizontal Layouts:
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        lbStyle = "background-color:rgba(37, 41, 52, 0.9);color: aliceblue; padding-left:10px;margin-top:2px;"
        lbTxtStyle="background-color:#f5f5f5; padding-left:5px;"
        self.lbStaff = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbStaff.setFont(font)
        self.lbStaff.setStyleSheet(lbStyle)

        self.lbStaffDesc = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbStaffDesc.setFont(font)
        self.lbStaffDesc.setStyleSheet(lbTxtStyle)

        self.lbParkingLot = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbParkingLot.setStyleSheet(lbStyle)
        self.lbParkingLot.setFont(font)

        self.lbParkingLotDesc = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbParkingLotDesc.setFont(font)
        self.lbParkingLotDesc.setStyleSheet(lbTxtStyle)

        self.lbCamera = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbCamera.setStyleSheet(lbStyle)
        self.lbCamera.setFont(font)

        self.lbCameraDesc = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbCameraDesc.setFont(font)
        self.lbCameraDesc.setStyleSheet(lbTxtStyle)
        self.lbRFID = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbRFID.setStyleSheet(lbStyle)
        self.lbRFID.setFont(font)
        self.lbRFIDDesc = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbRFIDDesc.setFont(font)
        self.lbRFIDDesc.setStyleSheet(lbTxtStyle)
        self.lbPlateNumber = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbPlateNumber.setStyleSheet(lbStyle)
        self.lbPlateNumber.setFont(font)
        self.lbPlateNumberDesc = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lbPlateNumberDesc.setFixedWidth(127)
        self.lbPlateNumberDesc.setFixedHeight(55)
        self.lbPlateNumberDesc.setFont(font)
        self.lbPlateNumberDesc.setStyleSheet(lbTxtStyle)
        self.lbNotification = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbNotification.setFont(font)
        self.lbNotification.setStyleSheet(lbTxtStyle)


        self.hLayStaff.addWidget(self.lbStaff)
        self.hLayStaff.addWidget(self.lbStaffDesc)

        self.hLayParkingLot.addWidget(self.lbParkingLot)
        self.hLayParkingLot.addWidget(self.lbParkingLotDesc)

        self.hLayCamera.addWidget(self.lbCamera)
        self.hLayCamera.addWidget(self.lbCameraDesc)

        self.hLayRFID.addWidget(self.lbRFID)
        self.hLayRFID.addWidget(self.lbRFIDDesc)

        self.hLayPlateNumber.addWidget(self.lbPlateNumber)
        self.hLayPlateNumber.addWidget(self.lbPlateNumberDesc)

        self.hLayNotification.addWidget(self.lbNotification)
        ################################################################
        ## Buttons:
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnEnter = QtWidgets.QPushButton(self.centralwidget)
        self.btnEnter.setGeometry(QtCore.QRect(660, 400, 121, 51))
        self.btnEnter.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnEnter.setFont(font)
        self.btnEnter.setStyleSheet("#btnEnter:hover{background-color: #be3144;color: aliceblue;}")
        self.btnEnter.setObjectName("btnEnter")
        
        self.btnSkip = QtWidgets.QPushButton(self.centralwidget)
        self.btnSkip.setGeometry(QtCore.QRect(790, 400, 121, 51))
        self.btnSkip.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSkip.setStyleSheet("#btnSkip:hover{background-color: #45567d;color: aliceblue;}")
        self.btnSkip.setFont(font)
        self.btnSkip.setObjectName("btnSkip")

        #####################################################################

        self.lbEntranceImg_2 = QtWidgets.QLabel(self.centralwidget)
        self.lbEntranceImg_2.setGeometry(QtCore.QRect(340, 50, 301, 401))
        self.lbEntranceImg_2.setStyleSheet("padding: 6px;\n"
"background-color: rgba(37, 41, 52, 0.9);")
        self.lbEntranceImg_2.setText("")
        self.lbEntranceImg_2.setPixmap(QtGui.QPixmap("0.jpg"))
        self.lbEntranceImg_2.setScaledContents(True)
        self.lbEntranceImg_2.setObjectName("lbEntranceImg_2")
        self.lbEntranceTxt_2 = QtWidgets.QLabel(self.centralwidget)
        self.lbEntranceTxt_2.setGeometry(QtCore.QRect(340, 10, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.lbEntranceTxt_2.setFont(font)
        self.lbEntranceTxt_2.setStyleSheet("background-color: #45567d;\n"
"color: #f5f5f5;\n"
"padding: 3px;\n"
"border-radius: 1px;\n"
"")
        self.lbEntranceTxt_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbEntranceTxt_2.setObjectName("lbEntranceTxt_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 942, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setNotifications(self, notifications):
        self.lbNotification.setText(notifications)

    def msg_box(self,text='', msg_type='error', detail=''):
        msg = QMessageBox()
        msg_type = msg_type.upper()

        if msg_type == 'ERROR':
                title = msg_type
                icon = QMessageBox.Critical
                buttons = QMessageBox.Ok
        ## More msg_type here:

        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(buttons)
        msg.setDetailedText(detail)
        msg.exec_()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbEntranceTxt.setText(_translate("MainWindow", "Entrance Gate"))
        self.lbInformation.setText(_translate("MainWindow", "Information"))
        self.lbStaff.setText(_translate("MainWindow", "Staff ID"))
        self.lbParkingLot.setText(_translate("MainWindow", "PKL ID:"))
        self.lbCamera.setText(_translate("MainWindow", "Camera ID:"))
        self.lbRFID.setText(_translate("MainWindow", "RFID:"))
        self.lbPlateNumber.setText(_translate("MainWindow", "Plate:"))
        self.btnEnter.setText(_translate("MainWindow", "Enter"))
        self.btnSkip.setText(_translate("MainWindow", "Skip"))
        self.lbEntranceTxt_2.setText(_translate("MainWindow", "Exit Gate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNew.setText(_translate("MainWindow", "New.."))
        self.actionOpen.setText(_translate("MainWindow", "Open.."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
