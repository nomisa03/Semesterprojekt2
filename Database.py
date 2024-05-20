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
    # Function to process an incoming string, split it, and handle different cases based on the split content

    string_to_split = incomming
    # Splitting the incoming string by ";"
    split_list = string_to_split.split(";")

    # Print the split list for debugging
    print(split_list)

    # Processing the first part of the split list
    data_to_split = split_list[0]
    M1 = data_to_split.split(":")
    M1.pop(0)  # Removing the first element from M1
    print(M1)  # Print M1 for debugging

    try:
        if M1[0] == "2":
            # If the first element after pop is "2", call sendtimestamp function
            sendtimestamp()
        else:
            try:
                # Processing the second part of the split list
                data_to_split1 = split_list[1]
                rum1 = data_to_split1.split(":")
                # Removing unnecessary elements from rum1
                rum1.pop(0)
                rum1.pop(0)
                rum1.pop(0)
                rum1.pop(1)
                rum1.pop(2)

                if rum1[0] == "0.00":
                    # If the first element is "0.00", it's a fake reading
                    print("Fake reading")
                    main()  # Call main function to restart or handle the next steps
                else:
                    # Parsing date and time from the remaining elements
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
                    rum1.append(date)  # Appending the parsed date to rum1
                    print(rum1)  # Print rum1 for debugging
            except:
                # If there is an error in splitting data
                print("failed to split data")
                print(incomming)  # Print the incoming string for debugging
                main()  # Call main function to restart or handle the next steps

            try:
                # Processing the third part of the split list
                data_to_split2 = split_list[2]
                rum2 = data_to_split2.split(":")
                # Removing unnecessary elements from rum2
                rum2.pop(0)
                rum2.pop(0)
                rum2.pop(0)
                rum2.pop(1)
                rum2.pop(2)

                if rum2[0] == "0.00":
                    # If the first element is "0.00", it's a fake reading
                    print("Fake reading")
                    main()  # Call main function to restart or handle the next steps
                else:
                    # Parsing date and time from the remaining elements
                    parts1 = rum2[2].split(',')
                    year1 = int(parts1[0], 16)
                    month1 = int(parts1[1], 16)
                    day1 = int(parts1[2], 16)
                    hour1 = int(parts1[3], 16)
                    minute1 = int(parts1[4], 16)
                    second1 = int(parts1[5], 16)
                    year1 += 2000
                    date1 = datetime(year1, month1, day1, hour1, minute1, second1)
                    print(date1)  # Print the parsed date for debugging
                    rum2.pop(2)
                    rum2.append(date1)  # Appending the parsed date to rum2
                    print(rum2)  # Print rum2 for debugging
            except:
                # If there is an error in splitting data
                print("failed to split data")
                main()  # Call main function to restart or handle the next steps

            try:
                # Inserting rum1 data into the database table Rum1
                conn.execute("INSERT INTO Rum1 VALUES(? , ? , ?)", rum1)
                print("Data successfully in table Rum 1")
                conn.commit()  # Commit the transaction
            except:
                # If there is a database error
                print("DataError")
                main()  # Call main function to restart or handle the next steps

            try:
                # Inserting rum2 data into the database table Rum2
                conn.execute("INSERT INTO Rum2 VALUES(? , ? , ?)", rum2)
                print("Data successfully in table Rum 2")
                conn.commit()  # Commit the transaction
                main()  # Call main function to restart or handle the next steps
            except:
                # If there is a database error
                print("DataError.")
                main()  # Call main function to restart or handle the next steps
    except:
        # If there is a connection error or other master failure
        print("Master failed or connection error")
        main()  # Call main function to restart or handle the next steps

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
