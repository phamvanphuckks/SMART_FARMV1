# Controller - RELAY - truy xuất từng row trong bảng controller - gửu từng row lên server
for i in range(1, max_Relay + 1):
    if(DB.check_syn("backup_controller", i)==False): # phat hien ra la co data chua sync- vet tu day
        DB.update_data_backup_row("backup_controller", i, "ok")
        # data = DB.get_data_backup_row("backup_controller", i)
    else:
        pass
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["id"]        =  data[0][3]
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]     =  int(data[0][4])
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"] =  data[0][5]   
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["battery"]   =  data[0][6]    
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["time"]      =  data[0][7]
    CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["syn"]       =  data[0][8]

    if(data[0][1] == 27 ):
        payload_data = {
            'sub_id': "G02",
            'time'  : CONSTANT.DATA_RELAY["time"],
            "relay_1": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]),
                'battery': 100
            }
        }
    elif(data[0][1] == 28 ):
        payload_data = {
            'sub_id': "G02",
            'time'  : CONSTANT.DATA_RELAY["time"],
            "relay_2": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]),
                'battery': 100
            }
        }
    elif(data[0][1] == 29 ):
        payload_data = {
            'sub_id': "G02",
            'time'  : CONSTANT.DATA_RELAY["time"],
            "relay_3": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]),
                'battery': 100
            }
        }
    elif(data[0][1] == 30 ):
        payload_data = {
            'sub_id': "G02",
            'time'  : CONSTANT.DATA_RELAY["time"],
            "relay_4": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]),
                'battery': 100
            }
        }
    elif(data[0][1] == 31 ):
        payload_data = {
            'sub_id': "G02",
            'time'  : CONSTANT.DATA_RELAY["time"],
            "relay_5": {
                "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["RF_signal"],
                'value': str(CONSTANT.DATA_RELAY["NODE" + str(data[0][1])]["value"]),
                'battery': 100
            }
        }
    else: 
        pass
    
    print(json.dumps(payload_data))

    if(check_internet() == True): 
        client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_data))
    else:
        pass


    