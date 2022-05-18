#import pyodbc
import pickle
import mysql.connector
#from statsmodels.tsa.arima.model import ARIMA
from datetime import date,datetime

conn = mysql.connector.connect(
    host = "localhost",
    database = "Temperature_db",
    user = "Buddhika",
    password = "256595")

cursor = conn.cursor()
cursor.execute('SELECT * FROM Temp_db')

for row in cursor:
    print((row))

pickle_in = open("model","rb")
Predict_list = pickle.load(pickle_in)

from datetime import date
today = date.today()
d1 = today.strftime("%Y-%m-%d")
s= d1.split("-")
s[0] = int(s[0])+1
new = str(s[0]) + "-"+str(s[1])+"-"+str(1)

f=[]
for i in cursor:
    f.append(str(i[0]))
    print(cursor)

updated_pred_list = Predict_list.predict('2013-10-01',new)

for i,j in updated_pred_list.items():
    date = datetime.strftime(i," %Y-%m-%d")  
    print(date,j)
    cursor.execute("insert into Temp_db (Dates ,Value) values ('"+date+"', "+str(j)+") ")
    conn.commit()
