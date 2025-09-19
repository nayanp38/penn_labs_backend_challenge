import os

from app import app, DB_FILE
from db_create import db
from models import *
import json
from pathlib import Path


def create_user(username: str, display_name: str, email: str, admin: bool):
    exists = User.query.filter_by(username=username).first()
    if exists:
        print('User already exists.')
        return

    new_user = User(username=username, 
                display_name=display_name, 
                email=email, 
                admin=admin)
    db.session.add(new_user)
    db.session.commit()
    print(f'Created user {username}.')

def load_data():
    '''
    load clubs from json to the db
    '''
    data_path = Path(__file__).parent / 'clubs.json'
    if not data_path.exists():
        print(f'clubs.json not found at {data_path}')
        return

    with data_path.open() as f:
        clubs = json.load(f)

        # find all unique tag names
        unique_tags = set()
        for c in clubs:
            for t in c.get("tags", []) or []:
                if t and t.strip():
                    unique_tags.add(t.strip())

        # make the new tags
        created_tags = 0
        for tag_name in unique_tags:
            if not Tag.query.filter_by(name=tag_name).first():
                db.session.add(Tag(name=tag_name))
                created_tags += 1
        if created_tags:
            db.session.commit()

        # build club objects and attach tags
        added = 0
        for c in clubs:
            code = c.get("code")
            if not code:
                continue
            if Club.query.filter_by(code=code).first():
                print(f'Skipping existing club: {code}')
                continue

            # building clubs
            tag_names = [t for t in (c.get("tags", []) or []) if t and t.strip()]
            club = Club(code=c["code"], name=c.get("name", ""), description=c.get("description"))
            club.tags = [Tag.query.filter_by(name=tn).first() for tn in tag_names]

            db.session.add(club)
            added += 1

        if added:
            db.session.commit()
        print(f'Loaded {added} new clubs with {created_tags} new tags).')


# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    LOCAL_DB_FILE = 'instance/' + DB_FILE
    if os.path.exists(LOCAL_DB_FILE):
        os.remove(LOCAL_DB_FILE)

    with app.app_context():
        db.create_all()
        create_user('josh', 'Josh', 'josh@seas.upenn.edu', False)
        load_data()
