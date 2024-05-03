import logging
from time import sleep

from fastapi import FastAPI, APIRouter

from python.game import GAME
from enum import Enum
from pydantic import BaseModel, constr

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()

v0_router = APIRouter(prefix="/v0")


class Input(BaseModel):
    """Input is currently handled as a single character."""
    char: constr(max_length=1)


@v0_router.get("/world")
def get_world():
    return {
        "game_text_list": GAME._world_to_string_list()
    }


# TODO: Once persistence is added
#   And more than a single game can be handled by the server.
#   Need to add game_id to all put requests
@v0_router.put("/input")
def put_input(m_input: Input):
    logger.info(f"put_input {m_input}")
    GAME.handle_input(m_input.char)
    return m_input


@v0_router.put("/tick")
def put_tick():
    GAME._tick()
    return True


app.include_router(v0_router)

# TODO: Need to update main.py so it can be ran using uvicorn.
