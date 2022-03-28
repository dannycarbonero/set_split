# set_split Front End Initializer
# Created by: PyQt5 UI code generator 5.15.2
# C.

from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_Dialog(object):

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(884, 951)

        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(10, 10, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.tracklist_label = QtWidgets.QLabel(Dialog)
        self.tracklist_label.setGeometry(QtCore.QRect(440, 20, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.tracklist_label.setFont(font)
        self.tracklist_label.setObjectName("tracklist_label")

        self.tracklist_link = QtWidgets.QTextEdit(Dialog)
        self.tracklist_link.setGeometry(QtCore.QRect(440, 55, 300, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tracklist_link.setFont(font)
        self.tracklist_link.setObjectName("tracklist_link")

        self.tracklist_update = QtWidgets.QPushButton(Dialog)
        self.tracklist_update.setGeometry(QtCore.QRect(760, 55, 100, 35))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tracklist_update.setFont(font)
        self.tracklist_update.setObjectName("update")

        self.tracklist_disp = QtWidgets.QTextBrowser(Dialog)
        self.tracklist_disp.setGeometry(QtCore.QRect(440, 100, 421, 631))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tracklist_disp.setFont(font)
        self.tracklist_disp.setObjectName("tracklist_disp")

        self.get_file = QtWidgets.QPushButton(Dialog)
        self.get_file.setGeometry(QtCore.QRect(15, 100, 151, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.get_file.setFont(font)
        self.get_file.setObjectName("get_file")

        self.file_path = QtWidgets.QLabel(Dialog)
        self.file_path.setGeometry(QtCore.QRect(15, 175, 384, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_path.setFont(font)
        self.file_path.setObjectName("file_path")

        self.output_label = QtWidgets.QLabel(Dialog)
        self.output_label.setGeometry(QtCore.QRect(12, 250, 256, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.output_label.setFont(font)
        self.output_label.setObjectName("output_label")

        self.output_dir = QtWidgets.QLabel(Dialog)
        self.output_dir.setGeometry(QtCore.QRect(15, 300, 384, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_dir.setFont(font)
        self.output_dir.setObjectName("output_dir")

        self.album_artist_input = QtWidgets.QTextEdit(Dialog)
        self.album_artist_input.setGeometry(QtCore.QRect(440, 790, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.album_artist_input.setFont(font)
        self.album_artist_input.setObjectName("album_artist_input")

        self.album_artist_label = QtWidgets.QLabel(Dialog)
        self.album_artist_label.setGeometry(QtCore.QRect(440, 760, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.album_artist_label.setFont(font)
        self.album_artist_label.setObjectName("album_artist_label")

        self.album_label = QtWidgets.QLabel(Dialog)
        self.album_label.setGeometry(QtCore.QRect(440, 850, 160, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.album_label.setFont(font)
        self.album_label.setObjectName("album_label")

        self.album_input = QtWidgets.QTextEdit(Dialog)
        self.album_input.setGeometry(QtCore.QRect(440, 880, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.album_input.setFont(font)
        self.album_input.setObjectName("album_input")

        self.genre_label = QtWidgets.QLabel(Dialog)
        self.genre_label.setGeometry(QtCore.QRect(690, 850, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.genre_label.setFont(font)
        self.genre_label.setObjectName("genre_label")

        self.genre_input = QtWidgets.QTextEdit(Dialog)
        self.genre_input.setGeometry(QtCore.QRect(690, 880, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.genre_input.setFont(font)
        self.genre_input.setObjectName("genre_input")

        self.offset_label = QtWidgets.QLabel(Dialog)
        self.offset_label.setGeometry(QtCore.QRect(690, 760, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.offset_label.setFont(font)
        self.offset_label.setObjectName("offset_label")

        self.offset_input = QtWidgets.QTextEdit(Dialog)
        self.offset_input.setGeometry(QtCore.QRect(690, 790, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.offset_input.setFont(font)
        self.offset_input.setObjectName("offset_input")

        self.output_update = QtWidgets.QTextBrowser(Dialog)
        self.output_update.setGeometry(QtCore.QRect(40, 375, 380, 384))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.output_update.setFont(font)
        self.output_update.setObjectName("output_update")

        self.run = QtWidgets.QPushButton(Dialog)
        self.run.setGeometry(QtCore.QRect(80, 780, 281, 141))
        font = QtGui.QFont()
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        self.run.setFont(font)
        self.run.setObjectName("run")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def retranslateUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title.setText(_translate("Dialog", "Set Split"))
        self.get_file.setText(_translate("Dialog", "Select File"))
        self.output_label.setText(_translate("Dialog", "Output Directory:"))
        self.tracklist_label.setText(_translate("Dialog", "Tracklist:"))
        self.tracklist_disp.setText(_translate("Dialog", "Tracklist Will Show Here"))
        self.tracklist_update.setText(_translate("Dialog", "Update"))
        self.tracklist_link.setText(_translate("Dialog", "Paste 1001 tracklists Set Link Here"))
        self.album_artist_label.setText(_translate("Dialog", "Album Artist:"))
        self.album_label.setText(_translate("Dialog", "Album:"))
        self.genre_label.setText(_translate("Dialog", "Genre:"))
        self.offset_label.setText(_translate("Dialog", "Offset (s)"))
        self.run.setText(_translate("Dialog", "Run"))
        Dialog.setWindowTitle('Set Split')
