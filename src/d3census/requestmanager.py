from typing import Any
import json
import asyncio

import aiohttp
from aiohttp import ClientSession
from aiohttp.http import HttpProcessingError
from returns.result import Result, Success, Failure


"""
A request manager that is adapted from real python async io example.
"""


async def fetch_json(url: str, session: ClientSession) -> Result[str, str]:
    response = await session.request(
        method="GET",
        url=url
    )

    try:
        response.raise_for_status()

        json = await response.text()
        return Success(json)

    except(
        aiohttp.ClientError, 
        aiohttp.http.HttpProcessingError,
        aiohttp.ClientResponseError,
        ) as e:

        match e:
            case aiohttp.ClientError | aiohttp.http.HttpProcessingError:
                print(f"Failed with error {e} for URL: {url}")
            case aiohttp.ClientResponseError:
                print(f"Failed with response code {response.status} for URL: {url}")

        return Failure(f"Failed to pull data from {url}, see logs.")


async def parse_json(json_response: str) -> Result[list[list[str]], str]:
    try:
        return Success(json.loads(json_response))

    except:
        return Failure(f"Unable to parse json.")


async def workflow(
    task: str,
    session: ClientSession,
    attempts: int = 0,
) -> list[list[str]]:
    attempts = 0
    while attempts < 3:
        json_response = await fetch_json(task, session)
        match json_response:
            case Failure(msg):
                print(msg)
                attempts+=1
                continue

            case Success(response_str):
                msg = "unkown error"
                lists = await parse_json(response_str)

                match lists:
                    case Failure(_):
                        attempts+=1
                        continue

                    case Success(result):
                        return result

    raise HttpProcessingError(message=msg)


async def worker(
        queries: list[str], 
        outbox: list[list[Any]],
        session: ClientSession
    ):
    while queries:
        task = queries.pop()

        result = await workflow(task, session)
        outbox.append(result)


async def request_manager(calls: list[str]) -> list[list]:
    outbox = []
    async with ClientSession() as session:
        tasks = [
            worker(calls, outbox, session)
            for _ in range(5)
        ]
        await asyncio.gather(*tasks)

    return outbox 
