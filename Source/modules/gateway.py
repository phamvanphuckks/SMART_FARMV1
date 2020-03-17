#Serial
import minimalmodbus
import serial
import serial.tools.list_ports

# library programer development
import constant as CONSTANT
import math

'''
    đọc dữ liệu từ gateway(Xanh) : sử dụng thư viện minimalmodbus
'''

class Gateway():
    # init MOSBUS RTU
    def __init__(self, port_name, id_device=1):
        self.instrument = minimalmodbus.Instrument(port_name, id_device) 
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.05
        self.instrument.mode = minimalmodbus.MODE_RTU  # seconds
        self.initialize()

    def initialize(self): # khi mình khởi động tắt tất cả thiết bị và cập nhập trạng thái off trên app
        # for i in range(27, 31):
            # self.control_RL(i, 1, 0)
        self.control_RL(5, 1, 0)
        pass

    # convert data to int 16
    def convert_data(self, data):
        value = ''
        for i in range(0, len(data)):
            value += hex(data[i])
        value = value.replace('0x', '')
        value = '0x'+value
        return int(value, 16)

# registeraddress- Search in file Modbus memmap of WR433 V1.9 : C:\Users\Pham Van Phuc\Desktop\SFARM-master
    # get number of node of Wriless 
    def get_num_of_node(self):
        data = self.instrument.read_registers(
            registeraddress=272, number_of_registers=2, functioncode=3)
        value = self.convert_data(data)
        return value

    # read mosbus adr
    def get_modbus_adr(self):
        data = self.instrument.read_registers(
            registeraddress=256, number_of_registers=1, functioncode=3)
        value = self.convert_data(data)
        return value

    # read mosbus baudrate
    def get_modbus_baudrate(self):
        data = self.instrument.read_registers(
            registeraddress=257, number_of_registers=1, functioncode=3)
        value = self.convert_data(data)
        return value

    # read mosbus parity
    def get_modbus_parity(self):
        data = self.instrument.read_registers(
            registeraddress=258, number_of_registers=1, functioncode=3)
        value = self.convert_data(data)
        return value
# end file - Modbus memmap of WR433 V1.9

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


# get id of node - do họ đặt
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
        pos : thứ tự các node mình setup
    '''
    def get_node_id(self, pos=1, id=1):        # Read ID of device  !! OK check xong
        data = self.instrument.read_registers(
                registeraddress=(271 + (pos)*2), number_of_registers=2, functioncode=3)
        value = self.convert_data(data)
        return str(value)


# registeraddress : Template_WR433_V1.6:SFARM-master\Daviteq Modbus Configuration Tool Version 1.2
    # get main parmeter
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_main_parameter(self, pos=1, id=1):  # read Data   !! OK check xong
        if(id == 1):
            data = self.instrument.read_registers(registeraddress=(41217 + (pos-1)*256), number_of_registers=1, functioncode=3)  
            return round((data[0]/10), 2) 
        elif(id == 2):
            data = self.instrument.read_float(registeraddress=(41217 + (pos-1)*256), number_of_registers=2, functioncode=3)
            return round(data, 2)
        elif(id == 3):
            data = self.instrument.read_float(registeraddress=(41217 + (pos-1)*256), number_of_registers=2, functioncode=3)
            return round(data, 2)
        else:
            pass


# address in file memap of WS433-RL - C:\Users\Pham Van Phuc\Desktop\SFARM-master
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_second_parameter(self, pos=1, id=1):     # get second parameter     !! OK check xong
        data = self.instrument.read_float(registeraddress=(41220 + ((pos-1)*256)), number_of_registers=2, functioncode=3)
        return round(data, 2)
    
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_battery(self, pos=1, id=1):       # get Batterry    !! OK check xong
        data = self.instrument.read_register(41216 + ((pos-1)*256))
        return data         



    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_status_node(self, pos=1, id=1):     #kiểm tra xem node là node gì VD : 11 - độ ẩm đất  !! OK check xong
        data = self.instrument.read_register((41219 + (pos-1)*256))
        return CONSTANT.STATUS_NODE[str(data)]

    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    # 68 : node1,2    69 : node3,4 ...
    def get_RFsignal(self, pos=1, id=1):     # get RF signal            !! OK check xong

        data = self.instrument.read_registers(registeraddress=(67 + math.ceil(pos/2)), number_of_registers=1, functioncode=3)
        data = hex(data[0]).replace('0x', '')
        hi_byte = data[0]
        lo_byte = data[len(data) - 1]

        if ((pos%2) != 0): # 1,3,5,7,9 ... hi_byte
            return CONSTANT.RSSI[str(hi_byte)]
        else:
            return CONSTANT.RSSI[str(lo_byte)]

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

    '''
        5 RELAY -  1 RELAY 2 chanel
        pos : vị trí của NODE RELAY trên hệ thống: thứ tự mình add vào trong gateway
        chanel : chanel 1, 2
        status : 1 - ON ,0 - OFF 
    '''
#test realy--------------------------------------------------------------------------------------------
    #   pos : thứ tự relay trong gateway
    #   chanel : từng chân relay trong module relay
    def control_RL(self, pos, chanel, status): # control realy
        try:
            self.instrument.write_register(registeraddress=(2000 + (pos-1)*8 +(chanel-1)), value=status,
                                                number_of_decimals=0, functioncode=16, signed=False)
        except :
            pass
           
    # get status of relay - phản hồi trạng thái hiện tại của relay
    def get_status_RL(self, pos, chanel):
        try:
            data = self.instrument.read_registers(
                    registeraddress=(2000 + (pos-1)*8 +(chanel-1)), number_of_registers=1, functioncode=3)
            return data[0]	
        except :
            pass


#---------------------------------------------------------------------------------------------------------