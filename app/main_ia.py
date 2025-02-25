from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from database_ia import SessionLocalIA
from sql_generator import generar_sql_desde_texto
from chat_generator import generar_respuesta_chat_con_cache
from pydantic import BaseModel
import ollama

app = FastAPI(title="API SQL IA")

# Montar directorio estático
app.mount("/static", StaticFiles(directory="."), name="static")

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

@app.post("/consulta_ia/")
def consulta_ia(pregunta: Pregunta, db: Session = Depends(get_db)):
    """
    Recibe una pregunta en lenguaje natural, la convierte en SQL y ejecuta la consulta.
    """
    respuesta_sql = generar_sql_desde_texto(pregunta.pregunta)

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
def consulta_chat(pregunta: Pregunta):
    """
    Recibe una pregunta en lenguaje natural y devuelve la respuesta de Mistral.
    """
    return generar_respuesta_chat_con_cache(pregunta.pregunta)

@app.post("/consulta_chat_stream/")
async def consulta_chat_stream(pregunta: Pregunta):
    """
    Versión streaming de la consulta de chat.
    """
    async def generate():
        try:
            stream = ollama.chat(
                model="mistral",
                messages=[{"role": "user", "content": pregunta.pregunta}],
                stream=True,
                options={
                    "temperature": 0.7,
                    "num_thread": 4
                }
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            yield f"Error: {str(e)}"
    
    return StreamingResponse(generate(), media_type="text/plain")