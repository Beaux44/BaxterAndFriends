from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import starlette
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
song_lock = asyncio.Lock()
song = None


@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@app.get("/now_playing")
async def now_playing(request: Request):
    return templates.TemplateResponse("nowPlaying.html", {"request": request})


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

