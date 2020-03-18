#Serial
import serial.tools.list_ports
import serial

from datetime  import datetime   
import constant  as CONSTANT

# file này giao tiếp với GateWay(Đỏ) : 

class Gateway1():
    def __init__(self, port_name, baudrate, timeout): #khởi tạo serial
        self.ser            = serial.Serial()
        self.ser.port       = str(port_name)
        self.ser.baudrate   = baudrate
        self.ser.timeout    = timeout

        self.open_COM()

    def open_COM(self): # mở cổng COM
        if (self.ser.is_open == False):
            self.ser.open()

    def write_data(self, data): # ghi dữ liệu từ máy tính xuống GateWay(Đỏ)
        self.ser.write(data.encode('utf-8'))
    #    self.ser.flush()

    def read_data(self): # đọc tất cả các dòng
        return self.ser.readlines()

    def load_data(self):
        try:
            data = self.read_data() # đọc dữ liệu từ con đỏ, con đỏ có dữ liệu sau đó đọc cảm biến  daviteq  rồi gửu lên
            print("data_raw")
            print(data)
            if(len(data) != 0):
                for i in range(0, len(data)):
                    data[i] = data[i].decode('utf-8') # giải mãi hex sang string
                Str  = data[0]           # Str dòng thứ nhất chứa thống LEN, vv...
                Str1 = data[1]           # Str1 chứa giá trị nhận

                now = datetime.now()
                timestamp = int(datetime.timestamp(now))
                now = datetime.fromtimestamp(timestamp)

                payload = {
                    'LEN': Str[Str.find('LEN:') + len("LEN:"):Str.find(',', Str.find('LEN:') + len("LEN:"))],
                    'RSSI': Str[Str.find('RSSI:') + len("RSSI:"):Str.find(',', Str.find('RSSI:') + len("RSSI:"))],
                    'SNR': Str[Str.find("SNR:") + len("SNR:"):len(Str) - 2],
                    'DATA': bytes.fromhex(Str1[Str1.find("\"") +
                                            1: Str1.find("\"", 1 + int(Str1.find("\"")))]).decode('utf-8'),
                    'TIME': now}
                print("payload_raw")
                print(payload)

                # trước thì gái trị cảm biến gửu lên theo payload['DATA'] =  G00_độ ẩm đất_nhiệt độ_ánh sáng_ .... 
                # tách data thôi - có thể bỏ or không Data = payload['DATA'].split('_') 
                # ở đây chưa bỏ
                Data = payload['DATA'].split('_') 

                print("Data-split")
                print(Data)
                
                if (int(payload['RSSI'])   >= -54 and int(payload['RSSI']) <= 0):
                    signal = "Perfect"
                elif (int(payload['RSSI']) >= -69 and int(payload['RSSI']) <= -55):
                    signal = "Good"
                elif (int(payload['RSSI']) >= -79 and int(payload['RSSI']) <= -70):
                    signal = "Medium"
                elif (int(payload['RSSI']) >= -100 and int(payload['RSSI']) <= -80):
                    signal = "Bad"
                else:
                    signal = "Worse"

                # Data[0] tên của thiết bị
                if (Data[0] == "G00"):
                    CONSTANT.DATA_G00["NODE32"]["RF_signal"]   = signal 
                    CONSTANT.DATA_G00["NODE32"]["value"]       = Data[1]
                    CONSTANT.DATA_G00["NODE32"]["battery"]     = int((float(Data[2])-2.8)*100/(3.3-2.8)) # % pin 
                    CONSTANT.DATA_G00["NODE32"]["time"]        = now
                    CONSTANT.DATA_G00["NODE32"]["syn"]         = "ok"
                elif (Data[0] == "G01"):
                    CONSTANT.DATA_G01["NODE33"]["RF_signal"]   = signal 
                    CONSTANT.DATA_G01["NODE33"]["value"]       = Data[1]  
                    CONSTANT.DATA_G01["NODE33"]["battery"]     = int((float(Data[2])-2.8)*100/(3.3-2.8))
                    CONSTANT.DATA_G01["NODE33"]["time"]        =   now
                    CONSTANT.DATA_G01["NODE33"]["time"]        =   "ok"
                else:
                    return False
                
                return True
            else:
                return False
        except:
            pass
