from fastapi import FastAPI, WebSocket
from fastapi_socketio import SocketManager
from fastapi.staticfiles import StaticFiles

app = FastAPI()
sio = SocketManager(app=app)

app.mount("/", StaticFiles(directory="server/static", html=True), name="static")

@app.sio.on('join')
async def handle_join(sid, *args, **kwargs):
    await app.sio.emit('lobby', 'User joined')
    
@sio.on('test')
async def test(sid, *args, **kwargs):
    await sio.emit('hey', 'joe')

#@socket_manager.on("connect")
#async def connect(sid, env):
#    print("New Client Connected to This id :"+" "+str(sid))
    
#@socket_manager.on("disconnect")
#async def disconnect(sid):
#    print("Client Disconnected: "+" "+str(sid))
    


#app.websocket("/ws")
#async def websocket_endpoint(websocket: WebSocket):
#    await websocket.accept()
#    while True:
#        data = await websocket.receive_text()
#        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
