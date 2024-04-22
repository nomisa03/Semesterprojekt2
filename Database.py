import sqlite3
from datetime import datetime

now = datetime.now()

conn = sqlite3.connect('database.db')

cur = conn.cursor()

data = [
(now), ("Rum 1"), (28) ,("Person i rummet"), ("Giver varm luft")
]

cur.execute("CREATE TABLE IF NOT EXISTS Data(Timestamp, Room, Temperatur, Aktvitet, Statusrum)")

cur.execute("INSERT INTO Data VALUES(? , ? , ? , ? , ?)", data)

conn.commit()



def Readsystem()
    #Læs I2C fra data harvester
    #while read = true
    cur.execute("INSERT INTO Data VALUES(? , ? , ? , ? , ?)", data)
    return 0



#def makegraph()
    #cur.execute(Read)
    #read = grahp
    #Matplotlib
    #Send til GUI
    #return graph
