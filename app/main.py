from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .datasources.weather import WeatherDataSource
from .datasources.transport import TransportDataSource

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/configs", StaticFiles(directory="configs"), name="configs")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

# Serve index.html at the root
@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

@app.get("/weather")
async def weather():
    weather_data_source = WeatherDataSource()
    weather_data = weather_data_source.get_data()
    return weather_data

@app.get("/transport")
async def transport():
    transport_data_source = TransportDataSource()
    transport_data = transport_data_source.get_data()
    return transport_data