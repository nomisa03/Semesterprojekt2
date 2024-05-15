import serial
ser = serial.Serial(port='COM5', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)



def main():
    while True:
        #line = ser.in_waiting
        data = ser.readline().decode('utf-8')
        #line.decode('UTF-8')
        #print(line.strip())
        if len(data) > 8:
            print(data)



if __name__ == "__main__":
    main()
