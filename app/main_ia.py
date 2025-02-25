from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database_ia import SessionLocalIA
from sql_generator import generar_sql_desde_texto
from chat_generator import generar_respuesta_chat_con_cache
from pydantic import BaseModel
import ollama
from config_handler import config_handler
import json

app = FastAPI(title="API SQL IA")

# Montar directorio estático
app.mount("/static", StaticFiles(directory="static"), name="static")

# Añadir ruta para el index.html
@app.get("/")
async def read_index():
    return FileResponse('index.html')

# Añadir ruta para consultas_chat.html
@app.get("/consultas_chat")
async def read_consultas_chat():
    return FileResponse('consultas_chat.html')

def get_db():
    db = SessionLocalIA()
    try:
        yield db
    finally:
        db.close()

class Pregunta(BaseModel):
    pregunta: str
    config: dict = {}

class Configuracion(BaseModel):
    sql: dict
    chat: dict

@app.post("/consulta_ia/")
async def consulta_ia(pregunta: Pregunta, db: Session = Depends(get_db)):
    """
    Recibe una pregunta en lenguaje natural, la convierte en SQL y ejecuta la consulta.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    
    # Usar la configuración proporcionada o la predeterminada
    respuesta_sql = generar_sql_desde_texto(pregunta_texto, config_params)

    if "error" in respuesta_sql:
        return respuesta_sql  # Devuelve error si la consulta no es segura

    consulta_sql = respuesta_sql["sql"]

    try:
        # Convertir la consulta a texto SQL usando text()
        sql_text = text(consulta_sql)
        result = db.execute(sql_text)
        # Obtener los nombres de las columnas
        columns = result.keys()
        # Convertir los resultados a una lista de diccionarios
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        return {
            "sql": consulta_sql,
            "resultado": rows
        }
    except Exception as e:
        return {"error": f"Error en la consulta: {str(e)}"}

@app.post("/consulta_chat/")
async def consulta_chat(pregunta: Pregunta):
    """
    Recibe una pregunta en lenguaje natural y devuelve la respuesta de Mistral.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    
    return generar_respuesta_chat_con_cache(pregunta_texto, config_params)

@app.post("/consulta_chat_stream/")
async def consulta_chat_stream(pregunta: Pregunta):
    """
    Versión streaming de la consulta de chat.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    
    # Obtener parámetros de configuración
    params = config_handler.get_chat_params()
    # Actualizar con los parámetros personalizados
    if config_params:
        params.update(config_params)
    
    async def generate():
        try:
            stream = ollama.chat(
                model="mistral",
                messages=[{"role": "user", "content": pregunta_texto}],
                stream=True,
                options={
                    "temperature": params.get('temperature', 0.7),
                    "top_k": params.get('top_k', 40),
                    "top_p": params.get('top_p', 0.9),
                    "num_predict": params.get('num_predict', 100),
                    "num_thread": params.get('num_thread', 4)
                }
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")

# Nuevas rutas para manejar la configuración
@app.get("/api/config")
def get_config():
    """Devuelve la configuración actual."""
    return JSONResponse(config_handler.get_config())

@app.get("/api/config/default")
def get_default_config():
    """Devuelve la configuración predeterminada."""
    # Recargar la configuración desde el archivo
    config_handler._load_config()
    return JSONResponse(config_handler.get_config())

@app.post("/api/config")
def update_config(config: Configuracion):
    """Actualiza la configuración."""
    config_handler.update_config(config.dict())
    return JSONResponse({"status": "success", "message": "Configuración actualizada"})