from flask import Flask, request, jsonify
from db_create import db

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"

# Initialize the centralized db with this app
db.init_app(app)

# Import models after db is available on the app to avoid circular imports
from models import *


@app.route("/")
def main():
    return "Welcome to Penn Club Review!"


@app.route("/api")
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

@app.route("/api/clubs", methods=["GET"])
def api_clubs():
    '''
    return a JSON of all clubs
    '''
    clubs = Club.query.all()
    return jsonify([c.to_dict() for c in clubs])

if __name__ == "__main__":
    app.run()
