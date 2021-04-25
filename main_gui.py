from PyQt5 import QtCore, QtGui, QtWidgets
from Face.myFDA import MyFda
from Mask.myMDA import MyMDA
from Databases.dbHandler import DbHandler
import tkinter.messagebox as msgbx
import tkinter as tk


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 640))
        MainWindow.setMaximumSize(QtCore.QSize(800, 640))
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r'res/icon.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Menu Bar Parent
        self.Menus = QtWidgets.QTabWidget(self.centralwidget)
        self.Menus.setGeometry(QtCore.QRect(0, 0, 800, 640))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Menus.sizePolicy().hasHeightForWidth())
        self.Menus.setSizePolicy(sizePolicy)
        self.Menus.setMinimumSize(QtCore.QSize(800, 640))
        self.Menus.setMaximumSize(QtCore.QSize(800, 640))
        self.Menus.setObjectName("Menus")

        # Menu About
        self.menuAbout = QtWidgets.QWidget()
        self.menuAbout.setObjectName("menuAbout")
        self.bgAbout = QtWidgets.QLabel(self.menuAbout)
        self.bgAbout.setGeometry(QtCore.QRect(0, 0, 800, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bgAbout.sizePolicy().hasHeightForWidth())
        self.bgAbout.setSizePolicy(sizePolicy)
        self.bgAbout.setText("")
        self.bgAbout.setPixmap(QtGui.QPixmap("res/about.png"))
        self.bgAbout.setObjectName("bgAbout")

        # Menu Setup
        self.Menus.addTab(self.menuAbout, "")
        self.menuSetup = QtWidgets.QWidget()
        self.menuSetup.setObjectName("menuSetup")
        self.bgSetup = QtWidgets.QLabel(self.menuSetup)
        self.bgSetup.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.bgSetup.setText("")
        self.bgSetup.setTextFormat(QtCore.Qt.PlainText)
        self.bgSetup.setPixmap(QtGui.QPixmap("res/Setup.png"))
        self.bgSetup.setObjectName("bgSetup")
        self.getNameSetup = QtWidgets.QLineEdit(self.menuSetup)  # Name Input Box
        self.getNameSetup.setEnabled(True)
        self.getNameSetup.setGeometry(QtCore.QRect(60, 410, 460, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.getNameSetup.setFont(font)
        self.getNameSetup.setAcceptDrops(False)
        self.getNameSetup.setInputMethodHints(QtCore.Qt.ImhNone)
        self.getNameSetup.setMaxLength(30)
        self.getNameSetup.setReadOnly(False)
        self.getNameSetup.setObjectName("getNameSetup")
        self.btnSetup = QtWidgets.QPushButton(self.menuSetup)  # Enter button to get name
        self.btnSetup.clicked.connect(lambda: self.cmdSetup())
        self.btnSetup.setGeometry(QtCore.QRect(620, 400, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btnSetup.setFont(font)
        self.btnSetup.setDefault(False)
        self.btnSetup.setFlat(False)
        self.btnSetup.setObjectName("btnSetup")

        # Train Model Menu
        self.Menus.addTab(self.menuSetup, "")
        self.menuTrain = QtWidgets.QWidget()
        self.menuTrain.setObjectName("menuTrain")
        self.bgTrain = QtWidgets.QLabel(self.menuTrain)
        self.bgTrain.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.bgTrain.setText("")
        self.bgTrain.setTextFormat(QtCore.Qt.PlainText)
        self.bgTrain.setPixmap(QtGui.QPixmap("res/trainmodel.png"))
        self.bgTrain.setObjectName("bgTrain")

        self.btnTrain = QtWidgets.QPushButton(self.menuTrain)
        self.btnTrain.clicked.connect(lambda: self.cmdTrain())
        self.btnTrain.setGeometry(QtCore.QRect(360, 380, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btnTrain.setFont(font)
        self.btnTrain.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                    "color: rgb(255, 255, 255);")
        self.btnTrain.setDefault(False)
        self.btnTrain.setFlat(False)
        self.btnTrain.setObjectName("btnTrain")

        # Deploy Menu
        self.Menus.addTab(self.menuTrain, "")
        self.menuDeploy = QtWidgets.QWidget()
        self.menuDeploy.setObjectName("menuDeploy")
        self.bgDeploy = QtWidgets.QLabel(self.menuDeploy)
        self.bgDeploy.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.bgDeploy.setText("")
        self.bgDeploy.setTextFormat(QtCore.Qt.PlainText)
        self.bgDeploy.setPixmap(QtGui.QPixmap("res/deploy.png"))
        self.bgDeploy.setObjectName("bgDeploy")

        self.btnDeploy = QtWidgets.QPushButton(self.menuDeploy)
        self.btnDeploy.clicked.connect(lambda: self.cmdDeploy())
        self.btnDeploy.setGeometry(QtCore.QRect(580, 260, 81, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDeploy.sizePolicy().hasHeightForWidth())
        self.btnDeploy.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btnDeploy.setFont(font)
        self.btnDeploy.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
                                     "color: rgb(255, 255, 255);")
        self.btnDeploy.setDefault(False)
        self.btnDeploy.setFlat(False)
        self.btnDeploy.setObjectName("btnDeploy")

        # Admin Control Panel
        self.Menus.addTab(self.menuDeploy, "")
        self.menuAdmin = QtWidgets.QWidget()
        self.menuAdmin.setObjectName("menuAdmin")
        self.noMaskTable = QtWidgets.QTableWidget(self.menuAdmin)

        self.noMaskTable.setGeometry(QtCore.QRect(20, 50, 751, 281))
        self.noMaskTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.noMaskTable.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.noMaskTable.setObjectName("noMaskTable")
        self.noMaskTable.setColumnCount(3)
        self.noMaskTable.setColumnWidth(0, 248)
        self.noMaskTable.setColumnWidth(1, 248)
        self.noMaskTable.setColumnWidth(2, 248)

        self.noMaskTable.setHorizontalHeaderLabels(['Name', 'Time', 'Date'])

        self.btnAdminReset = QtWidgets.QPushButton(self.menuAdmin)
        self.btnAdminReset.clicked.connect(lambda: self.cmdReset())
        self.btnAdminReset.setGeometry(QtCore.QRect(680, 560, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btnAdminReset.setFont(font)
        self.btnAdminReset.setDefault(False)
        self.btnAdminReset.setFlat(False)
        self.btnAdminReset.setObjectName("btnAdminReset")

        self.btnAdminRefresh = QtWidgets.QPushButton(self.menuAdmin)
        self.btnAdminRefresh.clicked.connect(lambda: self.cmdRefresh())
        self.btnAdminRefresh.setGeometry(QtCore.QRect(550, 560, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.btnAdminRefresh.setFont(font)
        self.btnAdminRefresh.setDefault(False)
        self.btnAdminRefresh.setFlat(False)
        self.btnAdminRefresh.setObjectName("btnAdminRefresh")

        self.lbAdmin = QtWidgets.QLabel(self.menuAdmin)
        self.lbAdmin.setGeometry(QtCore.QRect(20, 20, 751, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbAdmin.setFont(font)
        self.lbAdmin.setObjectName("lbAdmin")
        self.Menus.addTab(self.menuAdmin, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.Menus.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def cmdSetup(self):
        objSetup = MyFda(self.getNameSetup.text())
        status = objSetup.inputImgDataset()
        if status:
            notif = msgbx.showinfo("Success", "Data stored successfully!")
        else:
            notif = msgbx.showerror("Failed", "Reset the database from Admin Panel and try again")
    def cmdTrain(self):
        objTrain = MyFda("")

        s1, s2 = objTrain.trainImgDataset()
        if s1 and s2:

            notif = msgbx.showinfo("Success", "Model Successfully Trained and Saved!")

        else:
            notif = msgbx.showerror("Failed", "Reset the database from Admin Panel and try again")

    def cmdDeploy(self):
        objDeploy = MyMDA()
        objDeploy.ioMain()



    def cmdReset(self):

        objReset = DbHandler("", "")
        objReset.deleteall()



    def cmdRefresh(self):
        dbInstance = DbHandler("", "")
        data_rows = dbInstance.displayDb()
        try:
            for i in range(self.noMaskTable.rowCount()):
                self.noMaskTable.removeRow(i)
        except:
            pass
        for row in data_rows:
            nos = data_rows.index(row)
            self.noMaskTable.insertRow(nos)

            self.noMaskTable.setItem(nos, 0, QtWidgets.QTableWidgetItem(row[1]))
            self.noMaskTable.setItem(nos, 1, QtWidgets.QTableWidgetItem(row[2]))
            self.noMaskTable.setItem(nos, 2, QtWidgets.QTableWidgetItem(row[3]))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Param Dane\'s Advanced Tensorflow Application"))
        self.Menus.setTabText(self.Menus.indexOf(self.menuAbout), _translate("MainWindow", "About"))
        self.btnSetup.setText(_translate("MainWindow", "Start"))
        self.Menus.setTabText(self.Menus.indexOf(self.menuSetup), _translate("MainWindow", "Setup"))
        self.btnTrain.setText(_translate("MainWindow", "Start"))
        self.Menus.setTabText(self.Menus.indexOf(self.menuTrain), _translate("MainWindow", "Train Model"))
        self.btnDeploy.setText(_translate("MainWindow", "DEPLOY"))
        self.Menus.setTabText(self.Menus.indexOf(self.menuDeploy), _translate("MainWindow", "Deploy Application"))
        self.btnAdminReset.setText(_translate("MainWindow", "Reset"))
        self.btnAdminRefresh.setText(_translate("MainWindow", "Refresh"))
        self.lbAdmin.setText(_translate("MainWindow", "People detected without masks:"))
        self.Menus.setTabText(self.Menus.indexOf(self.menuAdmin), _translate("MainWindow", "Admin Control Panel"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
