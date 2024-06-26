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

# The main function that runs at program start
def main():
    time.sleep(t)  # Pause the program for 't' seconds
    incomming = []  # Initialize an empty list for incoming data
    data = ser.readline().decode('utf-8')  # Read a line from the serial port and decode it to a UTF-8 string
    #data string for debugging with the setup
    #data = ['M:1;I:48:T:36.10:S:4:D:24,5,5,14,12,36;I:49:T:30.10:S:10:D:24,5,5,14,12,36;']
    #data = ['M:1;I:48:T:0.00:S:1:D:24,5,5,14,12,36;I:49:T:31.60:S:1:D:24,5,5,14,12,36;']
    #data = []
    incomming = data  # Assign the incoming data to the variable 'incomming'
    
    if data:  # If data is available
        if len(data) > 0:  # Check if the data length is greater than 0
            print("Putting into table")  # Print a debug message
            print(incomming)  # Print the incoming data
            Readsystem(incomming)  # Call the function 'Readsystem' with the incoming data as an argument
        else:
            print("not long enough")  # Print a debug message if data is not long enough
            print(data)  # Print the current data
            print(incomming)  # Print the incoming data
            main()  # Call the main function again (recursively)
    else:
        print("Empty waiting for data")  # Print a debug message if no data is available
        main()  # Call the main function again (recursively)

# Function to send a timestamp
def sendtimestamp():
    mystr = ""  # Initialize an empty string
    mystr += hex(dt.year)  # Add the year in hexadecimal
    mystr += hex(dt.month)  # Add the month in hexadecimal
    mystr += hex(dt.day)  # Add the day in hexadecimal
    mystr += hex(dt.hour)  # Add the hour in hexadecimal
    mystr += hex(dt.minute)  # Add the minute in hexadecimal
    mystr += hex(dt.second)  # Add the second in hexadecimal
    mystr += hex(0x0d)  # Add a carriage return character in hexadecimal
    print(mystr)  # Print the timestamp string
    main()  # Call the main function again

# Program entry point
if __name__ == "__main__":
    main()  # Call the main function