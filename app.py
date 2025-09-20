from flask import Flask, request, jsonify
from db_create import db
from services import *

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE}"
db.init_app(app)

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

    if (not code) or (not name): 
        return jsonify({'error': 'code and name fields required'}), 400

    data = {
        'code': code.strip().lower(),
        'name': name.strip(),
        'description': description.strip(),
        'tags': [t.strip().title() for t in tags]
    }

    create_club(data)

    return jsonify({'Created club': f'{data['code']}'})



@app.route("/api/clubs/favorite", methods=["POST"])
def api_club_favorite():
    '''
    favorites a club
    '''
    code = request.args.get('code')
    username = request.args.get('username')

    if (not code) or (not username):
        return jsonify({'error': 'club code and username required'}), 400

    club = Club.query.filter_by(code=code).first()
    if not club:
        return jsonify({'error': 'Club not found'}), 404

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    fav = Favorite(club_id=club.id, user_id=user.id)
    db.session.add(fav)
    db.session.commit()

    return jsonify(club.to_dict())



@app.route('/api/clubs/<code>', methods=['PATCH'])
def api_club_update(code):
    '''
    updates a club if user is admin.
    updateable fields: name, description, tags
    '''
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'admin username required'}), 401

    user = User.query.filter_by(username=username).first()
    if not user or not user.admin:
        return jsonify({'error': 'admin privileges required'}), 403

    club = Club.query.filter_by(code=code).first()
    if not club:
        return jsonify({'error': 'Club not found'}), 404

    name = request.args.get('name')
    description = request.args.get('description')
    tags = request.args.getlist('tag')

    data = {}

    if name:
        data['name'] = name.strip()
    if description:
        data['description'] = description.strip()
    if tags:
        data['tags'] = [t.strip().title() for t in tags]


    try:
        club.update_from_dict(data)
        db.session.add(club)
        db.session.commit()
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(club.to_dict())


@app.route('/api/tags', methods=['GET'])
def api_tags():
    '''
    return a JSON of all tags and the number of clubs associated with each tag
    '''
    tags = Tag.query.all()
    return jsonify([t.to_dict() for t in tags])



if __name__ == "__main__":
    app.run()
