import ollama
import re

def generar_sql_desde_texto(texto):
    """
    Toma una pregunta en lenguaje natural y genera una consulta SQL usando Ollama (Mistral).
    """
    print(f"Texto recibido: {texto}")
    
    try:
        respuesta = ollama.chat(
            model="mistral",
            messages=[{
                "role": "user", 
                "content": f"Genera SOLO una consulta SQL para MariaDB sin explicaciones adicionales. La consulta debe ser: {texto}"
            }]
        )

        # Obtener la respuesta
        contenido = respuesta["message"]["content"].strip()
        
        # Extraer solo la consulta SQL (la primera línea que empiece con SELECT)
        match = re.search(r'SELECT\s+.*?;', contenido, re.IGNORECASE | re.DOTALL)
        if match:
            consulta_sql = match.group(0)
            print(f"SQL generado: {consulta_sql}")
            return {"sql": consulta_sql}
        else:
            print(f"No se encontró una consulta SQL válida en: {contenido}")
            return {"error": "No se pudo generar una consulta SQL válida"}
            
    except Exception as e:
        print(f"Error al generar SQL: {str(e)}")
        return {"error": f"Error al generar SQL: {str(e)}"}