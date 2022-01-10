import psycopg2
from sshtunnel import SSHTunnelForwarder
import usermenu
import json

f = open('source_files/creds.json')

credentials = json.load(f)
f.close()

dbName = credentials["db_name"]
username = credentials["usnm"]
password = credentials["pswd"]


# with SSHTunnelForwarder(
#         ('starbug.cs.rit.edu', 22),
#         ssh_username=username,
#         ssh_password=password,
#         remote_bind_address=('localhost', 5432)) as server:
#     server.start()
#     print("SSH tunnel established")
#     params = {
#         'database': dbName,
#         'user': username,
#         'password': password,
#         'host': 'localhost',
#         'port': server.local_bind_port
#     }
#
#     conn = psycopg2.connect(**params)
#     curs = conn.cursor()
#     usermenu.menu(conn, curs)
#     curs.close()
#     conn.close()
#
# print("Database connection established")
