import sqlite3
from datetime import datetime
import serial
import time

t = 1  # time to sleep = 1 sec

# Connect to local database in file system
conn = sqlite3.connect('database.db')
cur = conn.cursor()  # Cursor for looking in database

# Setting up our serial port to read the system
ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
ser.dtr = False
ser.rts = False

# Create tables if they do not exist
cur.execute("CREATE TABLE IF NOT EXISTS Rum1(Temperatur REAL, Aktivitet TEXT, Time TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS Rum2(Temperatur REAL, Aktivitet TEXT, Time TEXT)")

def read_system(incoming):
    split_list = incoming.split(";")
    print(split_list)

    try:
        if split_list[0].startswith("M:2"):
            send_timestamp()
        else:
            # Process Rum1
            try:
                data_to_split1 = split_list[1]
                rum1 = data_to_split1.split(":")[2:4]
                date_info = split_list[1].split(":")[5]
                if rum1[0] == "0.00":
                    print("Fake reading")
                    main()
                else:
                    rum1_bits = format(int(rum1[1]), '08b')
                    parts = [int(x, 16) for x in date_info.split(',')]
                    date = datetime(parts[0] + 2000, parts[1], parts[2], parts[3], parts[4], parts[5])
                    rum1[1] = rum1_bits
                    rum1.append(date)
                    print(rum1)
            except Exception as e:
                print(f"Failed to process Rum1 data: {e}")
                print(incoming)
                main()

            # Process Rum2
            try:
                data_to_split2 = split_list[2]
                rum2 = data_to_split2.split(":")[2:4]
                date_info = split_list[2].split(":")[5]
                if rum2[0] == "0.00":
                    print("Fake reading")
                    main()
                else:
                    rum2_bits = format(int(rum2[1]), '08b')
                    parts = [int(x, 16) for x in date_info.split(',')]
                    date = datetime(parts[0] + 2000, parts[1], parts[2], parts[3], parts[4], parts[5])
                    rum2[1] = rum2_bits
                    rum2.append(date)
                    print(rum2)
            except Exception as e:
                print(f"Failed to process Rum2 data: {e}")
                main()

            # Insert data into Rum1
            try:
                conn.execute("INSERT INTO Rum1 VALUES(? , ? , ?)", rum1)
                print("Data successfully in table Rum 1")
                conn.commit()
            except Exception as e:
                print(f"DataError in Rum1: {e}")
                main()

            # Insert data into Rum2
            try:
                conn.execute("INSERT INTO Rum2 VALUES(? , ? , ?)", rum2)
                print("Data successfully in table Rum 2")
                conn.commit()
                main()
            except Exception as e:
                print(f"DataError in Rum2: {e}")
                main()
    except Exception as e:
        print(f"Master failed or connection error: {e}")
        main()

def main():
    time.sleep(t)
    incoming_data = ""
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            incoming_data += data
            if data.endswith(";"):
                break

    if incoming_data:
        print("Putting into table")
        print(incoming_data)
        read_system(incoming_data)
    else:
        print("Empty, waiting for data")
        main()

def send_timestamp():
    dt = datetime.now()
    mystr = f"{dt.year:04x}{dt.month:02x}{dt.day:02x}{dt.hour:02x}{dt.minute:02x}{dt.second:02x}0d"
    print(mystr)
    ser.write(bytes.fromhex(mystr))
    main()

if __name__ == "__main__":
    main()
