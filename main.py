#  importar fatapion FastAPI
from fastapi import FastAPI
# Crear una instancia de la aplicación FastAPI
app = FastAPI()
# Definir una ruta raíz que devuelve un mensaje de bienvenida
@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a FastAPI!"}  
