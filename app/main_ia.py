from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text  # Añadir esta importación
from database_ia import SessionLocalIA
from sql_generator import generar_sql_desde_texto
from pydantic import BaseModel

app = FastAPI(title="API SQL IA")

# Montar directorio estático
app.mount("/static", StaticFiles(directory="."), name="static")

# Añadir ruta para el index.html
@app.get("/")
async def read_index():
    return FileResponse('index.html')

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