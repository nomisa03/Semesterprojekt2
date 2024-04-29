import sqlite3
from datetime import datetime
import matplotlib as plt
from matplotlib import gridspec
import serial

now = datetime.now() #For making a timestamp of current time

conn = sqlite3.connect('database.db') #connet to local database in file system
cur = conn.cursor() #cursoer for looking in database

#data = [
#(now), ("Rum 1"), (28) ,("Person i rummet"), ("Giver varm luft")
#]
#Example of a data frame from master arduino

#Setting up our serial port to read the system
ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Timestamp, Room, Temperatur, Aktvitet, Statusrum)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Timestamp, Room, Temperatur, Aktvitet, Statusrum)")

def Readsystem(incomming):
    rooms = 0
    incomming.split(";",) # so list looks like this incommin = [Rum1, 28 , ("Person i rummet") : Rum2, 28, ("Tomt")]
    string_count = len(incomming)
    cur.execute("INSERT INTO Rum1 VALUES(? , ? , ? , ? , ?)",now, incomming[1])
    print("Data succsesfu in table Rum 1")
    conn.commit
    if len(incomming) == string_count():
        try:
            cur.execute("INSERT INTO Rum2 VALUES(? , ? , ? , ? , ?)",now, incomming[2])
            print("Data succsesfu in table Rum 2")
            conn.commit
            main()
        except:
            print("More rooms than allowed.")
            main()



def main()
    while True:
        ser.open()
        line = ser.readline()
        incomming = line.decode()
        print(incomming)
        Readsystem(incomming)
        ser.close()


if __name__ == "__main__":
    main()
