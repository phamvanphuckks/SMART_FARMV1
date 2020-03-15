from PyQt5.QtWidgets import QFileDialog, QAction, QGroupBox, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.QtCore    import QTimer, QTime, QThread, pyqtSignal, Qt
from PyQt5.QtGui     import QPixmap, QCloseEvent, QColor
from PyQt5           import QtWidgets, uic, QtGui, QtCore

import constant  as CONSTANT
import sys, socket


class qt5Class():
    def __init__(self):
        self.App = QtWidgets.QApplication([])
        self.app = uic.loadUi("guis\\main.ui")
        self.app.closeEvent = self.closeEvent # khi close, gọi sự kiện closeEvent
        self.app.label_12.hide()
        self.LCD_Number()
        self.Upadte_Pin_Relay()
        self.initialize()
        # self.Update_RF_Relay()

    def debugg(self, error, information):
        QMessageBox.critical(self.app, error, information)

    def initialize(self): # khi mình khởi động off hết
        for i in range(1, 6):
            self.UpdatePicture(i, 0)
        if(self.check_internet()== True):
            self.display_internet(1)
        else:
            self.display_internet(0)
        self.app.label_2.hide()


    def closeEvent(self, event: QCloseEvent):
        # QMessageBox.critical(self.app, "LỖI NGUY HIỂM","KHÔNG NÊN TẮT PHẦN MỀM KHI KHÔNG CẦN THIẾT!!!")
        reply = QMessageBox.question(self.app, 'Window Close', 'Are you sure you want to close the window?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            print('Window closed')
        else:
            event.ignore()

    def Update_L(self, data_payload, option, location):
        if(location == "G00"):
            if (option == 1):
                if (data_payload['NODE23']['value'] <= CONSTANT.L['min']):
                    self.app.tab1_l1.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE23']['value']  >= CONSTANT.L['max']):
                    self.app.tab1_l1.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_l1.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_l1.setText(str(data_payload['NODE23']['value'] ))
            else:
                pass
        elif(location == "G01"):
            if(option == 2):
                if (data_payload['NODE24']['value']  <= CONSTANT.L['min']):
                    self.app.tab1_l2.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE24']['value']  >= CONSTANT.L['max']):
                    self.app.tab1_l2.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_l2.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_l2.setText(str(data_payload['NODE24']['value'] ))
            else:
                pass
        else:
            pass

# PH

    def Update_PH(self, data_payload, option, location):
        if(location == "G00"):
            if (option == 1):
                if (data_payload['NODE32']['value'] <= CONSTANT.PH['min']):
                    self.app.tab1_ph1.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE32']['value'] >= CONSTANT.PH['max']):
                    self.app.tab1_ph1.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_ph1.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_ph1.setText(str(data_payload['NODE32']['value']))
            else:
                pass
        elif(location == "G01"):
            if(option == 2):
                if (data_payload['NODE33']['value'] <= CONSTANT.PH['min']):
                    self.app.tab1_ph2.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE33']['value'] >= CONSTANT.PH['max']):
                    self.app.tab1_ph2.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_ph2.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_ph2.setText(str(data_payload['NODE33']['value']))
            else:
                pass
        else:
            pass

# Nhiệt độ

    def Update_T(self, data_payload, option, location):
        if(location == "G00"):
            if (option == 1):
                if (data_payload['NODE25']['value'] <= CONSTANT.T['min']):
                    self.app.tab1_t1.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE25']['value'] >= CONSTANT.T['max']):
                    self.app.tab1_t1.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_t1.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_t1.setText(str(data_payload['NODE25']['value']))
            else:
                pass
        elif(location == "G01"):
            if (option == 2):
                if (data_payload['NODE26']['value'] <= CONSTANT.T['min']):
                    self.app.tab1_t2.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE26']['value'] >= CONSTANT.T['max']):
                    self.app.tab1_t2.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_t2.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_t2.setText(str(data_payload['NODE26']['value']))
            else:
                pass
        else:
            pass
# Độ ẩm KK

    def Update_H(self, data_payload, option, location):
        if(location == "G00"):
            if (option == 1):
                if (data_payload['NODE21']['value'] <= CONSTANT.H['min']):
                    self.app.tab1_h1.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE21']['value'] >= CONSTANT.H['max']):
                    self.app.tab1_h1.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_h1.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_h1.setText(str(data_payload['NODE21']['value']))
            else:
                pass
        elif(location == "G01"):
            if(option == 2):
                if (data_payload['NODE22']['value'] <= CONSTANT.H['min']):
                    self.app.tab1_h2.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE22']['value'] >= CONSTANT.H['max']):
                    self.app.tab1_h2.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_h2.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_h2.setText(str(data_payload['NODE22']['value']))
            else:
                pass
        else:
            pass

# Độ ẩm Đất

    def Update_SM(self, data_payload, option, location):
        if(location == "G00"):
            if (option == 1):
                if (data_payload['NODE1']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm1.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE1']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm1.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm1.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm1.setText(str(data_payload['NODE1']['value'] ))

            if (option == 2):
                if (data_payload['NODE2']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm2.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE2']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm2.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm2.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm2.setText(str(data_payload['NODE2']['value'] ))

            if (option == 3):
                if (data_payload['NODE3']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm3.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE3']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm3.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm3.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm3.setText(str(data_payload['NODE3']['value'] ))

            if (option == 4):
                if (data_payload['NODE4']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm4.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE4']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm4.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm4.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm4.setText(str(data_payload['NODE4']['value'] ))
            if (option == 5):
                if (data_payload['NODE5']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm5.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE5']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm5.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm5.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm5.setText(str(data_payload['NODE5']['value'] ))
            if (option == 6):
                if (data_payload['NODE6']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm6.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE6']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm6.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm6.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm6.setText(str(data_payload['NODE6']['value'] ))
            if (option == 7):
                if (data_payload['NODE7']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm7.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE7']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm7.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm7.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm7.setText(str(data_payload['NODE7']['value'] ))
            if (option == 8):
                if (data_payload['NODE8']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm8.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE8']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm8.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm8.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm8.setText(str(data_payload['NODE8']['value'] ))
            if (option == 9):
                if (data_payload['NODE9']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm9.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE9']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm9.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm9.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm9.setText(str(data_payload['NODE9']['value'] ))
            if (option == 10):
                if (data_payload['NODE10']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm10.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE10']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm10.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm10.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm10.setText(str(data_payload['NODE10']['value'] ))
            else:
                pass
        elif(location == "G01"):
            if (option == 11):
                if (data_payload['NODE11']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm11.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE11']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm11.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm11.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm11.setText(str(data_payload['NODE11']['value'] ))
            if (option == 12):
                if (data_payload['NODE12']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm12.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE12']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm12.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm12.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm12.setText(str(data_payload['NODE12']['value'] ))
            if (option == 13):
                if (data_payload['NODE13']['value']  <= CONSTANT.SM['min']):
                    self.app.tab1_sm13.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE13']['value']  >= CONSTANT.SM['max']):
                    self.app.tab1_sm13.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm13.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm13.setText(str(data_payload['NODE13']['value'] ))
            if (option == 14):
                if (data_payload['NODE14']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm14.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE14']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm14.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm14.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm14.setText(str(data_payload['NODE14']['value']))
            if (option == 15):
                if (data_payload['NODE15']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm15.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE15']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm15.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm15.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm15.setText(str(data_payload['NODE15']['value']))
            if (option == 16):
                if (data_payload['NODE16']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm16.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE16']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm16.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm16.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm16.setText(str(data_payload['NODE16']['value']))
            if (option == 17):
                if (data_payload['NODE17']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm17.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE17']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm17.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm17.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm17.setText(str(data_payload['NODE17']['value']))
            if (option == 18):
                if (data_payload['NODE18']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm18.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE18']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm18.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm18.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm18.setText(str(data_payload['NODE18']['value']))
            if (option == 19):
                if (data_payload['NODE19']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm19.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE19']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm19.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm19.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm19.setText(str(data_payload['NODE19']['value']))
            if (option == 20):
                if (data_payload['NODE20']['value'] <= CONSTANT.SM['min']):
                    self.app.tab1_sm20.setStyleSheet(
                        "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                elif (data_payload['NODE20']['value'] >= CONSTANT.SM['max']):
                    self.app.tab1_sm20.setStyleSheet(
                        "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                else:
                    self.app.tab1_sm20.setStyleSheet(
                        "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                self.app.tab1_sm20.setText(str(data_payload['NODE20']['value']))
            else:
                pass
        else:
            pass

    # hướng phát triển của 2 function này
    # đầu vào sẽ nhận hàm data_payload, option sẽ là thứ tự của các relay
    def Upadte_Pin_Relay(self):
        self.app.tab2_pin1.setText("Pin : 100" )
        self.app.tab2_pin2.setText("Pin : 100" )
        self.app.tab2_pin3.setText("Pin : 100" )
        self.app.tab2_pin4.setText("Pin : 100" )
        self.app.tab2_pin5.setText("Pin : 100" )

    def Update_RF_Relay(self, data_payload):
        self.app.tab2_th1.setText("TÍN HIỆU" + str(data_payload["NODE27"]["RF_signal"]))
        # self.app.tab2_th2.setText("TÍN HIỆU" + str(data_payload["NODE28"]["RF_signal"]))
        # self.app.tab2_th3.setText("TÍN HIỆU" + str(data_payload["NODE29"]["RF_signal"]))
        # self.app.tab2_th4.setText("TÍN HIỆU" + str(data_payload["NODE30"]["RF_signal"]))
        # self.app.tab2_th5.setText("TÍN HIỆU" + str(data_payload["NODE31"]["RF_signal"]))

    def check_internet(self):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80), 1)
            return True
        except OSError:
            pass
        return False

    def display_internet(self, option):
        if (option == 1):
            self.app.lbl_internet.hide()

        else:
            self.app.lbl_internet.show()
            self.app.lbl_internet.setStyleSheet(
                "QLabel {color: red; border-radius: 9px;   border: 2px solid red}")
            self.app.lbl_internet.setText("KHÔNG CÓ INTERNET")



    def chang_status_RL(self, device, status):
        if (device == 1):
            if (status == 1):
                self.app.tab2_img_1.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_on.png"))
                self.app.tab2_btn_r1on.setStyleSheet(
                    "QPushButton {background-color: rgb(0, 170, 0);}")
                self.app.tab2_btn_r1off.setStyleSheet(
                    "QPushButton {background-color: rgb(229, 229, 229);}")
            elif (status == 0):
                self.app.tab2_img_1.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_off.jpg"))        
                self.app.tab2_btn_r1on.setStyleSheet(
                    "QPushButton {background-color: rgb(229, 229, 229);}")
                self.app.tab2_btn_r1off.setStyleSheet(
                    "QPushButton {background-color: rgb(255, 0, 0);}")
            else:
                pass
        elif (device == 2):
            if (status == 1):
                self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\curtain_on.png"))
                self.app.tab2_btn_r2on.setStyleSheet(
                        "QPushButton {background-color: rgb(0, 170, 0);}")
                self.app.tab2_btn_r2off.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")

            elif (status == 0):
                self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\curtain_off.png"))
                self.app.tab2_btn_r2on.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                self.app.tab2_btn_r2off.setStyleSheet(
                        "QPushButton {background-color: rgb(255, 0, 0);}")
            else:
                pass
        elif (device == 3):
            if (status == 1):
                self.app.tab2_img_3.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_on.png"))
                self.app.tab2_btn_r3on.setStyleSheet(
                        "QPushButton {background-color: rgb(0, 170, 0);}")
                self.app.tab2_btn_r3off.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
            elif (status == 0):
                self.app.tab2_img_3.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_off.jpg"))
                self.app.tab2_btn_r3on.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                self.app.tab2_btn_r3off.setStyleSheet(
                        "QPushButton {background-color: rgb(255, 0, 0);}")
            else:
                pass
        elif (device == 4):
            if (status == 1):
                self.app.tab2_img_4.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\curtain_on.png"))
                self.app.tab2_btn_r4on.setStyleSheet(
                        "QPushButton {background-color: rgb(0, 170, 0);}")
                self.app.tab2_btn_r4off.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
            elif (status == 0):
                self.app.tab2_img_4.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\curtain_off.png"))
                self.app.tab2_btn_r4on.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                self.app.tab2_btn_r4off.setStyleSheet(
                        "QPushButton {background-color: rgb(255, 0, 0);}")
            else:
                pass
        elif (device == 5):
            if (status == 1):
                self.app.tab2_img_5.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_on.png"))
                self.app.tab2_btn_r5on.setStyleSheet(
                        "QPushButton {background-color: rgb(0, 170, 0);}")
                self.app.tab2_btn_r5off.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
            elif (status == 0):
                self.app.tab2_img_5.setPixmap(QtGui.QPixmap(
                    "photos\\dieu_khien_thiet_bi\\wplum_off.jpg"))
                self.app.tab2_btn_r5on.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                self.app.tab2_btn_r5off.setStyleSheet(
                        "QPushButton {background-color: rgb(255, 0, 0);}")
            else:
                pass
        else:
            pass

    def UpdatePicture(self, device, status): # update picture when press
        if(device == 1):
            if(status == 1):    # relay1 on
                self.chang_status_RL(1, 1)
            elif(status == 0):  # relay1 off
                self.chang_status_RL(1, 0)
                # khi mà counter ấn off - dừng luôn

                if(CONSTANT.SubThread_pump1.isActive()):
                    CONSTANT.SubThread_pump1.stop() # dừng bơm lại
                    CONSTANT.flag_pump1   = 0   #trở về trạng thái bắt đầu
                    CONSTANT.flag_pump1_N = 1
                    CONSTANT.TIME["pump1"]["minute"] = 0    # cập nhập lại biến time
                    CONSTANT.TIME["pump1"]["second"] = 10
                    self.app.lcdNumber.hide() 
            else:
                pass
        elif(device == 2):
            if(status == 1):   
                self.chang_status_RL(2, 1)
            elif(status == 0):
                self.chang_status_RL(2, 0)

                if(CONSTANT.SubThread_lamp1.isActive()):
                    CONSTANT.SubThread_lamp1.stop() # dừng bơm lại
                    CONSTANT.flag_lamp1 = 0 
                    CONSTANT.flag_lamp1_N = 1
                    CONSTANT.TIME["lamp1"]["minute"] = 0    # cập nhập lại biến time
                    CONSTANT.TIME["lamp1"]["second"] = 10
                    self.app.lcdNumber_2.hide() 
            else:
                pass
        elif(device == 3):
            if(status == 1):   
                self.chang_status_RL(3, 1)
            elif(status == 0):
                self.chang_status_RL(3, 0)

                if(CONSTANT.SubThread_pump2.isActive()):
                    CONSTANT.SubThread_pump2.stop() # dừng bơm lại
                    CONSTANT.flag_pump2 = 0 
                    CONSTANT.flag_pump2_N = 1
                    CONSTANT.TIME["pump2"]["minute"] = 0    # cập nhập lại biến time
                    CONSTANT.TIME["pump2"]["second"] = 10                    
                    self.app.lcdNumber_3.hide() 
            else:
                pass
        elif(device == 4):
            if(status == 1):    
                self.chang_status_RL(4, 1)
            elif(status == 0):
                self.chang_status_RL(4, 0)

                if(CONSTANT.SubThread_lamp2.isActive()):
                    CONSTANT.SubThread_lamp2.stop() # dừng bơm lại
                    CONSTANT.flag_lamp2 = 0 
                    CONSTANT.flag_lamp2_N = 1
                    CONSTANT.TIME["lamp2"]["minute"] = 0    # cập nhập lại biến time
                    CONSTANT.TIME["lamp2"]["second"] = 10
                    self.app.lcdNumber_4.hide()
            else:
                pass
        elif(device == 5):
            if(status == 1):  
                self.chang_status_RL(5, 1)
            elif(status == 0):
                self.chang_status_RL(5, 0)
                if(CONSTANT.SubThread_pump3.isActive()):
                    CONSTANT.SubThread_pump3.stop() # dừng bơm lại
                    CONSTANT.flag_pump3 = 0 
                    CONSTANT.flag_pump3_N = 1
                    CONSTANT.TIME["pump3"]["minute"] = 0    # cập nhập lại biến time
                    CONSTANT.TIME["pump3"]["second"] = 10
                    self.app.lcdNumber_5.hide() 
            else:
                pass
        else:
            pass


    # mới xử lý được từ 2 phút - 00 : nhưng chưa có chỗ nào phục hồi lại 
    # giá trị 2p đó - bug
    def LCD_Number(self):
        global h,m,s

        # time = QTime.currentTime()
        # text = time.toString('hh:mm:ss')
        # self.app.lcdNumber.display(text)
        # time = ("{0}:{1}".format(5,"00"))
        # self.app.lcdNumber.setDigitCount(5) # hien thi so dem

        # current_time = datetime.now().strftime("%H:%M:%S")
        # self.app.lcdNumber_2.display(text)
        # self.app.lcdNumber_3.display(text)
        # self.app.lcdNumber_4.display(text)
        # self.app.lcdNumber_5.display(text)

        self.app.lcdNumber.hide()
        self.app.lcdNumber_2.hide()
        self.app.lcdNumber_3.hide()
        self.app.lcdNumber_4.hide()
        self.app.lcdNumber_5.hide()
        pass


    # format 5:00 - time = ("{0}:{1}".format(m,s))

    def countdown_pump1(self):
        if (CONSTANT.TIME["pump1"]["second"] > 0):
            CONSTANT.TIME["pump1"]["second"] -= 1
        else:
            if (CONSTANT.TIME["pump1"]["minute"] > 0):
                CONSTANT.TIME["pump1"]["minute"]  -= 1
                CONSTANT.TIME["pump1"]["second"] = 59
            elif((CONSTANT.TIME["pump1"]["minute"] ==0) & (CONSTANT.TIME["pump1"]["second"]==0)):
                self.app.lcdNumber.hide() 
                CONSTANT.SubThread_pump1.stop() # dừng bơm lại
                CONSTANT.flag_pump1 = 0 
                CONSTANT.flag_pump1_N = 0
                return 
            else:
                pass 
        time = ("{0}:{1}".format(CONSTANT.TIME["pump1"]["minute"] , CONSTANT.TIME["pump1"]["second"])) 

        self.app.lcdNumber.show()
        self.app.lcdNumber.setDigitCount(len(time))
        self.app.lcdNumber.display(time)

    def countdown_pump2(self):
        if (CONSTANT.TIME["pump2"]["second"] > 0):
            CONSTANT.TIME["pump2"]["second"] -= 1
        else:
            if (CONSTANT.TIME["pump2"]["minute"] > 0):
                CONSTANT.TIME["pump2"]["minute"]  -= 1
                CONSTANT.TIME["pump2"]["second"] = 59
            elif((CONSTANT.TIME["pump2"]["minute"] ==0) & (CONSTANT.TIME["pump2"]["second"]==0)):
                self.app.lcdNumber_3.hide() 
                CONSTANT.SubThread_pump2.stop() # dừng bơm lại
                CONSTANT.flag_pump2 = 0 
                CONSTANT.flag_pump2_N = 0
                return 
            else:
                pass 
        time = ("{0}:{1}".format(CONSTANT.TIME["pump2"]["minute"] , CONSTANT.TIME["pump2"]["second"])) 

        self.app.lcdNumber_3.show()
        self.app.lcdNumber_3.setDigitCount(len(time))
        self.app.lcdNumber_3.display(time)

    def countdown_pump3(self):
        if (CONSTANT.TIME["pump3"]["second"] > 0):
            CONSTANT.TIME["pump3"]["second"] -= 1
        else:
            if (CONSTANT.TIME["pump3"]["minute"] > 0):
                CONSTANT.TIME["pump3"]["minute"]  -= 1
                CONSTANT.TIME["pump3"]["second"] = 59
            elif((CONSTANT.TIME["pump3"]["minute"] ==0) & (CONSTANT.TIME["pump3"]["second"]==0)):
                self.app.lcdNumber_5.hide() 
                CONSTANT.SubThread_pump3.stop() # dừng bơm lại
                CONSTANT.flag_pump3 = 0 
                CONSTANT.flag_pump3_N = 0
                return 
            else:
                pass 
        time = ("{0}:{1}".format(CONSTANT.TIME["pump3"]["minute"] , CONSTANT.TIME["pump3"]["second"])) 

        self.app.lcdNumber_5.show()
        self.app.lcdNumber_5.setDigitCount(len(time))
        self.app.lcdNumber_5.display(time)

    def countdown_lamp1(self):
        if CONSTANT.TIME["lamp1"]["second"] > 0:
            CONSTANT.TIME["lamp1"]["second"]  -=1
        else:
            if CONSTANT.TIME["lamp1"]["minute"]  > 0:
                CONSTANT.TIME["lamp1"]["minute"] -= 1
                CONSTANT.TIME["lamp1"]["second"]  = 59
            elif((CONSTANT.TIME["lamp1"]["minute"] ==0) & (CONSTANT.TIME["lamp1"]["second"] ==0)):
                self.app.lcdNumber_2.hide() 
                CONSTANT.SubThread_lamp1.stop() # dừng bơm lại
                CONSTANT.flag_lamp1 = 0 
                CONSTANT.flag_lamp1_N = 0
                return
            else:
                pass 
        time = ("{0}:{1}".format(CONSTANT.TIME["lamp1"]["minute"] , CONSTANT.TIME["lamp1"]["second"] )) 
        self.app.lcdNumber_2.show()
        self.app.lcdNumber_2.setDigitCount(len(time))
        self.app.lcdNumber_2.display(time)

    def countdown_lamp2(self):
        if CONSTANT.TIME["lamp2"]["second"] > 0:
            CONSTANT.TIME["lamp2"]["second"]  -=1
        else:
            if CONSTANT.TIME["lamp2"]["minute"]  > 0:
                CONSTANT.TIME["lamp2"]["minute"] -= 1
                CONSTANT.TIME["lamp2"]["second"]  = 59
            elif((CONSTANT.TIME["lamp2"]["minute"] ==0) & (CONSTANT.TIME["lamp2"]["second"] ==0)):
                self.app.lcdNumber_4.hide() 
                CONSTANT.SubThread_lamp2.stop() # dừng bơm lại
                CONSTANT.flag_lamp2 = 0 
                CONSTANT.flag_lamp2_N = 0
                return
            else:
                pass 
        time = ("{0}:{1}".format(CONSTANT.TIME["lamp2"]["minute"] , CONSTANT.TIME["lamp2"]["second"] )) 
        self.app.lcdNumber_4.show()
        self.app.lcdNumber_4.setDigitCount(len(time))
        self.app.lcdNumber_4.display(time)
 