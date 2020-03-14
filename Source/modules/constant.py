from PyQt5.QtCore import QTimer, QTime, QThread, pyqtSignal, QDate, Qt
import random


# countdown

global TIME,DEVICE

TIME = {
    "pump1" : {"second":10, "minute":0},
    "pump2" : {"second":10, "minute":0},
    "pump3" : {"second":10, "minute":0},
    "lamp1" : {"second":10, "minute":0},
    "lamp2" : {"second":10, "minute":0},
} 

global SubThread_pump1, SubThread_pump1, SubThread_pump3
global SubThread_lamp1, SubThread_lamp2

global Thread_pump1, Thread_pump1, Thread_pump3
global Thread_lamp1, Thread_lamp2

SubThread_pump1 = QTimer()
SubThread_pump2 = QTimer()
SubThread_pump3 = QTimer()
SubThread_lamp1 = QTimer()
SubThread_lamp2 = QTimer()

Thread_pump1 = QTimer()
Thread_pump2 = QTimer()
Thread_pump3 = QTimer()
Thread_lamp1 = QTimer()
Thread_lamp2 = QTimer()

global flag_pump1, flag_pump2, flag_pump3
global flag_lamp1, flag_lamp2

flag_pump1 = 0
flag_pump2 = 0
flag_pump3 = 0

flag_lamp1 = 0
flag_lamp2 = 0

global flag_pump1_N, flag_pump2_N, flag_pump3_N
global flag_lamp1_N, flag_lamp2_N

flag_pump1_N = 1
flag_pump2_N = 1
flag_pump3_N = 1

flag_lamp1_N = 1
flag_lamp2_N = 1

# global test
# test = 5
# Pump1_second = 5
#--------------------------------------------------------------------------------------------------
global posBackup_G00, posBackup_G01 # vi tri STT trong data base khi mat mang
global flag_backup # co backup
global flag_backup_N

posBackup_G00 = 1
posBackup_G01 = 1
flag_backup   = 0
flag_backup_N = 1

global DATA_G00, DATA_G01, DATA_G02


DATA_G00 = {
    "sub_id": "G00",
    "time"  : "",
    "NODE1":  {"name": "soil_moistrure1", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE2":  {"name": "soil_moistrure2", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE3":  {"name": "soil_moistrure3", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE4":  {"name": "soil_moistrure4", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE5":  {"name": "soil_moistrure5", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE6":  {"name": "soil_moistrure6", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE7":  {"name": "soil_moistrure7", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE8":  {"name": "soil_moistrure8", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE9":  {"name": "soil_moistrure9", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE10": {"name": "soil_moistrure10", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},

    "NODE21": {"name": "humidity1",         "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE23": {"name": "light1",            "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE25": {"name": "temperature1",      "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE32": {"name": "ph1",               "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},

    "NODE27": {"name": "relay1", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"}
}

DATA_G01 = {
    "sub_id":"G01",    
    "time"  : "",
    "NODE11": {"name": "soil_moistrure11", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE12": {"name": "soil_moistrure12", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE13": {"name": "soil_moistrure13", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE14": {"name": "soil_moistrure14", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE15": {"name": "soil_moistrure15", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE16": {"name": "soil_moistrure16", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE17": {"name": "soil_moistrure17", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE18": {"name": "soil_moistrure18", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE19": {"name": "soil_moistrure19", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE20": {"name": "soil_moistrure20", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},

    "NODE22": {"name": "humidity2",         "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE24": {"name": "light2",            "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE26": {"name": "temperature2",      "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE33": {"name": "ph2",               "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"}
}

DATA_G02 = {
    "sub_id": "G02",
    "time"  :  "",
    "NODE27": {"name": "relay1", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"},
    "NODE28": {"name": "relay2", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"},
    "NODE29": {"name": "relay3", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"},
    "NODE30": {"name": "relay4", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"},
    "NODE31": {"name": "relay5", "id":0,  "value" : 0, "battery": 99, "RF_signal":"", "time":"", "syn":"error"}
}

SENSOR = {
    "soil_moistrure" : 1,
    "humidity"       : 2,
    "light"          : 3,
    "relay"          : 4
}

BATTERY = {
    '10': "10 %",
    '30': "30 %",
    '60': "60 %",
    '99': "Full Battery"
}
RSSI = {
    "4": "perfect",
    "3": "good",
    "2": "medium",
    "1": "bad"
}


L = {
    'min': 30,
    'max': 70
}
PH = {
    'min': 4,
    'max': 7
}
T = {
    'min': 20,
    'max': 30
}
H = {
    'min': 75,
    'max': 80
}
SM = {
    'min': 55,
    'max': 60
} 

TIME_OUT = 4000

# name GW default - tên này có thể thay đổi nếu port thay đổi
GW_Blue_NAME  = "COM3"        # GateWay(Xanh) : thu dữ liệu của bọn đại việt và điều khiển máy bơm
GW_Red_NAME   = "COM4"         # GateWay(Đỏ) : thu dữ liệu từ cảm biến của mình

