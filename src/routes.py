from src import api
from src.resources.actors import ActorListApi
from src.resources.films import FilmListApi

api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<uuid>', strict_slashes=False)
