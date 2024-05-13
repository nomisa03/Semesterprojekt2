import sqlite3
from datetime import datetime
import serial
import time
t = 5 #time to sleep = 1 secs
dt = datetime.now()

#['M:1;S:48:T:31.20:M:1;S:49:T:1.20:M:1;\r\n']e

conn = sqlite3.connect('database.db') #connet to local database in file system
cur = conn.cursor() #cursoer for looking in database

#Setting up our serial port to read the system
ser = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)

# Aktivitet høj = 1, lav = 0. Statusrum -1 = afgiver varme, 0 = neutral, 1 = får varme
cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Temperatur, Aktivitet, Time)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Temperatur, Aktivitet, Time)")

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
        data_to_split1 = split_list[2]
        rum1 = data_to_split1.split(":")
        rum1.pop(0)
        rum1.pop(0)
        rum1.pop(0)
        rum1.pop(1)
        rum1.pop(2)
        parts = rum1[2].split(',')
        day_of_year = int(parts[0])
        hours = int(parts[1])
        minutes = int(parts[2])
        seconds = int(parts[3])
        date = datetime.strptime(f'{day_of_year} {hours}:{minutes}:{seconds}', '%j %H:%M:%S')
        rum1.pop(2)
        rum1.append(date)
        print(rum1)

        data_to_split2 = split_list[3]
        rum2 = data_to_split2.split(":")
        rum2.pop(0)
        rum2.pop(0)
        rum2.pop(0)
        rum2.pop(1)
        rum2.pop(2)
        parts1 = rum2[2].split(',')
        day_of_year1 = int(parts1[0])
        hours1 = int(parts1[1])
        minutes1 = int(parts1[2])
        seconds1 = int(parts1[3])
        date1 = datetime.strptime(f'{day_of_year1} {hours1}:{minutes1}:{seconds1}', '%j %H:%M:%S')
        rum2.pop(2)
        rum2.append(date1)
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
    time.sleep(t)
    # Read the latest line from the serial port
    latest_line = ''
    while ser.in_waiting:
        latest_line = ser.readline().decode('utf-8').strip()

    # Clear the input buffer by reading and discarding any remaining data
    while ser.in_waiting:
        ser.read(ser.in_waiting)

    # Close the serial port when done
    ser.close()
    print(latest_line)
    incomming = []
    incomming = latest_line
    Readsystem(incomming)




    #while True:
        #ser.close()
        #ser.open()
        #time.sleep(t)

        #test string to test the programs.
        #incomming = ['M:2']
        #incomming = ['M:1;S:48:T:31.20:M:1:D:2023,06,14,12,14,30;M:1;S:49:T:1.20:M:1:D:2023,06,14,12,14,30;\r\n']
        #incomming = ['M:1;I:48:T:24.30:S:1:D:70,5,11,14,31,48;I:49:T:1.00:S:1:D:70,5,11,14,31,48']

        #Readsystem(incomming)
        #print(incomming)
        #bytestoread = ser.readline().decode('utf-8').strip()
        #incomming = []
        #incomming.append(bytestoread)
        #print(incomming)
        #Readsystem(incomming)
        #ser.reset_input_buffer()
        #ser.close()



def sendtimestamp():
    mystr = ""
    mystr += hex(dt.year)
    mystr += hex(dt.month)
    mystr += hex(dt.day)
    mystr += hex(dt.hour)
    mystr += hex(dt.minute)
    mystr += hex(dt.second)
    mystr += hex(0x0d)
    print(mystr)
    ser.write(mystr.encode())
    main()

if __name__ == "__main__":
    main()
