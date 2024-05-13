import sqlite3
from datetime import datetime
#import serial
import time
t = 1 #time to sleep = 1 secs
dt = datetime.now()

incomming = [] #creating the list for the data to be in

#['M:1;S:48:T:31.20:M:1;S:49:T:1.20:M:1;\r\n']e

conn = sqlite3.connect('database.db') #connet to local database in file system
cur = conn.cursor() #cursoer for looking in database

#Setting up our serial port to read the system
#ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

# Aktivitet høj = 1, lav = 0. Statusrum -1 = afgiver varme, 0 = neutral, 1 = får varme
cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Timestamp, Temperatur, Aktivitet)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Timestamp, Temperatur, Aktivitet)")

def Readsystem(incomming):
    string_to_split = incomming[0]
    # Splitting the string by ";"
    split_list = string_to_split.split(";")

    print(split_list)

    data_to_split = split_list[0]
    M1 = data_to_split.split(":")
    M1.pop(0)
    print(M1)
    if M1[0] == "2":
        sendtimestamp()
    else:
        data_to_split1 = split_list[1]
        rum1 = data_to_split1.split(":")
        rum1.pop(0)
        rum1.pop(0)
        rum1.pop(0)
        rum1.pop(1)
        rum1.insert(0,datetime.now())
        print(rum1)

        data_to_split2 = split_list[2]
        rum2 = data_to_split2.split(":")
        rum2.pop(0)
        rum2.pop(0)
        rum2.pop(0)
        rum2.pop(1)
        rum2.insert(0,datetime.now())
        print(rum2)

        try:
            conn.execute("INSERT INTO Rum1 VALUES(? , ? , ?)",rum1)
            print("Data succsesfully in table Rum 1")
            conn.commit()
        except:
            print("DataError")
            main()


        try:
            conn.execute("INSERT INTO Rum2 VALUES(? , ? , ?)",rum2)
            print("Data succsesfully in table Rum 2")
            conn.commit()
            main()
        except:
            print("DataError.")
            main()



def main():
    while True:
        time.sleep(t)
        #ser.open()
        #line = ser.in_waiting
        incomming = ['M:1;S:48:T:31.20:M:1;S:49:T:1.20:M:1;\r\n']
        Readsystem(incomming)
        print(incomming)
        #print(line)
        #if line > 40:
            #incomming.append(bytestoread.decode("UTF-8"))
            #print(incomming)
            #Readsystem(incomming)
            #ser.close()



def sendtimestamp():
    mystr = ""
    mystr += hex(dt.year)
    mystr += hex(dt.month)
    mystr += hex(dt.day)
    mystr += hex(dt.hour)
    mystr += hex(dt.minute)
    mystr += hex(dt.second)
    mystr += "\r\n"
    print(mystr)
    # ser.open()
    # ser.write(mystr)
    # ser.close()
    main()

if __name__ == "__main__":
    main()
