#!/usr/bin/env python
import pytest

from chatrapper import AsyncRapper, Rapper, ReqHeader


def test_header():
    rh = ReqHeader(**{"hello": "world"})
    assert isinstance(dict(ReqHeader()), dict)


@pytest.mark.asyncio
async def test_async_rapper_working():
    answer = await AsyncRapper(stream=False
                               )("What is the capital of the United States?")
    assert "Washington" in answer


@pytest.mark.asyncio
async def test_get_ession_id():
    session_id = await AsyncRapper().get_new_session_id()
    assert session_id is not None
