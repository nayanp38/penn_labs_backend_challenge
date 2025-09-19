from db_create import db
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between clubs and tags
club_tags = db.Table(
	'club_tags',
	db.Column('club_id', db.Integer, db.ForeignKey('club.id'), primary_key=True),
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
)


class Club(db.Model):
	__tablename__ = 'club'

	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.Text)
	tags = relationship('Tag', secondary=club_tags, back_populates='clubs')

	def to_dict(self):
		'''
		create JSON dict from club
		'''
		return {
			'id': self.id,
			'code': self.code,
			'name': self.name,
			'description': self.description,
			'tags': [t.name for t in self.tags],
		}

	@staticmethod
	def from_dict(data):
		'''
		create club from dict
		'''
		tags = data.get('tags', []) or []
		club = Club(code=data['code'], name=data.get('name', ''), description=data.get('description'))
		# Attach Tag objects (caller should add to session and commit)
		club.tags = []
		for tag_name in tags:
			tag = Tag.get_or_create(tag_name)
			club.tags.append(tag)
		return club


class Tag(db.Model):
	__tablename__ = 'tag'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, unique=True, nullable=False)

	clubs = relationship('Club', secondary=club_tags, back_populates='tags')

	@staticmethod
	def get_or_create(name):
		'''
		retrieve a tag or create a new one if it doesnt exist
		'''
		name = name.strip()
		if not name:
			return None
		exists = Tag.query.filter_by(name=name).first()
		if exists:
			return exists
		return Tag(name=name)


class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True, nullable=False)
	email = db.Column(db.String, unique=True, nullable=True)
	display_name = db.Column(db.String, nullable=True)
	admin = db.Column(db.Boolean, default=False)
	created = db.Column(db.DateTime, server_default=db.func.now())

	def to_dict(self):
		return {
			'id': self.id,
			'username': self.username,
			'email': self.email,
			'display_name': self.display_name,
			'admin': self.admin,
			'created': self.created.isoformat() if self.created else None,
		}

	@staticmethod
	def from_dict(data):
		return User(
			username=data.get('username'),
			email=data.get('email'),
			display_name=data.get('display_name'),
			is_admin=bool(data.get('is_admin', False)),
		)

