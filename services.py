from models import *

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


def create_club(data):
    exists = Club.query.filter_by(code=data['code']).first()
    if exists:
        print('Club already exists.')
        return

    new_club = Club.from_dict(data)
    db.session.add(new_club)
    db.session.commit()
    print(f'Created club {data['code']}.')
'''

def create_club(code: str, name: str, description: str, tags: list):
    exists = Club.query.filter_by(code=code).first()
    if exists:
        print('Club already exists.')
        return

    new_club = Club(code=code,
                    name=name,
                    description=description,
                    tags=tags)
    db.session.add(new_club)
    db.session.commit()
    print(f'Created club {name}.')

'''