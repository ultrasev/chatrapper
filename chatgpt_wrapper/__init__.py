#!/usr/bin/env python
import asyncio
import base64
import json
import typing
from uuid import uuid4

import httpx
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


class GPTWrapper(object):
    def __init__(self,
                 access_token: str,
                 model: str) -> None:
        """ API wrapper for OpenAI's ChatGPT.
        Args:
            access_token (str): ChatGPT access token, acquired from https://chat.openai.com/api/auth/session
            model (str): model name, options include:
                - "text-davinci-002-render-sha", default model for ChatGPT-3.5
                - "GPT-4", GPT-4 model
        """
        self.access_token = access_token
        self.model = model

    def get_content(self, chunk: str) -> str:
        try:
            text = chunk.lstrip("data: ").strip()
            return json.loads(text)['message']['content']['parts'][0]
        except json.decoder.JSONDecodeError:
            return ""

    async def _stream_from_wss(self, chunk: str) -> typing.AsyncGenerator[str, None]:
        url = json.loads(chunk)['wss_url']
        async with websockets.connect(url) as websocket:
            while True:
                try:
                    response = await websocket.recv()
                    body = json.loads(response)["body"]
                    body = base64.b64decode(body).decode('utf-8')
                    if 'DONE' in body:
                        break
                    yield body
                except ConnectionClosedOK:
                    break
                except ConnectionClosedError:
                    break

    async def stream(self,
                     text: str) -> typing.AsyncGenerator[str, None]:
        body = {
            "action": "next",
            "arkose_token": "null",
            "conversation_mode": {"kind": "primary_assistant"},
            "force_paragen": False,
            "force_rate_limit": False,
            "history_and_training_disabled": True,
            "messages": [{
                "metadata": {},
                "author": {
                    "role": "user"
                },
                "content": {
                    "content_type": "text",
                    "parts": [text]
                }
            }],
            "model": self.model,
            "parent_message_id": str(uuid4()),
            "timezone_offset_min": -330,
            "stream": True
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                'POST',
                url="https://chat.openai.com/backend-api/conversation",
                headers={
                    "accept": "text/event-stream",
                    "accept-language": "en-US",
                    "authorization": f"Bearer {self.access_token}",
                    "content-type": "application/json",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "Referer": "https://chat.openai.com/",
                    "Referrer-Policy": "strict-origin-when-cross-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
                },
                    data=json.dumps(body)) as response:
                async for chunk in response.aiter_text():
                    chunk = chunk.lstrip("data: ").strip()
                    if "wss_url" in chunk:
                        async for x in self._stream_from_wss(chunk):
                            yield self.get_content(x)
                    else:
                        yield self.get_content(chunk)

    async def __call__(self, text: str) -> str:
        prev = ""
        async for x in self.stream(text):
            print(x.replace(prev, ""), end="", flush=True)
            prev = max(prev, x, key=len)
        return prev


async def async_chat(text: str,
                     token: str,
                     model: str = "text-davinci-002-render-sha") -> str:
    rapper = GPTWrapper(token, model)
    response = await rapper(text)
    return response


def chat(text: str,
         token: str,
         model: str = "text-davinci-002-render-sha") -> str:
    return asyncio.run(async_chat(text, token, model))
