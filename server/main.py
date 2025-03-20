from fastapi import FastAPI
from fastapi_socketio import SocketManager
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
socket_manager = SocketManager(app=app)

@app.sio.on("join")
async def handle_join(sid, *args, **kwargs):
    await app.sio.emit("test", "123")

# Mount the static directory located inside the server folder
app.mount("/static", StaticFiles(directory="server/static"), name="static")


@app.get("/")
async def read_index():
    # Serve the static HTML file from the new location
    return FileResponse("server/static/index.html")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
