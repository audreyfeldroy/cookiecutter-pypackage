import app.bootstrap

import hug

from apphelpers.rest.hug import APIFactory
from app.endpoints import setup_routes

import app.models

from converge import settings


def make_app():
    router = hug.route.API(__name__)

    api_factory = APIFactory(router)
    api_factory.setup_db_transaction(app.models.db)
    # sessiondb_conn = dict(host=settings.SESSIONSDB_HOST,
    #                       port=settings.SESSIONSDB_PORT,
    #                       password=settings.SESSIONSDB_PASSWD,
    #                       db=settings.SESSIONSDB_NO)
    # api_factory.setup_session_db(sessiondb_conn)

    setup_routes(api_factory)


make_app()
