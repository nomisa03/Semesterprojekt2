from datetime import datetime
dt = datetime.now()

mystr = ""
mystr += hex(dt.year)
mystr += hex(dt.month)
mystr += hex(dt.day)
mystr += hex(dt.hour)
mystr += hex(dt.minute)
mystr += hex(dt.second)
print(mystr)