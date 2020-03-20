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

        self.pathbk = "databases\\DBBK_OF_SFARM.db"
        self.conbk  = sql.connect(self.pathbk, check_same_thread=False)
        self.curbk  = self.conbk.cursor()

    def creat_table(self, place):
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
            self.curbk.execute(cmd)
        lock.release()

    def insert_data_nongtraiG00(self, place, syn):
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
            for i in range(1, 15):
                if(i == 11): i = 21
                elif(i == 12): i = 23
                elif(i == 13): i = 25
                elif(i == 14): i = 32

                self.cur.execute(cmd, ( str(CONSTANT.DATA_G00["NODE"+str(i)]["node"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["name"]), 
                str(CONSTANT.DATA_G00["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["value"]), 
                str(CONSTANT.DATA_G00["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["battery"]),
                str(CONSTANT.DATA_G00["NODE"+str(i)]["time"]),  syn)
                
            )
        lock.release()

    def insert_data_nongtraiG01(self, place, syn):
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
            for i in range(11, 25):
                if(i == 21): i = 22
                elif(i == 22): i = 24
                elif(i == 23): i = 26
                elif(i == 24): i = 33

                self.cur.execute(cmd, (str(CONSTANT.DATA_G01["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G01["NODE"+str(i)]["name"]), 
                str(CONSTANT.DATA_G01["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["value"]), 
                str(CONSTANT.DATA_G01["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["battery"]),
                str(CONSTANT.DATA_G01["NODE"+str(i)]["time"]),  syn)
            )
        lock.release()

    def insert_data_backup_nongtraiG00(self, place, syn):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.conbk:
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
            self.curbk.execute(cmd)

            cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
            for i in range(1, 15):
                if(i == 11): i = 21
                elif(i == 12): i = 23
                elif(i == 13): i = 25
                elif(i == 14): i = 32
                self.curbk.execute(cmd, (str(CONSTANT.DATA_G00["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G00["NODE"+str(i)]["name"]), 
                str(CONSTANT.DATA_G00["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["value"]), 
                str(CONSTANT.DATA_G00["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G00["NODE"+str(i)]["battery"]),
                str(CONSTANT.DATA_G00["NODE"+str(i)]["time"]),  syn)
            )
        lock.release()

    def insert_data_backup_nongtraiG01(self, place, syn):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.conbk:
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
            self.curbk.execute(cmd)

            cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
            for i in range(11, 25):
                if(i == 21): i = 22
                elif(i == 22): i = 24
                elif(i == 23): i = 26
                elif(i == 24): i = 33
                self.curbk.execute(cmd, (str(CONSTANT.DATA_G01["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G01["NODE"+str(i)]["name"]), 
                str(CONSTANT.DATA_G01["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["value"]), 
                str(CONSTANT.DATA_G01["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["battery"]),
                str(CONSTANT.DATA_G01["NODE"+str(i)]["time"]),  syn)
            )
        lock.release()

    def insert_data_Relay(self, place, syn):
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
                for i in range(27, 32):
                    self.cur.execute(cmd, (str(CONSTANT.DATA_G01["NODE"+str(i)]["node"]),str(CONSTANT.DATA_G01["NODE"+str(i)]["name"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["id"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["value"]), 
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["RF_signal"]), str(CONSTANT.DATA_G01["NODE"+str(i)]["battery"]),
                    str(CONSTANT.DATA_G01["NODE"+str(i)]["time"]),  syn)
                )
            lock.release()

    def insert_data_row(self, place, node, name, id, value,  RF_signal, battery, time, syn):
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
 
            self.cur.execute(cmd, (str(node), str(name),str(id), str(value), str(RF_signal), str(battery), str(time),  str(syn)))
        lock.release()

    def insert_data_backup_row(self, place, node, name, id, value,  RF_signal, battery, time, syn):
        lock.acquire(True)
        table_name = "data_of_"+ str(place) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.conbk:
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
            self.curbk.execute(cmd)

            cmd = "INSERT INTO " + table_name + " (node,name,id,value,RF_signal,battery,time,syn) VALUES(?,?,?,?,?,?,?,?)"
 
            self.curbk.execute(cmd, (str(node), str(name),str(id), str(value), str(RF_signal), str(battery), str(time),  str(syn)))
        lock.release()

    def update_data_backup_row(self, table_name, pos, status):
        lock.acquire(True)
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.conbk:
            cmd = "UPDATE %s" %table + " SET syn='%s'"%status + " WHERE stt=" + str(pos)
            self.curbk.execute(cmd)
        lock.release()

    def update_data_row(self, table_name, pos, status):
        lock.acquire(True)
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "UPDATE %s" %table + " SET syn='%s'"%status + " WHERE stt=" + str(pos)
            self.cur.execute(cmd)
            lock.release()

    def check_syn(self, table_name, stt):
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        lock.acquire(True)
        with self.conbk:
            cmd = "SELECT * FROM %s" %table + " WHERE stt="+ str(stt)
            self.curbk.execute(cmd)
            data = self.curbk.fetchall()
        lock.release()
        if(data != []): # nêu mà giá trị đấy tồn tại thì mới đọc
            if(data[0][8] == "ok"):
                return True
            else:
                return False

    def remove_data(self, table_name, pos):
        lock.acquire(True)
        with self.con:
            cmd = "DELETE from %s" %table_name+" where stt="+str(pos)
            self.cur.execute(cmd)
            lock.release()

    def find_pos_backup(self, table_name):
        lock.acquire(True)
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")

        with self.conbk:
            cmd = "SELECT stt FROM %s" %table + " WHERE stt=(SELECT MAX(stt)  FROM %s" %table + ")"
            self.curbk.execute(cmd)
            data = self.curbk.fetchall()
        lock.release()
        if (data == []):   return 1
        else:   return   data[0][0]

    def get_data_backup_row(self, table_name, pos):

        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        lock.acquire(True)
        with self.conbk:
            cmd = "SELECT * FROM %s" %table + " WHERE stt="+ str(pos)
            self.curbk.execute(cmd)
            data = self.curbk.fetchall()
        lock.release()
        return data

    # Query với n cột trong bảng của ngày hôm đó
    def get_data_n_row(self, table_name, n): # sợ đọc load vào 1 mảng bị tràn mình sẽ chia làm hai sử dụng kiểu ringbuffer - chưa viết đc
        lock.acquire(True)
        datas = []
        data  = []
        table = "data_of_"+ str(table_name) + "_"+ datetime.now().strftime("%d_%m_%Y")
        with self.con:
            cmd = "SELECT * FROM %s" %table
            self.cur.execute(cmd)
            data = self.cur.fetchall()
        lock.release()
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
        




