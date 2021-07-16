from PyQt5 import QtCore, QtGui, QtWidgets
import os
import socket,cv2, pickle,struct
from cryptography.fernet import Fernet

with open('Key.key','rb') as f:
    key = f.read()

fernet = Fernet(key)

class Ui_MainWindow(object):
    def startclient(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_ip = self.lineEdit.text() #server ip address
        port = 9999
        client_socket.connect((host_ip,port))
        if client_socket:
            self.ipname.setText("Video Connected")
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
                while len(data) < payload_size:
                        packet = client_socket.recv(4096) # 4KB data
                        if not packet: break
                        data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0] 
	
                while len(data) < msg_size:
                        data += client_socket.recv(4096) #receiving encrypted data from client
                frame_data = data[:msg_size] #breaking data into equal sized segments
                frame_data=fernet.decrypt(frame_data) #decrypting received data
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("RECEIVING VIDEO",frame) #display video
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                        self.ipname.setText("Video Disconnected")
                        break
        client_socket.close()
    
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 380, 151, 28))
        self.pushButton.setObjectName("pushButton")
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(250, 60, 231, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 60, 161, 20))
        self.label.setObjectName("label")
        self.ipname = QtWidgets.QLabel(self.centralwidget)
        self.ipname.setGeometry(QtCore.QRect(350, 170, 100, 16))
        self.ipname.setText("")
        self.ipname.setObjectName("status")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 167, 150, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.startclient)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Connect to server"))
        self.label.setText(_translate("MainWindow", "IP address of host :"))
        self.label_3.setText(_translate("MainWindow", "Connection status :"))
	
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
