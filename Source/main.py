from PyQt5.QtWidgets import QFileDialog, QAction, QGroupBox, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.QtCore    import QTimer, QTime, QThread, pyqtSignal
from PyQt5           import QtCore,QtGui
from datetime        import datetime   # date_time

import sys, time, json, socket    # library in python

import serial
import serial.tools.list_ports
import random
import paho.mqtt.client as mqtt # mqtt

# library programer development
import constant     as  CONSTANT
import db_handler   as  SQLite

from gateway    import Gateway
from Lora       import Gateway1
from qt5        import qt5Class


# define globale
Windowns = qt5Class()
DB       = SQLite.DataBase()

'''
---------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------
'''

#--define MQTT--------------------------------------
MQTT_HOST = 'smartfarm.tinasoft.com.vn'
MQTT_USER = 'smartFarm'
MQTT_PWD  = 'Smartktdt1@123!'
MQTT_TOPIC_SEND    = 'send_data'
MQTT_TOPIC_CONTROL = 'controller'
MQTT_TOPIC_STATUS  = 'control_status'


MQTT_TOPIC_BACKUP  = 'backup_data'

def Init_mqtt():
    global client
    if (check_internet() == True): # kiểm tra internet nếu có gửu cho a vững
        client = mqtt.Client()
        client.username_pw_set(MQTT_USER, MQTT_PWD)
        client.connect(MQTT_HOST, 1883)
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_start()
        get_status_all()
        print("connect mqtt")
    else:
        Windowns.debugg("Lỗi kết nối", "Không có internet")

#--end--------------------------------------------------------------------------------------------------------


#---controller device------------------------------------------------------------------------------------------
'''
+ hàm điểu khiển thiết bị
    + UpdatePicture() trong file qt5.py,  
    + control_RL() trong file gateway_v1.py
    + get_status() : gửu message trạng thái của relay lên server
'''
def ControlDevice(device, status): # kiêu kiểu thế này
    if (device == 1):  # pump1
        if(status == 1):
            # GW_Blue.control_RL(5, 1, 1) # GateWay(Xanh) điểu khiển Relay 
            Windowns.UpdatePicture(device, status) # thay đổi trên app
            get_status(27)    # sau khi bấm gửu trạng thái của tất cả relay lên web, hàm này chưa hoàn thiện
            print("RELAY1 ON") 
        elif(status == 0):
            # GW_Blue.control_RL(5, 1, 0)
            Windowns.UpdatePicture(device, status)
            get_status(27)
            print("RELAY1 OFF") 
        else:
            pass
    elif(device == 2): # lamp1
        if(status == 1):
            # GW_Blue.control_RL(1, 1) # GateWay(Xanh) điểu khiển Relay 
            Windowns.UpdatePicture(device, status) # thay đổi trên app
            get_status(28)
            print("RELAY2 ON") 
        elif(status == 0):
        #            GW_Blue.control_RL(1, 0)
            Windowns.UpdatePicture(device, status)
            get_status(28)
            print("RELAY2 OFF") 
        else:
            pass
    elif(device == 3): # pump2
        if(status == 1):
        #            GW_Blue.control_RL(1, 1) # GateWay(Xanh) điểu khiển Relay 
            Windowns.UpdatePicture(device, status) # thay đổi trên app
            get_status(29)
            print("RELAY3 ON") 
        elif(status == 0):
        #            GW_Blue.control_RL(1, 0)
            Windowns.UpdatePicture(device, status)
        #                get_status_all()
            get_status(29)
            print("RELAY3 OFF") 
        else:
            pass
    elif(device == 4): # lamp2
        if(status == 1):
        #            GW_Blue.control_RL(1, 1) # GateWay(Xanh) điểu khiển Relay 
            Windowns.UpdatePicture(device, status) # thay đổi trên app
            get_status(30)
            print("RELAY4 ON") 
        elif(status == 0):
        #            GW_Blue.control_RL(1, 0)
            Windowns.UpdatePicture(device, status)
            get_status(30)
            print("RELAY4 OFF") 
        else:
            pass
    elif(device == 5): # pump3
        if(status == 1):
        #            GW_Blue.control_RL(1, 1) # GateWay(Xanh) điểu khiển Relay 
            Windowns.UpdatePicture(device, status) # thay đổi trên app
            get_status(31)
            print("RELAY5 ON") 
        elif(status == 0):
        #            GW_Blue.control_RL(1, 0)
            Windowns.UpdatePicture(device, status)
            get_status(31)
            print("RELAY5 OFF") 
        else:
            pass 
    else:
        if(status == 1):
        #            GW_Blue.control_RL(1, 1) # GateWay(Xanh) điểu khiển Relay 
                    Windowns.UpdatePicture(device, status) # thay đổi trên app
        #            if (check_internet() == 1):
        #                get_status_all()    # sau khi bấm gửu trạng thái của tất cả relay lên web, hàm này chưa hoàn thiện
        elif(status == 0):
        #            GW_Blue.control_RL(1, 0)
                    Windowns.UpdatePicture(device, status)
        #            if (check_internet() == 1):
        #                get_status_all()
        else:
            pass

'''
    + lấy trạng thái của tất cả thiết bị relay
    + Init_mqtt() gọi function này : cập nhập lại button khi mất mạng và khi khởi động hệ thống
'''
def get_status_all(): # lấy trạng thái hiện tại của thiet bi
    global client, GW_Blue

    # # Relay trang trai G00
    # payload_dataG00 = {
    #     'sub_id'     : "G00",
    #     'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'time'       : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "relay_1": {
    #         "RF_signal": GW_Blue.get_RFsignal(5),
    #         'value'    : str(GW_Blue.get_status_RL(5,1)),
    #         'battery'  : 100
    #     },
    #     # "relay_2": {
    #     #     "RF_signal": GW_Blue.get_RFsignal(28),
    #     #     'value'    : str(GW_Blue.get_status_RL(28,1)),
    #     #     'battery'  : 100
    #     # }
    # }
    # # Relay trang trai G01
    # payload_dataG01 = {
    #     'sub_id'     : "G01",
    #     'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     'time'       : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #     "relay_1": {
    #         "RF_signal": GW_Blue.get_RFsignal(5),
    #         'value'    : str(GW_Blue.get_status_RL(5,1)),
    #         'battery'  : 100
    #     },
    #     # "relay_2": {
    #     #     "RF_signal": GW_Blue.get_RFsignal(28),
    #     #     'value'    : str(GW_Blue.get_status_RL(28,1)),
    #     #     'battery'  : 100
    #     # }
    # }

    # if (check_internet() == True): 
    #     client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_dataG00))
    #     client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_dataG01))

    #     print( json.dumps(payload_dataG00))
    #     print( json.dumps(payload_dataG01))

    # else:
    #     print("topic MQTT_TOPIC_STATUS ko dc guu")
    #     pass
    pass


'''
    + lấy trạng thái của từng relay
    G00 : relay_1, relay_2
    G01 : relay_1, relay_2
'''
def get_status(pos): 
    global client, GW_Blue
    # neu ma la 27 phai chinh 5 thanh 27
    # CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]     = int(GW_Blue.get_status_RL(5, 1))
    # CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"] = GW_Blue.get_RFsignal(5, CONSTANT.SENSOR["relay"])
    # CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"]        = GW_Blue.get_node_id(5, CONSTANT.SENSOR["relay"])

    # 1 nong trai se co 2 relay Relay_1 va relay_2
    if(pos == 27):
        payload_data = {
            'sub_id': "G00",
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_1": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                'battery': 100
            }
        }
    elif(pos == 28):
        payload_data = {
            'sub_id': "G00",
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_2": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                'battery': 100
            }
        }
    elif(pos == 29):
        payload_data = {
            'sub_id': "G01",
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_1": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                'battery': 100
            }
        }
    elif(pos == 30):
        payload_data = {
            'sub_id': "G01",
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_2": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                'battery': 100
            }
        }
    elif(pos == 31):
        payload_data = {
            'sub_id': "G01",
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_5": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                'battery': 100
            }
        }
    else:
        pass
    
    # publish message to server and insert database controller
    if(check_internet() == True): 
        DB.insert_data_row("controller", pos, CONSTANT.DATA_RELAY["NODE" + str(pos)]["name"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"],
        CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"], 100, 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ok")
        print("connect to internet")
        client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_data))

        print(json.dumps(payload_data))

    else:
        DB.insert_data_backup_row("backup_controller", pos, CONSTANT.DATA_RELAY["NODE" + str(pos)]["name"],CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"],
        CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"], 100, 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error")
        print("disconnect to internet")


def on_connect(client, userdata, flags, rc):    # subscrie on  topic
    # print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_CONTROL)

def on_message(client, userdata, msg):  # received data - chua code xong
    print(msg.topic+" "+str(msg.payload))
    data = json.loads(msg.payload.decode('utf-8'))
    if ("relay_1" in data): 
        if (data['relay_1']['value'] == '1'):
            ControlDevice(1, 1)
        if (data['relay_1']['value'] == '0'):
            ControlDevice(1, 0)
    if ("relay_2" in data):
        if (data['relay_2']['value'] == '1'):
            ControlDevice(2, 1)
        if (data['relay_2']['value'] == '0'):
            ControlDevice(2, 0)
            print("Máy 2 OFF")
    if ("relay_3" in data):
        if (data['relay_3']['value'] == '1'):
            ControlDevice(3, 1)
        if (data['relay_3']['value'] == '0'):
            ControlDevice(3, 0)
    if ("relay_4" in data):
        if (data['relay_4']['value'] == '1'):
            ControlDevice(4, 1)
        if (data['relay_4']['value'] == '0'):
            ControlDevice(4, 0)
    if ("relay_5" in data):

def Init_Button():
    Windowns.app.tab2_btn_r1off.clicked.connect(lambda:ControlDevice(1, 0))
    Windowns.app.tab2_btn_r1on.clicked.connect(lambda:ControlDevice(1, 1))

    Windowns.app.tab2_btn_r2off.clicked.connect(lambda:ControlDevice(2, 0))
    Windowns.app.tab2_btn_r2on.clicked.connect(lambda:ControlDevice(2, 1))

    Windowns.app.tab2_btn_r3off.clicked.connect(lambda:ControlDevice(3, 0))
    Windowns.app.tab2_btn_r3on.clicked.connect(lambda:ControlDevice(3, 1))

    Windowns.app.tab2_btn_r4off.clicked.connect(lambda:ControlDevice(4, 0))
    Windowns.app.tab2_btn_r4on.clicked.connect(lambda:ControlDevice(4, 1))

    Windowns.app.tab2_btn_r5off.clicked.connect(lambda:ControlDevice(5, 0))
    Windowns.app.tab2_btn_r5on.clicked.connect(lambda:ControlDevice(5, 1))  

#---end ----------------------------------------------------------------------------------------------------------


#--- Update Data--------------------------------------------------------------------------------------------------
def Init_UI(): # khởi tạo GateWay_Xanh
    global GW_Blue

    ports = serial.tools.list_ports.comports()
    check_device = ''

    if(len(ports) > 0): # khởi tạo để kết nối với GateWay(Xanh)
        for port in ports:
            # print(port)
            if ("USB-SERIAL CH340" in str(port)):
                check_device = port.device
                break
        if (check_device != ''):
            GW_Blue = Gateway(CONSTANT.GW_Blue_NAME)   #Define GW_Blue kế thừa CONSTANT.GW_Blue_NAME
            print("Da ket noi GateWay")
        else:
            QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI",
                                      "KHÔNG ĐÚNG THIẾT BỊ")
            sys.exit()
    else:
        QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI",
                                  "KHÔNG CÓ COM NÀO ĐƯỢC KẾT NỐI")
        sys.exit()

def Init_Lora(): # khoi tao GateWay do
    global GW_Red, app
    ports = serial.tools.list_ports.comports() # mảng những ports các kết nối vào máy tính nhúng
    check_device = ''

    if(len(ports) > 0):
        for port in ports:
            if ("USB-SERIAL CH340" in str(port) or "USB-to-Serial" in str(port)):
                check_device = port.device
                print(check_device)
                break
        if (check_device != ''):
            GW_Red = Gateway1(CONSTANT.GW_Red_NAME, 9600, 0.2)
            print("Da ket noi Lora")            
        else:
            print("Không đúng thiết bị!")
            QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI COM",
                                      "KHÔNG ĐÚNG THIẾT BỊ!")
            sys.exit() # đóng phần mềm
    else:
        QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI COM",
                                  "KHÔNG CÓ COM NÀO KẾT NỐI!")
        sys.exit()
    try: # đưa GateWay(đỏ) vào mode nhận
        GW_Red.open() # mở cổng COM
        GW_Red.write_data("AT\r\n")
        print(GW_Red.read_data())
        GW_Red.write_data("AT+MODE=TEST\r\n")
        print(GW_Red.read_data())
        GW_Red.write_data("AT+TEST=RFCFG,433\r\n")
        print(GW_Red.read_data())
        GW_Red.write_data("AT+TEST=RXLRPKT\r\n")
        print(GW_Red.read_data())
    except:
        QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI COM",
                                  "KHÔNG THỂ KẾT NỐI")
        pass

def Update_GatewayRed():
    global GW_Red, Windowns

    try:
        GW_Red.load_data()
        # kiểm tra khi mà đọc được cả 2 cảm biến PH
        if((CONSTANT.DATA_G00["NODE32"]["syn"] == "ok") & (CONSTANT.DATA_G01["NODE33"]["syn"] == "ok")):
            # Xoa bo ID
            CONSTANT.DATA_G00["NODE32"]["syn"] = "error"
            CONSTANT.DATA_G01["NODE33"]["syn"] = "error"

            Windowns.Update_PH(CONSTANT.DATA_G00, 1)
            Windowns.Update_PH(CONSTANT.DATA_G01, 2)

            return True
        else:
            return False
    except:
        pass

def Update_GatewayBlue():
    global GW_Blue, Windowns, client
    # # Trang trại G00

    # # cảm biến độ ẩm đất 
    # try:
    #     for i in range(1, 3):
    #         CONSTANT.DATA_G00["NODE" + str(i)]["value"]     = GW_Blue.get_main_parameter(i, CONSTANT.SENSOR["soil_moistrure"])
    #         CONSTANT.DATA_G00["NODE" + str(i)]["battery"]      = GW_Blue.get_battery(i, CONSTANT.SENSOR["soil_moistrure"])
    #         CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]   = GW_Blue.get_RFsignal(i, CONSTANT.SENSOR["soil_moistrure"])
    #         CONSTANT.DATA_G00["NODE" + str(i)]["id"]       = GW_Blue.get_node_id(i, CONSTANT.SENSOR["soil_moistrure"])
    #         CONSTANT.DATA_G00["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         CONSTANT.DATA_G00["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     print(json.dumps(CONSTANT.DATA_G00))
    #     if (check_internet() == True): # nếu có mạng gửu chuỗi cho a vững
    #         client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G00))
    #     else:
    #         print("Khong co mang")
    # except:
    #     pass
    # # cảm biến độ ẩm không khí
    # CONSTANT.DATA["NODE25"]["DATA"] = int(GW_Blue.get_main_parameter(3, CONSTANT.SENSOR["HUMIDITY"]))
    # CONSTANT.DATA["NODE25"]["PIN"]  = GW_Blue.get_battery(3, CONSTANT.SENSOR["HUMIDITY"])
    # CONSTANT.DATA["NODE25"]["SIGNAL"]   = GW_Blue.get_RFsignal(3, CONSTANT.SENSOR["HUMIDITY"])
    # CONSTANT.DATA["NODE25"]["ID"]   = GW_Blue.get_node_id(3, CONSTANT.SENSOR["HUMIDITY"])   
    # # cảm biến ánh sáng
    # CONSTANT.DATA["NODE21"]["DATA"] = int(GW_Blue.get_main_parameter(4, CONSTANT.SENSOR["LIGHT"]))
    # CONSTANT.DATA["NODE21"]["PIN"]  = GW_Blue.get_battery(4, CONSTANT.SENSOR["LIGHT"])
    # CONSTANT.DATA["NODE21"]["SIGNAL"]   = GW_Blue.get_RFsignal(4, CONSTANT.SENSOR["LIGHT"])
    # CONSTANT.DATA["NODE21"]["ID"]   = GW_Blue.get_node_id(4, CONSTANT.SENSOR["LIGHT"])   
    # # cảm biến nhiệt độ

    #----random-------------------------------------------------------------------------------
    for i in range(1, 11):
        CONSTANT.DATA_G00["NODE" + str(i)]["value"]       = random.randint(1,100)
        CONSTANT.DATA_G00["NODE" + str(i)]["battery"]     = random.randint(1,100)
        CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]   = "perfect"
        CONSTANT.DATA_G00["NODE" + str(i)]["id"]       = random.randint(10000,99999)
        CONSTANT.DATA_G00["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        CONSTANT.DATA_G00["time"]                      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if (check_internet() == True): # nếu có mạng gửu Data lên server
        DB.insert_data_nongtraiG00("nongtrai_G00", "ok")
    else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
        DB.insert_data_backup_nongtraiG00("backup_nongtrai_G00", "error")

    for i in range(11, 21):
        CONSTANT.DATA_G01["NODE" + str(i)]["value"]        = random.randint(1, 100)
        CONSTANT.DATA_G01["NODE" + str(i)]["battery"]      = random.randint(1,100)
        CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"]    = "perfect"
        CONSTANT.DATA_G01["NODE" + str(i)]["id"]       = random.randint(10000,99999)
        CONSTANT.DATA_G01["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        CONSTANT.DATA_G01["time"]                      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if (check_internet() == True): # nếu có mạng gửu Data lên server
        DB.insert_data_nongtraiG01("nongtrai_G01", "ok")  
    else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
        DB.insert_data_backup_nongtraiG01("backup_nongtrai_G01", "error")  

    # humidity
    for i in range(21, 23):
        if(i==21):
            CONSTANT.DATA_G00["NODE" + str(i)]["value"]        = random.randint(1,100)
            CONSTANT.DATA_G00["NODE" + str(i)]["battery"]      = random.randint(1,100)
            CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G00["NODE" + str(i)]["id"]           = random.randint(10000,99999)
            CONSTANT.DATA_G00["NODE" + str(i)]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G00["time"]                          = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G00", CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G00", CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"error")  
        elif(i==22):
            CONSTANT.DATA_G01["NODE" + str(i)]["value"]        = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["battery"]      = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G01["NODE" + str(i)]["id"]           = random.randint(10000,99999)
            CONSTANT.DATA_G01["NODE" + str(i)]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G01["time"]                          = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G01", CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G01", CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"error")  
        else:
            pass

    #light
    for i in range(23, 25):
        if(i==23):
            CONSTANT.DATA_G00["NODE" + str(i)]["value"]        = random.randint(1, 100)
            CONSTANT.DATA_G00["NODE" + str(i)]["battery"]      = random.randint(1, 100)
            CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G00["NODE" + str(i)]["id"]       = random.randint(10000, 99999)
            CONSTANT.DATA_G00["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G00["time"]                      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G00", CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G00", CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"error")  
        elif(i==24):
            CONSTANT.DATA_G01["NODE" + str(i)]["value"]        = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["battery"]      = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G01["NODE" + str(i)]["id"]       = random.randint(10000, 99999)
            CONSTANT.DATA_G01["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G01["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G01",CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G01", CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"error")  
        else:
            pass

    #temperature
    for i in range(25, 27):
        if(i==25):
            CONSTANT.DATA_G00["NODE" + str(i)]["value"]        = random.randint(1,100)
            CONSTANT.DATA_G00["NODE" + str(i)]["battery"]      = random.randint(1,100)
            CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G00["NODE" + str(i)]["id"]       = random.randint(10000,99999)
            CONSTANT.DATA_G00["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G00["time"]                      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G00",CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G00",CONSTANT.DATA_G00["NODE" + str(i)]["node"],CONSTANT.DATA_G00["NODE" + str(i)]["name"],CONSTANT.DATA_G00["NODE" + str(i)]["id"],
                CONSTANT.DATA_G00["NODE" + str(i)]["value"],CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"], CONSTANT.DATA_G00["NODE" + str(i)]["time"],"ok")  
        elif(i==26):
            CONSTANT.DATA_G01["NODE" + str(i)]["value"]        = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["battery"]      = random.randint(1,100)
            CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"]    = "perfect"
            CONSTANT.DATA_G01["NODE" + str(i)]["id"]       = random.randint(10000,99999)
            CONSTANT.DATA_G01["NODE" + str(i)]["time"]     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CONSTANT.DATA_G01["time"]                      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if (check_internet() == True): # nếu có mạng gửu Data lên server
                DB.insert_data_row("nongtrai_G01",CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"ok")  
            else:   # nêu không có mạng thì ghi vào cơ sở dữ liệu backup - syn-ERROR
                DB.insert_data_backup_row("backup_nongtrai_G01", CONSTANT.DATA_G01["NODE" + str(i)]["node"],CONSTANT.DATA_G01["NODE" + str(i)]["name"],CONSTANT.DATA_G01["NODE" + str(i)]["id"],
                CONSTANT.DATA_G01["NODE" + str(i)]["value"],CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"],
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"], CONSTANT.DATA_G01["NODE" + str(i)]["time"],"error")  
        else:
            pass

    #---end-----------------------------------------------------------------------------


    # update GUI - thieu PH
    for i in range(1, 11):
        Windowns.Update_SM(CONSTANT.DATA_G00, i, "G00")

    for i in range(11, 21):
        Windowns.Update_SM(CONSTANT.DATA_G01, i, "G01")

    Windowns.Update_H(CONSTANT.DATA_G00, 1, "G00")
    Windowns.Update_H(CONSTANT.DATA_G01, 2, "G01")

    Windowns.Update_L(CONSTANT.DATA_G00, 1, "G00")
    Windowns.Update_L(CONSTANT.DATA_G01, 2, "G01")

    Windowns.Update_T(CONSTANT.DATA_G00, 1, "G00")
    Windowns.Update_T(CONSTANT.DATA_G01, 2, "G01")
    # --end-------------------------------------------------------------------------

    # update RF_signal relay
    # for i in range(27, 31):
    #     CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"] = GW_Blue.get_RFsignal(i, CONSTANT.SENSOR["relay"])

    # CONSTANT.DATA_RELAY["NODE27"]["RF_signal"]   = GW_Blue.get_RFsignal(5, CONSTANT.SENSOR["relay"])
    # Windowns.Update_RF_Relay(CONSTANT.DATA_RELAY)
    #---end--------------------------------



    # send message to server

    if(check_internet() == True): 
        client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G00)) 
        client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G01)) 
    else:
        # Windowns.debugg("Lỗi kết nối", "Không có internet")
        print("khong co mang")

    # print(CONSTANT.DATA_G00)
    # print(CONSTANT.DATA_G01)

def check_internet():   # kiểm tra internet
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80), 2)
        return True
    except:
        return False

# nên ghi vào một file text rồi đọc ra - or la fix cung luon
def requirePort(): # Xac dinh COM 
    global GW_Blue_NAME, GW_Red_NAME 
    try:
        CONSTANT.GW_Blue_NAME  = input("Lua chon COM cho GateWay Xanh: ")
        # CONSTANT.GW_Red_NAME   = input("Lua chon COM cho GateWay Do: ")
    except KeyboardInterrupt:
        sys.exit()

    # su dung viec doc file
    # file = open("port\\port.txt", "r")
    # CONSTANT.GW_Blue_NAME = file.readline()
    # CONSTANT.GW_Red_NAME  = file.readline()
    # print(str)
    # # Đóng file
    # file.close()

#---end-----------------------------------------------------------------------------------------------------------





#---define thread-------------------------------------------------------------------------------------------------
# 0 1 -  khoi dau
# 0 0 -  dung
# 1 1 -  chay
# 1 0 - reserve
def Thread_pump1(): # flag_pump1 = 0 - chưa bật máy bơm, chưa đếm lùi - nếu flag_pump1 = 1 thì ko làm gì cả
    # bỏ cờ flag_pump1,flag_pump1_N=> khi mà điều kiện true. sẽ ra lệnh bệnh máy bơm nhiều lần
    if((CONSTANT.flag_pump1 == 0) & (CONSTANT.flag_pump1_N == 1)): 
        if(random.randint(1, 20) > 18): # kiểm tra điều kiện- nhớ phải xét khoảng, 10< y 20<đây chưa xét khoảng
            CONSTANT.SubThread_pump1.start(1000) # bắt đầu đếm lui
            ControlDevice(1, 1)                 # Bật máy bơm
            CONSTANT.flag_pump1   = 1          
            CONSTANT.flag_pump1_N = 1
    elif((CONSTANT.flag_pump1 == 0) & (CONSTANT.flag_pump1_N == 0)):
        ControlDevice(1, 0)
        CONSTANT.TIME["pump1"]["minute"] = 0
        CONSTANT.TIME["pump1"]["second"] = 10
        CONSTANT.flag_pump1 = 0  
        CONSTANT.flag_pump1_N = 1
    else:
        pass

def Thread_pump2():
    if((CONSTANT.flag_pump2 == 0) & (CONSTANT.flag_pump2_N == 1)):
        if(random.randint(1, 20) > 18): # kiểm tra điều kiện- nhớ phải xét khoảng, đây chưa xét khoảng
            CONSTANT.SubThread_pump2.start(1000) # bắt đầu đếm lui
            ControlDevice(3, 1)                 # Bật máy bơm
            CONSTANT.flag_pump2   = 1          
            CONSTANT.flag_pump2_N = 1

    elif((CONSTANT.flag_pump2 == 0) & (CONSTANT.flag_pump2_N == 0)):
        ControlDevice(3, 0)
        CONSTANT.TIME["pump2"]["minute"] = 0
        CONSTANT.TIME["pump2"]["second"]  = 10
        CONSTANT.flag_pump2 = 0  
        CONSTANT.flag_pump2_N = 1
    else:
        pass

def Thread_pump3():
    if((CONSTANT.flag_pump3 == 0) & (CONSTANT.flag_pump3_N == 1)):
        if(random.randint(1, 20) > 18): # kiểm tra điều kiện- nhớ phải xét khoảng, đây chưa xét khoảng
            CONSTANT.SubThread_pump3.start(1000) # bắt đầu đếm lui
            ControlDevice(5, 1)                 # Bật máy bơm
            CONSTANT.flag_pump3   = 1          
            CONSTANT.flag_pump3_N = 1
    elif((CONSTANT.flag_pump3 == 0) & (CONSTANT.flag_pump3_N == 0)):
        ControlDevice(5, 0)
        CONSTANT.TIME["pump3"]["minute"] = 0
        CONSTANT.TIME["pump3"]["second"]  = 10
        CONSTANT.flag_pump3 = 0  
        CONSTANT.flag_pump3_N = 1
    else:
        pass

def Thread_lamp1():
    if((CONSTANT.flag_lamp1 == 0) & (CONSTANT.flag_lamp1_N == 1)):
        if(random.randint(1, 20) > 18): # kiểm tra điều kiện- nhớ phải xét khoảng, đây chưa xét khoảng
            CONSTANT.SubThread_lamp1.start(1000) # bắt đầu đếm lui
            ControlDevice(2, 1)                 # Bật máy bơm
            CONSTANT.flag_lamp1   = 1          
            CONSTANT.flag_lamp1_N = 1
    elif((CONSTANT.flag_lamp1 == 0) & (CONSTANT.flag_lamp1_N == 0)):
        ControlDevice(2, 0)
        CONSTANT.TIME["lamp1"]["minute"]  = 0
        CONSTANT.TIME["lamp1"]["second"]  = 10
        CONSTANT.flag_lamp1_N = 1
        CONSTANT.flag_lamp1   = 0

    else:
        pass

def Thread_lamp2():
    if((CONSTANT.flag_lamp2 == 0) & (CONSTANT.flag_lamp2_N == 1)):
        if(random.randint(1, 20) > 18): # kiểm tra điều kiện- nhớ phải xét khoảng, đây chưa xét khoảng
            CONSTANT.SubThread_lamp2.start(1000) # bắt đầu đếm lui
            ControlDevice(4, 1)                 # Bật máy bơm
            CONSTANT.flag_lamp2  = 1          
            CONSTANT.flag_lamp2_N = 1
    elif((CONSTANT.flag_lamp2 == 0) & (CONSTANT.flag_lamp2_N == 0)):
        ControlDevice(4, 0)
        CONSTANT.TIME["lamp2"]["minute"]  = 0
        CONSTANT.TIME["lamp2"]["second"]  = 10
        CONSTANT.flag_lamp2   = 0  
        CONSTANT.flag_lamp2_N = 1
    else:
        pass

#---backup data --------------------------------------------------------------
def Synchronous():
    global client

    Windowns.backup_Synchronous(1)
    max_G00   = DB.find_pos_backup("backup_nongtrai_G00")
    max_G01   = DB.find_pos_backup("backup_nongtrai_G01")
    max_Relay = DB.find_pos_backup("backup_controller")

    print("Synchronous begin")

    Init_mqtt()

    # NongtraiG00
    for i in range(1, max_G00 + 1):

        if(DB.check_syn("backup_nongtrai_G00", i)==False): # phat hien ra la co data chua sync- vet tu day
            DB.update_data_backup_row("backup_nongtrai_G00", i, "ok")
            data = DB.get_data_backup_row("backup_nongtrai_G00", i)
            if(data!=[]):
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["id"]        =  data[0][3]
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["value"]     =  int(data[0][4])
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["RF_signal"] =  data[0][5]   
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["battery"]   =  data[0][6]    
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["time"]      =  data[0][7]
                CONSTANT.DATA_G00["NODE" + str(data[0][1])]["syn"]       =  data[0][8]

                if(i%13==0):
                    CONSTANT.DATA_G00["sub_id"] = "G00"
                    CONSTANT.DATA_G00["time"] = data[0][7]
                    print(json.dumps(CONSTANT.DATA_G00))
                    if(check_internet() == True): 
                        client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G00))
                    else:
                        Windowns.debugg("Lỗi kết nối", "Không có internet")
        else:
            pass

    # NongtraiG01
    for i in range(1, max_G01 + 1):
        if(DB.check_syn("backup_nongtrai_G01", i)==False): # phat hien ra la co data chua sync- vet tu day
            DB.update_data_backup_row("backup_nongtrai_G01", i, "ok")
            data = DB.get_data_backup_row("backup_nongtrai_G01", i)
            if(data!=[]):
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["id"]        =  data[0][3]
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["value"]     =  int(data[0][4])
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["RF_signal"] =  data[0][5]   
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["battery"]   =  data[0][6]    
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["time"]      =  data[0][7]
                CONSTANT.DATA_G01["NODE" + str(data[0][1])]["syn"]       =  data[0][8]
                if(i%13 == 0):
                    CONSTANT.DATA_G01["sub_id"] = "G01"
                    CONSTANT.DATA_G01["time"] = data[0][7]
                    print(json.dumps(CONSTANT.DATA_G01))        
                    if(check_internet() == True): 
                        client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G01))
                    else:
                        Windowns.debugg("Lỗi kết nối", "Không có internet")
        else:
            pass

    # Controller - RELAY : Do relay chỉ cập nhập trạng thái khi mất mạng, mà khi có mạng hàm init_mqtt() sẽ
    # lại get tất cả trạng thái relay lên rồi. Ở đây ta chỉ cập nhập sync thành "ok"
    for i in range(1, max_Relay + 1):
        if(DB.check_syn("backup_controller", i)==False): # phat hien ra la co data chua sync- vet tu day
            DB.update_data_backup_row("backup_controller", i, "ok")
            # data = DB.get_data_backup_row("backup_controller", i)
        else:
            pass
    
    Windowns.backup_Synchronous(2)
    
    CONSTANT.flag_backup = 0
    CONSTANT.flag_backup_N = 1  

def Backup():


    Windowns.backup_Synchronous(0)

    DB.creat_table("backup_nongtrai_G00")
    DB.creat_table("backup_nongtrai_G01")
    DB.creat_table("backup_controller")
    print("backup begin")


    CONSTANT.flag_backup = 1
    CONSTANT.flag_backup_N = 0  

#---end------------------------------------------------------------------------------------------------


# theard sẽ chạy background - backup data khi mất mạng
# không nên truy cập widgets and GUI từ một luồng khác ngoài luồng chính
class YouThread(QtCore.QThread): # inheritance
    global client

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    # 0 - 1 : start
    # 0 - 0 : running
    # 1 - 1 : pass
    # 1 - 0 : có vết backup
    def run(self): #  background task - chạy ngầm để gửu dữ liệu : this is non-daemon thread. if use daemon : either complete or killed when main thread exits.
        while(True): # note daemon sử dụng khi : you don’t mind if it doesn’t complete or left in between.
            if(check_internet() == False): # khi mat mang se backup
                if((CONSTANT.flag_backup == 0) & (CONSTANT.flag_backup_N == 1)): # danh dau khi mat mang
                    Windowns.display_internet(0)
                    Backup()
                else:
                    pass          
            else:   
                # khi có mạng sẽ đẩy lên server - ý tưởng một là gửu lên từng row, hai là gửu lên một 
                # message backup -  CONSTANT.DATAG00 or  CONSTANT.DATAG00

                if((CONSTANT.flag_backup == 1) & (CONSTANT.flag_backup_N == 0)):
                    Windowns.display_internet(1)
                    Synchronous()
                else:
                    pass

thread = YouThread() 
thread.start()


def Init_Thread():
    CONSTANT.Thread_pump1.timeout.connect(Thread_pump1)
    CONSTANT.Thread_pump1.start(100)
    CONSTANT.SubThread_pump1.timeout.connect(Windowns.countdown_pump1)

    CONSTANT.Thread_pump2.timeout.connect(Thread_pump2)
    CONSTANT.Thread_pump2.start(100)
    CONSTANT.SubThread_pump2.timeout.connect(Windowns.countdown_pump2)

    CONSTANT.Thread_pump3.timeout.connect(Thread_pump3)
    CONSTANT.Thread_pump3.start(100)
    CONSTANT.SubThread_pump3.timeout.connect(Windowns.countdown_pump3)

    CONSTANT.Thread_lamp1.timeout.connect(Thread_lamp1)
    CONSTANT.Thread_lamp1.start(100)
    CONSTANT.SubThread_lamp1.timeout.connect(Windowns.countdown_lamp1)

    CONSTANT.Thread_lamp2.timeout.connect(Thread_lamp2)
    CONSTANT.Thread_lamp2.start(100)
    CONSTANT.SubThread_lamp2.timeout.connect(Windowns.countdown_lamp2)

#---end------------------------------------------------------------------------------------------------

if __name__ == "__main__": # điểm bắt đầu của một chương trình
    global GW_Blue
    # requirePort()
    # Init_UI()
    # Init_Lora()
    Init_Button()
    Init_Thread()
    Init_mqtt()


    '''
    + GateWay red : 1s bắn data lên một lần
    + GateWay Blue : 2p truy xuất data một lần
    Lúc updatate GateWay blue cũng là lúc bắn tất data của các nông trại lên.
    '''   
    read = QTimer()
    read.timeout.connect(Update_GatewayRed)
    read.start(1000)  

    blue = QTimer()
    blue.timeout.connect(Update_GatewayBlue)
    blue.start(1000)   
# end-mqtt-------------------------------------

    Windowns.app.show()
    sys.exit(Windowns.App.exec())
