from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .data import get_dashboard_data

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/configs", StaticFiles(directory="configs"), name="configs")

# Serve index.html at the root
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/dashboard")
async def dashboard():
    return get_dashboard_data()