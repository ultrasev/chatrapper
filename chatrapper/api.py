#!/user/bin/env python
import logging

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from .model import AsyncRapper, RefreshTokenException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()


class ChatCompletion(BaseModel):
    model: str
    messages: list
    stream: bool


@app.post("/v1/chat/completions")
async def get_chat_completions(completion: ChatCompletion):
    logging.info({
        "args": completion.dict(),
    })
    try:
        if completion.stream:
            return StreamingResponse(
                AsyncRapper(model=completion.model,
                            stream=completion.stream).stream_token(
                                completion.messages))
        else:
            return await AsyncRapper(model=completion.model,
                                     stream=completion.stream)(completion.messages)
    except RefreshTokenException as e:
        logging.error(e)
        return {"error": "Failed to refresh token"}
    except Exception as e:
        logging.error(e)
        return {"error": "Failed to get chat completions"}


@app.get("/helloworld")
def _hw():
    return {"hello": "world"}
