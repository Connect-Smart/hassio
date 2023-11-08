import os
import secrets
import asyncio
import aiohttp
import json
import logging
from aiohttp import web

async def get_entity_status(request):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://supervisor/api/states/entity_id') as response:
            data = await response.text()
            entity_status = json.loads(data)
            return web.Response(text=json.dumps(entity_status))

app = web.Application()
app.router.add_get('/get_entity_status', get_entity_status)

web.run_app(app, host='0.0.0.0', port=8099)


def generate_bashio_token():
    token_path = "/data/token.txt"
    if not os.path.isfile(token_path):
        token = secrets.token_hex(32)
        with open(token_path, "w") as file:
            file.write(token)
    else:
        with open(token_path, "r") as file:
            token = file.read().strip()
    return token

bashio_token = generate_bashio_token()


async def get_bashio_token(request):
    return web.Response(text=bashio_token)

app.router.add_get('/get_bashio_token', get_bashio_token)