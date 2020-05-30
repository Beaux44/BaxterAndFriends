from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import random
import asyncio
import starlette
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Quote(BaseModel):
    user: str
    text: str

song_lock = asyncio.Lock()
song = None
# lmao
quotes = [{"user": "Satan0", "text": "\"Not everything is a lesson, sometimes you just fail.\""},{"user": "Satan0", "text": "lol JSON? I use my own inarguably worse \"proprietary\" format that uses the same symbols but differently because I like making things harder Kappa"},{"user": "Satan0", "text": "\"Not everyone gets a happy ending. Suffering does not automatically mean it will get better in the future. Sometimes it will just get worse until you die. You can very well be that unlucky person.\""},{"user": "Satan0", "text": "\"Everyone is identical in their own secret unspoken belief that way deep down they are different from everyone else.\""},{"user": "Satan0", "text": "\"There are corpses on Mount Everest that were once highly motivated people.\""},{"user": "Satan0", "text": "fuckin gitler man"},{"user": "Satan0", "text": "I will search to the ends of the flat earth for this god damned fucking email"},{"user": "Satan0", "text": "you know I really hate how people have non-unique identifiers"},{"user": "Satan0", "text": "coffee and brusselsprouts is probably the weirdest fucking dinner I have ever fucking heard"},{"user": "Satan0", "text": "*when you inadvertently create the single best scheduler API in existence*"},{"user": "Satan", "text": "you need to stop fucking using a single 400 line file for everything"},{"user": "Satan0", "text": "preemptive optimization is the bane of good programs"},{"user": "not_a_knife", "text": "the code is a window into his soul"}]


@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@app.get("/now_playing")
async def now_playing(request: Request):
    return templates.TemplateResponse("nowPlaying.html", {"request": request})


@app.get("/random_quote", response_model=Quote)
async def random_quote():
    return random.choice(quotes)


@app.get("/favicon.ico")
async def favicon():
    raise HTTPException(status_code=403, detail="FUCK YOU BOI")


@app.get("/add_song")
async def add_song(request: Request):
    raise HTTPException(status_code=405, detail="Do this shit")


@app.get("/skip_song")
async def skip_song(request: Request):
    raise HTTPException(status_code=405, detail="Do this shit")


@app.websocket("/client")
async def client_sock(sock: WebSocket):
    global song
    await sock.accept()
    try:
        while True:
            try:
                data = await sock.receive_json()
                event = data["event"]

                if event == "CLOSE":
                    await sock.send_text("CLOSING SOCKET")
                    sock.close()
                    break
                elif event == "CONNECT":
                    await sock.send_text("SOCKET CONNECTED")
                elif event == "UPD_SLIDER":
                    print(f"NEW VAL FOR SLIDER <{data['name']}>: {data['value']}")
                elif event == "SONG":
                    async with song_lock:
                        song = data["song"]

            except json.JSONDecodeError:
                await sock.send_text("Fuck you")
                continue
    except starlette.websockets.WebSocketDisconnect:        
        print("Socket Disconnected")


@app.websocket("/now_playing")
async def now_sock(sock: WebSocket):
    global song
    await sock.accept()
    try:
        while True:
            await asyncio.sleep(0.5)
            async with song_lock:
                if song:
                    await sock.send_json(song)
                    song = None
    except starlette.websockets.WebSocketDisconnect:
        print("Now Playing Socket Abruptly Disconnected")

