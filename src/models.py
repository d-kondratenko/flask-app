import uuid

from src import db


class Film(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    uuid = db.Column(db.String(36), unique=True)
    description = db.Column(db.Text)
    distributed_by = db.Column(db.String(120), nullable=False)
    length = db.Column(db.Float)
    rating = db.Column(db.Float)

    def __int__(self, title, release_date, description, distributed_by, length, rating, uuid):
        self.title = title
        self.release_date = release_date
        self.description = description
        self.distributed_by = distributed_by
        self.length = length
        self.rating = rating
        self.uuid = str(uuid)

    def __repr__(self):
        return f'Film({self.title}, {self.uuid}, {self.distributed_by},{self.release_date})'

    def to_dict(self):
        return {
            'title': self.title,
            'uuid': self.uuid,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'description': self.description,
            'distributed_by': self.distributed_by,
            'length': self.length,
            'rating': self.rating
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    uuid = db.Column(db.String(36), nullable=False, unique=True)

    def __int__(self, name, birthday, is_active, uuid):
        self.name = name,
        self.birthday = birthday,
        self.is_active = is_active
        self.uuid = str(uuid)

    def __repr__(self):
        return f'Actor({self.name}, {self.birthday}, {self.is_active}, {self.uuid})'

    def to_dict(self):
        return {
            'name': self.name,
            'birthday': self.birthday.strftime('%Y-%m-%d'),
            'is_active': self.is_active,
            'uuid': self.uuid
        }
