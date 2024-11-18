from flask import Flask, jsonify
import pymssql

app = Flask(__name__)

@app.route('/check_connection')
def check_connection():
    try:
        # Update the connection parameters below
        conn = pymssql.connect(
            server='BSEF18ED06',#.database.windows.net',
            user='BSEF18ED06\ITprashasak',
            password='India@123',
            database='enquiries'
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
