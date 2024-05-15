import sqlite3
from datetime import datetime
import serial
import time
t = 1 #time to sleep = 1 secs
dt = datetime.now()

#M:1;I:48:T:0.00:S:1:D:70,5,11,14,34,49;I:49:T:31.60:S:1:D:70,5,11,14,31,30;

conn = sqlite3.connect('database.db') #connet to local database in file system
cur = conn.cursor() #cursoer for looking in database

#Setting up our serial port to read the system
ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
ser.dtr = False
ser.rts = False


# Aktivitet høj = 1, lav = 0. Statusrum -1 = afgiver varme, 0 = neutral, 1 = får varme
cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Temperatur, Aktivitet, Time)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Temperatur, Aktivitet, Time)")

def Readsystem(incomming):
    string_to_split = incomming
    # Splitting the string by ";"
    split_list = string_to_split.split(";")

    print(split_list)

    data_to_split = split_list[0]
    M1 = data_to_split.split(":")
    M1.pop(0)
    print(M1)
    try:
        if M1[0] == "2":
            sendtimestamp()

        else:
            try:
                data_to_split1 = split_list[1]
                rum1 = data_to_split1.split(":")
                rum1.pop(0)
                rum1.pop(0)
                rum1.pop(0)
                rum1.pop(1)
                rum1.pop(2)
                if rum1[0] == "0.00":
                    print("Fake reading")
                    main()
                else:
                    parts = []
                    parts = rum1[2].split(',')
                    year = int(parts[0], 16)
                    month = int(parts[1], 16)
                    day = int(parts[2], 16)
                    hour = int(parts[3], 16)
                    minute = int(parts[4], 16)
                    second = int(parts[5], 16)
                    year += 2000
                    date = datetime(year, month, day, hour, minute, second)
                    rum1.pop(2)
                    rum1.append(date)
                    print(rum1)
            except:
                print("failed to split data")
                print(incomming)

                main()


            try:
                data_to_split2 = split_list[2]
                rum2 = data_to_split2.split(":")
                rum2.pop(0)
                rum2.pop(0)
                rum2.pop(0)
                rum2.pop(1)
                rum2.pop(2)
                if rum1[0] == "0.00":
                    print("Fake reading")
                    main()
                else:
                    parts1 = []
                    parts1 = rum2[2].split(',')
                    year1 = int(parts1[0], 16)
                    month1 = int(parts1[1], 16)
                    day1 = int(parts1[2], 16)
                    hour1 = int(parts1[3], 16)
                    minute1 = int(parts1[4], 16)
                    second1 = int(parts1[5], 16)
                    year1 += 2000
                    date1 = datetime(year1, month1, day1, hour1, minute1, second1)
                    print(date1)
                    rum2.pop(2)
                    rum2.append(date1)
                    print(rum2)
            except:
                print("failed to split data")
                main()

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
    except:
        print("Master failed or connection error")
        main()



def main():
    time.sleep(t)
    incomming = []
    data = ser.readline().decode('utf-8')
    #data = ['M:1;I:48:T:36.10:S:4:D:24,5,5,14,12,36;I:49:T:30.10:S:10:D:24,5,5,14,12,36;']
    #data = ['M:1;I:48:T:0.00:S:1:D:24,5,5,14,12,36;I:49:T:31.60:S:1:D:24,5,5,14,12,36;']
    #data = []
    incomming = data
    if data:
        if len(data) > 0:
            print("Putting into table")
            print(incomming)
            Readsystem(incomming)
        else:
            print("not long enogh")
            print(data)
            print(incomming)
            main()
    else:

        print("Empty waiting for data")
        main()

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
    #ser.write(mystr.encode())
    main()

    #try:
        #while True:
            # Get the current time in hexadecimal format
            #time_hex = get_current_time_hex()
            # Add carriage return (CR) character (0x0D) at the end
            #message = time_hex + "0D"
            # Convert the hex string to bytes
            #message_bytes = bytes.fromhex(message)
            # Send the message over UART
            #ser.write(message_bytes)
            # Print sent message for debugging
            #print(f"Sent: {message_bytes}")
            # Wait for a second before sending the next time
            #time.sleep(1)

    #except:
        #print("Failed to send time")

    #finally:
        #main()


#def get_current_time_hex():
    # Get the current local time
    #current_time = time.localtime()
    # Format the time as HHMMSS
    #time_str = time.strftime("%H%M%S", current_time)
    # Convert the time string to its hexadecimal representation
    #time_hex = time_str.encode('utf-8').hex()
    #return time_hex

if __name__ == "__main__":
    main()
