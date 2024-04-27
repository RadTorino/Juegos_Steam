import pandas as pd
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def ruta_prueba():
    return "Hola"