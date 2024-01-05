# despite what vscode is saying it works
import mysql.connector as mysql

# in mysql created a localhost only user named "bot"
conn = mysql.connect(user='bot', password='SdZBB!9vUW&U]VofDfum', host='localhost', database='shelter_orders')

conn.close()