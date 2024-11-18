from flask import Flask
import pymssql

app = Flask(__name__)

# Configuration for pymssql
# app.config['SQL_SERVER'] = {
#     'server': 'hostname_or_ip',
#     'user': 'username',
#     'password': 'password',
#     'database': 'database_name'
# }
# app.config['SQL_SERVER'] = {
#     'server': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'enquiry_db'
# }
app.config['SQL_SERVER'] = {
    'server': 'AZUREBSEBTIDB',
    'user': 'btiuser',
    'password': 'bt!u$er@123',
    'database': 'BTI'
}

def get_db_connection():
    conn = pymssql.connect(
        server=app.config['SQL_SERVER']['server'],
        user=app.config['SQL_SERVER']['user'],
        password=app.config['SQL_SERVER']['password'],
        database=app.config['SQL_SERVER']['database']
    )
    print(conn)
    return conn

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM your_table')
#     results = cursor.fetchall()
#     conn.close()
#     return str(results)