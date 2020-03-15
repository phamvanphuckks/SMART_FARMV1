import sqlite3    as sql
import constant   as CONSTANT
import time

from threading import Lock
from datetime  import datetime

lock = Lock()


class DataBase():
    def __init__(self):
        self.path = "databases\\DB_OF_SFARM.db"
        self.con  = sql.connect(self.path, check_same_thread=False)
        self.cur  = self.con.cursor()

    def creaat_table(self, place):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                node        INTEGER     NULL,
                name        TEXT        NULL,
                id          TEXT        NULL,
                value       TEXT        NULL,
                RF_signal   TEXT        NULL,
                battery     TEXT        NULL,
                time        TEXT        NULL, 
                syn         TEXT        NULL)
                '''
            self.cur.execute(cmd)
            lock.release()
            self.con.commit()
        # self.con.close()

    def insert_data(self, place, syn):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                node        INTEGER     NULL,
                name        TEXT        NULL,
                id          TEXT        NULL,
                value       TEXT        NULL,
                RF_signal   TEXT        NULL,
                battery     TEXT        NULL,
                time        TEXT        NULL, 
                syn         TEXT        NULL)
                '''
            self.cur.execute(cmd)

            cmd = "INSERT INTO " + table_name + " (node,name,id,data,signal,pin,time,syn) VALUES(?,?,?,?,?,?,?,?)"
            # for i in range(1, 32):
            #     self.cur.execute(cmd, ( str(CONSTANT.DATA["NODE"+str(i)]["node"]), str(CONSTANT.DATA["NODE"+str(i)]["name"]), 
            #     str(CONSTANT.DATA["NODE"+str(i)]["id"]), str(CONSTANT.DATA["NODE"+str(i)]["value"]), str(CONSTANT.DATA["NODE"+str(i)]["battery"]),str(CONSTANT.DATA["NODE"+str(i)]["RF_signal"]), 
            #     str(CONSTANT.DATA["NODE"+str(i)]["time"]),  syn)
            #     )
            lock.release()
            self.con.commit()
        # self.con.close()

    def insert_data_row(self, place, node, id, name, value,  RF_signal, battery, time, syn):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "CREATE TABLE IF NOT EXISTS " + table_name + '''(
                stt         INTEGER     PRIMARY KEY AUTOINCREMENT,
                node        INTEGER     NULL,
                name        TEXT        NULL,
                id          TEXT        NULL,
                value       TEXT        NULL,
                RF_signal   TEXT        NULL,
                battery     TEXT        NULL,
                time        TEXT        NULL, 
                syn         TEXT        NULL)
                '''
            self.cur.execute(cmd)

            cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
 
            self.cur.execute(cmd, ( str(node), str(name),str(id), str(value), str(RF_signal), str(battery), str(time),  str(syn)))
            lock.release()
            self.con.commit()
        # self.con.close()

    def update_data(self, table_name, pos, status):
        lock.acquire(True)
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "UPDATE %s" %table + " SET syn='%s'"%status + " WHERE stt=" + str(pos)
            self.cur.execute(cmd)
            lock.release()
            self.con.commit()
        # self.con.close()

    def remove_data(self, table_name, pos):
        lock.acquire(True)
        with self.con:
            cmd = "DELETE from %s" %table_name+" where stt="+str(pos)
            self.cur.execute(cmd)
            lock.release()
            self.con.commit()
        self.con.close()

    def find_pos(self, table_name):
        lock.acquire(True)
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "SELECT stt FROM %s" %table + " WHERE stt=(SELECT MAX(stt)  FROM %s" %table + ")"
            self.cur.execute(cmd)
            lock.release()
            self.con.commit()
            data = self.cur.fetchall()
        # self.con.close()
        if (data == []):   return 1
        else:   return   data[0][0]

    # Đặt vấn đề với querry và getdata : với mảng có dữ liệu cực kì lớn thì sao thì lệnh fetchall sẽ rất lớn theo vượt quá buffer
    # vì vậy phải đọc từng ít một
    def get_data_row(self, table_name, pos):

        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        lock.acquire(True)
        with self.con:
            cmd = "SELECT * FROM %s" %table + " WHERE stt="+ str(pos)
            self.cur.execute(cmd)
            lock.release()
            self.con.commit()
            data = self.cur.fetchall()
        return data

    # Query với n cột trong bảng của ngày hôm đó
    def Query(self, table_name, n): # sợ đọc load vào 1 mảng bị tràn mình sẽ chia làm hai sử dụng kiểu ringbuffer - chưa viết đc
        lock.acquire(True)
        datas = []
        data  = []
        with self.con:
            cmd = "SELECT * FROM %s" %table_name
            self.cur.execute(cmd)
            lock.release()
            data = self.cur.fetchall()
        # self.con.close()
        
        for i in range(len(data)-n,len(data)):
            datas.append(data[i])
        return datas

    # Xóa tất cả các table trong database;
    def get_table_name(self):
        lock.acquire(True)
        with self.con:
            tables = list(self.cur.execute(
                    "select name from sqlite_master where type is 'table' "))
            lock.release()
        return tables

    def Delete_all_tb(self):
        lock.acquire(True)
        with self.con:
            tables = list(self.cur.execute(
                "select name from sqlite_master where type is 'table'"))
            for i in tables :
                if(i != "('sqlite_sequence',)"):
                    cmd = ';'.join(["DROP TABLE IF EXISTS %s" % i])
                else:
                    pass
            self.cur.executescript(cmd)
            self.con.commit()
            lock.release()
        




