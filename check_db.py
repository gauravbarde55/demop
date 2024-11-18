# from flask import Flask, jsonify
# import pyodbc

# app = Flask(__name__)

# # Database configuration
# SERVER = 'AZUREBSEBTIDB,1911'  # Server name and port
# USERNAME = 'btiuser'            # SQL Server username
# PASSWORD = 'bt!u$er@123'       # SQL Server password

# # Connection string for SQL Server authentication
# connection_string = (
#     f'DRIVER={{ODBC Driver 18 for SQL Server}};'
#     f'SERVER={SERVER};'
#     f'UID={USERNAME};'
#     f'PWD={PASSWORD};'
# )

# @app.route('/databases')
# def get_databases():
#     conn = None
#     cursor = None
#     try:
#         conn = pyodbc.connect(connection_string)
#         cursor = conn.cursor()

#         # Execute a query to get all databases
#         cursor.execute("SELECT name FROM sys.databases")
#         rows = cursor.fetchall()

#         # Extract database names into a list
#         databases = [row[0] for row in rows]

#         return jsonify(databases)

#     except Exception as e:
#         return jsonify({"error": str(e)})

#     finally:
#         if cursor is not None:
#             cursor.close()
#         if conn is not None:
#             conn.close()

# if __name__ == '__main__':
#     app.run(debug=True)



####################################

import pymssql

def ping_sql_server(server, user, password, database):
    try:
        # Establish a connection to the SQL Server instance
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        conn.close()  # Close the connection if successful
        return True  # Connection was successful
    except pymssql.OperationalError as e:
        print(f"OperationalError: {e}")  # Handle specific operational errors
        return False  # Connection failed
    except Exception as e:
        print(f"Error: {e}")  # Handle any other exceptions
        return False  # Connection failed

# Usage
# DB_HOST = 'AZUREBSEBTIDB\\AZUREBSEBTIDB22'  # e.g., 'localhost' or 'yourserver\instance'
# DB_HOST = 'AZUREBSEBTIDB',
DB_HOST = '172.16.173.4:1911'
DB_USER = 'btiuser'
DB_PASSWORD = 'bt!u$er@123'
DB_NAME = 'BTI'

if ping_sql_server(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
    print("Ping successful: SQL Server is reachable.")
else:
    print("Ping failed: Unable to reach SQL Server.")
