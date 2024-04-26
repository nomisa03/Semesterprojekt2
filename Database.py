import sqlite3
from datetime import datetime
import matplotlib as plt
from matplotlib import gridspec

now = datetime.now()

import serial

ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)


ser.close()

conn = sqlite3.connect('database.db')

cur = conn.cursor()

#data = [
#(now), ("Rum 1"), (28) ,("Person i rummet"), ("Giver varm luft")
#]

cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Timestamp, Room, Temperatur, Aktvitet, Statusrum)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Timestamp, Room, Temperatur, Aktvitet, Statusrum)")

def Readsystem(incomming):
    incomming.split(":",) # so list looks like this incommin = [Rum1, 28 , ("Person i rummet") : Rum2, 28, ("Tomt")]
    cur.execute("INSERT INTO Rum1 VALUES(? , ? , ? , ? , ?)",now, incomming[0])
    print("Data succsesfu in table Rum 1")
    conn.commit
    if len(incomming) == 2():
        try:
            cur.execute("INSERT INTO Rum2 VALUES(? , ? , ? , ? , ?)",now, incomming[1])
            print("Data succsesfu in table Rum 2")
            conn.commit
        else:
            return 0



while True:
    for line in ser.read():
        incomming = str(count) + str(': ') + chr(line)
        print(incomming)
        Readsystem(incomming)
        count = count+1


#def makegraph()
    #cur.execute(Read)
    #read = grahp
    #Matplotlib
    #Send til GUI
    #readdata()
    #return graph
