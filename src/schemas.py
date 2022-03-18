from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.models import Film, Actor


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        exclube = ['id']
        load_instance = True


class ActorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Actor
        exclube = ['id']
        load_instance = True
