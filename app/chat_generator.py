import ollama
import hashlib
from datetime import datetime, timedelta
from config_handler import config_handler

# Caché simple en memoria
_cache = {}

def generar_respuesta_chat(texto, config_params=None):
    """
    Toma una pregunta en lenguaje natural y genera una respuesta usando Ollama (Mistral).
    
    Args:
        texto (str): La pregunta en lenguaje natural.
        config_params (dict, optional): Parámetros de configuración personalizados.
    """
    print(f"Texto recibido en chat: {texto}")
    
    # Obtener parámetros de configuración
    params = config_handler.get_chat_params()
    
    # Actualizar con los parámetros personalizados
    if config_params:
        params.update(config_params)
    
    try:
        respuesta = ollama.chat(
            model="mistral",
            messages=[{
                "role": "user", 
                "content": texto
            }],
            options={
                "num_predict": params.get('num_predict', 100),
                "temperature": params.get('temperature', 0.7),
                "top_k": params.get('top_k', 40),
                "top_p": params.get('top_p', 0.9),
                "num_gpu": params.get('num_gpu', 1),
                "num_thread": params.get('num_thread', 4)
            }
        )

        # Obtener la respuesta
        contenido = respuesta["message"]["content"].strip()
        print(f"Respuesta generada: {contenido[:50]}...")
        
        return {
            "pregunta": texto,
            "respuesta": contenido
        }
            
    except Exception as e:
        print(f"Error al generar respuesta: {str(e)}")
        return {"error": f"Error al generar respuesta: {str(e)}"}

def generar_respuesta_chat_con_cache(texto, config_params=None):
    """
    Versión con caché de la función generar_respuesta_chat.
    
    Args:
        texto (str): La pregunta en lenguaje natural.
        config_params (dict, optional): Parámetros de configuración personalizados.
    """
    # Si hay configuración personalizada, no usar caché
    if config_params:
        return generar_respuesta_chat(texto, config_params)
    
    # Crear un hash de la consulta para usar como clave de caché
    texto_hash = hashlib.md5(texto.encode()).hexdigest()
    
    # Comprobar si está en caché y no ha expirado (caducidad de 1 hora)
    current_time = datetime.now()
    if texto_hash in _cache:
        cache_entry = _cache[texto_hash]
        if current_time - cache_entry["timestamp"] < timedelta(hours=1):
            print(f"Usando respuesta en caché para: {texto[:30]}...")
            return cache_entry["response"]
    
    # Si no está en caché o ha expirado, generar nueva respuesta
    response = generar_respuesta_chat(texto)
    
    # Guardar en caché
    _cache[texto_hash] = {
        "response": response,
        "timestamp": current_time
    }
    
    # Limitar tamaño del caché (máximo 100 entradas)
    if len(_cache) > 100:
        # Eliminar la entrada más antigua
        oldest_key = min(_cache.keys(), key=lambda k: _cache[k]["timestamp"])
        del _cache[oldest_key]
    
    return response