import uuid
from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import api, db
from src.models import Film, Actor
from src.schemas import FilmSchema


class FilmListApi(Resource):
    film_schema = FilmSchema()

    def get(self, uuid=None):
        if not uuid:
            films = db.session.query(Film).all()
            return self.film_schema.dump(films, many=True), 200

        film = db.session.filter_by(id=uuid).first()
        if not film:
            return '', 404
        return self.film_schema.dump(film), 200

    def post(self):
        try:
            film = self.film_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(film)
        db.session.commit()

        return self.film_schema.dump(film), 201

    def put(self, uuid):
        film = db.session.query()

    def patch(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        film_json = request.json
        title = film_json.get('title')
        release_date = datetime.strptime(film_json.get('release_date'), '%B %d, %Y') if film_json.get(
            'release_date') else None
        distributed_by = film_json.get('distributed_by')
        description = film_json.get('description')
        length = film_json.get('length')
        rating = film_json.get('rating')

        if title:
            film.title = title
        elif release_date:
            film.release_date = release_date
        elif distributed_by:
            film.distributed_by = distributed_by
        elif description:
            film.description = description
        elif length:
            film.length = length
        elif rating:
            film.rating = rating

        db.session.add(film)
        db.session.commit()
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return '', 404
        db.session.delete(film)
        db.session.commit()
        return '', 204


class ActorListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            actors = db.session.query(Actor).all()
            return [a.to_dict() for a in actors], 200

        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        return actor.to_dict(), 200

    def post(self):
        actor_json = request.json
        if not actor_json:
            return {'message': 'Wrong data'}, 400
        try:
            act = (actor_json['is_active'])
            if act == "True":
                act_bool = True
            else:
                act_bool = False
            actor = Actor(
                name=actor_json['name'],
                birthday=datetime.strptime(actor_json['birthday'], '%Y-%m-%d'),
                is_active=act_bool,
                uuid=uuid.uuid4().hex
            )

            db.session.add(actor)
            db.session.commit()
        except(ValueError, KeyError):
            return {'message': 'Wrong data'}, 400

        return {'message': 'Created successfully'}, 200

    def put(self, uuid):
        actor_json = request.json
        if not actor_json:
            return {'message': 'Wrong data'}, 400
        try:
            act = (actor_json['is_active'])
            if act == "True":
                act_bool = True
            else:
                act_bool = False
            db.session.query(Actor).filter_by(uuid=uuid).update(
                dict(
                    name=actor_json['name'],
                    birthday=datetime.strptime(actor_json['birthday'], '%Y-%m-%d'),
                    is_active=act_bool

                )
            )
            db.session.commit()
        except(ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        actor_json = request.json
        name = actor_json.get('name')
        birthday = datetime.strptime(actor_json.get('birthday', '%Y-%m-%d')) if actor_json.get('birthday') else None
        is_active = actor_json.get('is_active')

        if name:
            actor.name = name
        elif birthday:
            actor.birthday = birthday
        elif is_active:
            act = (actor_json['is_active'])
            if act == "True":
                act_bool = True
            else:
                act_bool = False
            actor.is_active = act_bool

        db.session.add(actor)
        db.session.commit()

        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        actor = db.session.query(Actor).filter_by(uuid=uuid).first()
        if not actor:
            return '', 404
        db.session.delete(actor)
        db.session.commit()
        return '', 204


api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<uuid>', strict_slashes=False)
