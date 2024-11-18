# import pymssql

# # Connection parameters
# SERVER = 'AZUREBSEBTIDB.database.windows.net,1911'  # Replace with your actual Azure SQL server name
# USERNAME = 'bseazure\\bti.ops'        # Replace with your Azure SQL username (usually formatted as 'username@servername')
# PASSWORD = 'Welcome@#$24'                     # Replace with your actual password
# DATABASE = 'BTI'                     # Replace with your actual database name

# def get_db_connection():
#     try:
#         conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
#         print("Connection successful!")
#         return conn
#     except pymssql.Error as e:
#         print(f"Error connecting to the database: {e}")
#         return None

# # Example usage
# if __name__ == "__main__":
#     connection = get_db_connection()
#     if connection:
#         connection.close()  # Close the connection when done



#############################################################
from flask import Flask, jsonify
import pymssql

app = Flask(__name__)

# @app.route('/check_connection')
@app.route('/')
def check_connection():
    try:
        # Update the connection parameters below
        conn = pymssql.connect(
            # server = 'AZUREBSEBTIDB:1911',  # Replace with your actual Azure SQL server name
            server = '172.16.173.4:1911',  # Replace with your actual Azure SQL server name
            user = 'btiuser',       # Replace with your Azure SQL username (usually formatted as 'username@servername')
            password = 'bt!u$er@123'  ,
            # user='BSEAZURE\\bti.ops',
            # password='Welcome@#$24',                   # Replace with your actual password
            database = 'BTI'
            # server='AZUREBSEBTIDB.database.windows.net,1911',
            # # server='AZUREBSEBTIDB.BSEAZURE.DOMAIN',#.database.windows.net',
            # # server='172.16.169.4',
            # # server='172.16.14.3,1911',
            # # user='BSEAZURE\\bti.ops',
            # # password='Welcome@#$24',
            # user='AZUREBSEBTIDB\\btiuser',
            # password='bt!u$er@123',
            # # SQL_USERNAME = 'btiuser'
            # # SQL_PASSWORD = 'bt!u$er@123'
            # # database='BTI'
            # database='BTI'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        
        conn.close()  # Close the connection
        return jsonify({"message": "Connection successful", "version": row[0]})
    
    except pymssql.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
