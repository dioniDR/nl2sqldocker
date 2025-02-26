from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database_ia import SessionLocalIA
from pydantic import BaseModel
from config_handler import config_handler
from ai_providers.base_provider import AIProvider
import json
import os

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
    provider: str = None  # Opcional: permite al usuario elegir el proveedor

class Configuracion(BaseModel):
    ai_provider: str = None
    sql: dict = {}
    chat: dict = {}
    ollama: dict = {}
    claude: dict = {}
    openai: dict = {}

def get_ai_provider(provider_name=None):
    """
    Obtiene el proveedor de IA adecuado basado en la configuración o la solicitud.
    
    Args:
        provider_name: Nombre opcional del proveedor a usar
        
    Returns:
        Una instancia del proveedor de IA
    """
    if provider_name is None:
        provider_name = config_handler.get_active_provider()
    
    try:
        return AIProvider.get_provider(provider_name)
    except ValueError as e:
        print(f"Error al obtener proveedor {provider_name}: {str(e)}")
        # Fallback al proveedor por defecto
        return AIProvider.get_provider("ollama")

@app.post("/consulta_ia/")
async def consulta_ia(pregunta: Pregunta, db: Session = Depends(get_db)):
    """
    Recibe una pregunta en lenguaje natural, la convierte en SQL y ejecuta la consulta.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    provider_name = pregunta.provider or config_handler.get_active_provider()
    
    # Obtener el proveedor de IA adecuado
    provider = get_ai_provider(provider_name)
    
    # Obtener la consulta SQL usando el proveedor
    respuesta_sql = await provider.generate_sql(pregunta_texto, config_params)

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
            "resultado": rows,
            "provider": provider_name
        }
    except Exception as e:
        return {"error": f"Error en la consulta: {str(e)}"}

@app.post("/consulta_chat/")
async def consulta_chat(pregunta: Pregunta):
    """
    Recibe una pregunta en lenguaje natural y devuelve la respuesta del modelo.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    provider_name = pregunta.provider or config_handler.get_active_provider()
    
    # Obtener el proveedor de IA adecuado
    provider = get_ai_provider(provider_name)
    
    # Generar respuesta de chat
    respuesta = await provider.generate_chat_response(pregunta_texto, config_params)
    
    # Añadir información del proveedor a la respuesta
    respuesta["provider"] = provider_name
    
    return respuesta

@app.post("/consulta_chat_stream/")
async def consulta_chat_stream(pregunta: Pregunta):
    """
    Versión streaming de la consulta de chat.
    """
    # Extraer la pregunta y la configuración del cuerpo de la solicitud
    pregunta_texto = pregunta.pregunta
    config_params = pregunta.config
    provider_name = pregunta.provider or config_handler.get_active_provider()
    
    # Obtener el proveedor de IA adecuado
    provider = get_ai_provider(provider_name)
    
    # Generar respuesta en streaming
    return StreamingResponse(provider.generate_stream_response(pregunta_texto, config_params), 
                             media_type="text/plain")

# Rutas para manejar la configuración
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
    config_handler.update_config(config.dict(exclude_unset=True))
    config_handler.save_config()
    return JSONResponse({"status": "success", "message": "Configuración actualizada"})

@app.get("/api/providers")
def get_available_providers():
    """Devuelve los proveedores disponibles y sus estados."""
    providers = {
        "ollama": {"available": True, "name": "Ollama (Mistral)"},
        "claude": {"available": bool(os.getenv("ANTHROPIC_API_KEY")), "name": "Claude (Anthropic)"},
        "openai": {"available": bool(os.getenv("OPENAI_API_KEY")), "name": "GPT (OpenAI)"}
    }
    
    # Añadir el proveedor activo
    active_provider = config_handler.get_active_provider()
    return JSONResponse({
        "providers": providers, 
        "active": active_provider
    })

# Punto de entrada
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
