from flask import Flask, request, jsonify
from db_create import db
from services import *

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db.init_app(app)

# import models after db to avoid circular imports
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


@app.route("/api/users", methods=["GET"])
def api_user_profile():
    '''
    retrieve a user profile from their username 
    '''
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'No username inputted'}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    profile = {
        "username": user.username,
        "display_name": user.display_name,
        "profile_created": user.created
    }
    return jsonify(profile)


@app.route("/api/clubs/search", methods=["GET"])
def api_club_search():
    '''
    return clubs whose name includes a string (case-insensitive)
    '''
    string = request.args.get('string').strip().lower()
    if not string:
        return jsonify({'error': 'No search parameter inputted'}), 400
    
    clubs = Club.query.filter(Club.name.ilike(f'%{string}%')).all()
    return jsonify([c.to_dict() for c in clubs])


@app.route("/api/clubs/create", methods=["POST"])
def api_club_create():
    '''
    create a club and add it to the database
    '''

    code = request.args.get('code')
    name = request.args.get('name')
    description = request.args.get('description')
    tags = request.args.getlist('tag')

    data = {
        'code': code.strip().lower(),
        'name': name.strip(),
        'description': description.strip(),
        'tags': [t.strip().title() for t in tags]
    }

    create_club(data)

    # create_club(code, name, description, tags)

    return jsonify({'Created club': f'{data['code']}'})


if __name__ == "__main__":
    app.run()
