from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the static directory located inside the server folder
app.mount("/static", StaticFiles(directory="server/static"), name="static")

@app.get("/")
async def read_index():
    # Serve the static HTML file from the new location
    return FileResponse("server/static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)