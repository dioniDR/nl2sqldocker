import ollama
import re
from config_handler import config_handler

def generar_sql_desde_texto(texto, config_params=None):
    """
    Toma una pregunta en lenguaje natural y genera una consulta SQL usando Ollama (Mistral).
    
    Args:
        texto (str): La pregunta en lenguaje natural.
        config_params (dict, optional): Parámetros de configuración personalizados.
    """
    print(f"Texto recibido: {texto}")
    
    # Obtener parámetros de configuración
    params = config_handler.get_sql_params()
    
    # Actualizar con los parámetros personalizados
    if config_params:
        params.update(config_params)
    
    try:
        respuesta = ollama.chat(
            model="mistral",
            messages=[{
                "role": "user", 
                "content": f"Genera SOLO una consulta SQL para MariaDB sin explicaciones adicionales. La consulta debe ser: {texto}"
            }],
            options={
                "num_predict": params.get('num_predict', 50),
                "temperature": params.get('temperature', 0.2),
                "top_k": params.get('top_k', 40),
                "top_p": params.get('top_p', 0.9),
                "num_gpu": params.get('num_gpu', 1),
                "num_thread": params.get('num_thread', 4)
            }
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