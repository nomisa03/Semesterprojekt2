import sqlite3
from datetime import datetime
import serial
from serial import Serial
splitc = ";"
incomming = []

#['M:1;S:48:T:31.20:M:1;S:49:T:1.20:M:1;\r\n']

now = datetime.now() #For making a timestamp of current time

conn = sqlite3.connect('database.db') #connet to local database in file system
cur = conn.cursor() #cursoer for looking in database

#data = [
#(now), ("Rum 1"), (28) ,("Person i rummet"), ("Giver varm luft")
#]
#Example of a data frame from master arduino

#Setting up our serial port to read the system
ser = serial.Serial(
    port='COM4',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

# Aktivitet høj = 1, lav = 0. Statusrum -1 = afgiver varme, 0 = neutral, 1 = får varme
cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Timestamp, Temperatur, Aktivitet)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Timestamp, Temperatur, Aktivitet)")

def Readsystem(incomming):
    rooms = 2
    #incomming.decode(encoding='UTF-8')
    incomming.split(";") # so list looks like this incommin = [Rum1; 28 , ("1") : Rum2, 28, ("0")]
    #string_count = len(incomming)
    rum1 = incomming[1].split(splitc)
    print(rum1)
    #rum1.pop(0)
    #rum1.pop(1)
    #rum1.pop(2)
    #rum1.pop(4)
    rum1.insert(0, now)
    rum2 = incomming[2].split(splitc)
    #rum2.pop(0)
    #rum2.pop(1)
    #rum2.pop(2)
    #rum2.pop(4)
    rum2.insert(0, now)
    if len(rum1) == 4:
        try:
            cur.execute("INSERT INTO Rum1 VALUES(? , ? , ?)",rum1)
            print("Data succsesfu in table Rum 1")
            conn.commit
        except:
            print("DataError")
            main()
    
    if len(rum2) == 4:
        try:
            cur.execute("INSERT INTO Rum2 VALUES(? , ? , ?)",rum2)
            print("Data succsesfu in table Rum 2")
            conn.commit
            main()
        except:
            print("DataError.")
            main()



def main():
    #while True:
        #ser.open()
        #bytesToRead = ser.in_waiting
        #print(bytesToRead)
        #if (bytesToRead > 3):
            #res = ser.read(bytesToRead)
            #print(res)
            #incomming = res.decode("utf-8")
            #print(incomming)
            #Readsystem(incomming)
            #ser.reset_input_buffer()
            #incomming = port.readline()
            #print(incomming)



    while True:
        #ser.open()
        line = ser.in_waiting
        print(line)
        if line > 37:
            bytestoread = ser.read(line)
            incomming.append(bytestoread.decode("UTF-8"))
            #incomming = ("Master brude være ligeglade" ";" "22"":""1"":""-1" ";" "18"":""0 "":""0" )
            print(incomming)
            Readsystem(incomming)
            #ser.close()


if __name__ == "__main__":
    main()
