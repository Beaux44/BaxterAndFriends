from fastapi import FastAPI, Request, HTTPException, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/client/")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    raise HTTPException(status_code=403, detail="FUCK YOU BOI")


@app.websocket("/client")
async def client_sock(sock: WebSocket):
    await sock.accept()
    while True:
        data = await sock.receive_text()
        await sock.send_text(f"received: {data}")


@app.websocket("/now_playing")
async def now_playing(sock: WebSocket):
    await sock.accept()
    try:
        while True:
            try:
                data = json.load(await sock.receive_text())
            except json.JSONDecodeError:
                await sock.send_text("Fuck you")
                continue
    except starlette.websockets.WebSocketDisconnect:        
        print("Socket Disconnected") 

