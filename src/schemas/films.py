from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Film


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        exclube = ['id']
        load_instance = True