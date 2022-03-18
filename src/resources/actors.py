
import uuid
from datetime import datetime

from flask import request
from flask_restful import Resource

from src import db
from src.database.models import Actor


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