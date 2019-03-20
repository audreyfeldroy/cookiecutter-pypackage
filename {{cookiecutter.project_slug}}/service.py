import app.bootstrap

from fastapi import FastAPI
from app.endpoints import setup_routes


def make_app():
    app = FastAPI()
    setup_routes(app)
    return app


app = make_app()
