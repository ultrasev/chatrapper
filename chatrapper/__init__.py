#!/usr/bin/env python
import asyncio
import uuid
import base64
import json
import typing
from uuid import uuid4

import httpx
import websockets
import logging
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

BASE_URL = "https://chat.openai.com"


class ReqHeader(object):
    def __init__(self, **kwargs):
        self._dict = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "oai-language": "en-US",
            "origin": BASE_URL,
            "pragma": "no-cache",
            "referer": BASE_URL,
            "sec-ch-ua":
            '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        self._dict.update(kwargs)

    def __iter__(self):
        return iter(self._dict.items())


class MessageDeserializer(object):
    def __init__(self, data: str) -> None:
        self.data = data.lstrip("data: ").strip()

    def __str__(self) -> str:
        try:
            js = json.loads(self.data)
            return js['message']['content']['parts'][0]
        except json.decoder.JSONDecodeError:
            return ""
        except KeyError:
            logging.error(f"Error: {self.data}")
            return ""


class AsyncRapper(object):
    def __init__(self,
                 access_token: str = "",
                 model: str = "text-davinci-002-render-sha",
                 stream: bool = True) -> None:
        """ API (w)rapper for OpenAI's ChatGPT.
        Args:
            access_token (str): ChatGPT access token, acquired from https://chat.openai.com/api/auth/session
            model (str): model name, options include:
                - "text-davinci-002-render-sha", default model for ChatGPT-3.5
                - "GPT-4", GPT-4 model
            stream (bool): whether to print the output in real-time or not
        """
        self.access_token = access_token
        self.model = model
        self.stream_real_time = stream
        self.device_id = str(uuid.uuid4())

    async def get_new_session_id(self) -> str:
        headers = dict(ReqHeader(**{"oai-device-id": self.device_id}))
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/backend-anon/sentinel/chat-requirements", headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get('token')
                return token
            else:
                logging.error(response.text)
                logging.error("Failed to refresh session ID and token")

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

        session_id = await self.get_new_session_id()
        assert session_id is not None, "Failed to get session ID"
        headers = dict(ReqHeader(
            **{"oai-device-id": self.device_id,
               "openai-sentinel-chat-requirements-token": session_id}))

        async with httpx.AsyncClient() as client:
            async with client.stream(
                    'POST',
                    url=f"{BASE_URL}/backend-api/conversation",
                    headers=headers,
                    data=json.dumps(body)
            ) as response:
                async for chunk in response.aiter_text():
                    chunk = chunk.lstrip("data: ").strip()
                    if "wss_url" in chunk:
                        async for x in self._stream_from_wss(chunk):
                            yield str(MessageDeserializer(x))
                    else:
                        yield str(MessageDeserializer(chunk))

    async def __call__(self, text: str) -> str:
        prev = ""
        async for x in self.stream(text):
            if self.stream_real_time:
                print(x.replace(prev, ""), end="", flush=True)
            prev = max(prev, x, key=len)
        return prev


class Rapper(object):
    def __init__(self,
                 access_token: str = "",
                 model: str = "text-davinci-002-render-sha",
                 stream: bool = True
                 ) -> None:
        self._proxy = AsyncRapper(access_token, model, stream)

    def __call__(self, text: str) -> str:
        return asyncio.run(self._proxy(text))
