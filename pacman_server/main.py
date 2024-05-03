import logging
from time import sleep

from fastapi import FastAPI

from python.game import GAME
import python.config as config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/world")
def get_world():
    return GAME._world_to_string()
