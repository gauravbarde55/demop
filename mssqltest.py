from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your own MSSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://username:password@server/database'
    '?driver=ODBC+Driver+17+for+SQL+Server'
)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def index():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
