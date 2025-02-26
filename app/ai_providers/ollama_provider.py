# app/ai_providers/ollama_provider.py
import ollama
import re
from typing import Dict, Any, AsyncGenerator, Optional
from .base_provider import AIProvider
from config_handler import config_handler

class OllamaProvider(AIProvider):
    """Implementación del proveedor de IA basado en Ollama (Mistral)."""
    
    async def generate_sql(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una consulta SQL utilizando Ollama/Mistral.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para Ollama
            
        Returns:
            Un diccionario con la consulta SQL o un mensaje de error
        """
        print(f"Texto recibido en Ollama: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_sql_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        try:
            respuesta = ollama.chat(
                model="mistral",
                messages=[{
                    "role": "user", 
                    "content": f"Genera SOLO una consulta SQL para MariaDB sin explicaciones adicionales. La consulta debe ser: {query}"
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
    
    async def generate_chat_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de chat utilizando Ollama/Mistral.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para Ollama
            
        Returns:
            Un diccionario con la respuesta
        """
        print(f"Texto recibido en chat Ollama: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_chat_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        try:
            respuesta = ollama.chat(
                model="mistral",
                messages=[{
                    "role": "user", 
                    "content": query
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
            print(f"Respuesta generada Ollama: {contenido[:50]}...")
            
            return {
                "pregunta": query,
                "respuesta": contenido
            }
                
        except Exception as e:
            print(f"Error al generar respuesta: {str(e)}")
            return {"error": f"Error al generar respuesta: {str(e)}"}
    
    async def generate_stream_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Genera una respuesta de chat en modo streaming usando Ollama/Mistral.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para Ollama
            
        Returns:
            Un generador asíncrono que produce fragmentos de texto
        """
        # Obtener parámetros de configuración
        params = config_handler.get_chat_params()
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        try:
            stream = ollama.chat(
                model="mistral",
                messages=[{"role": "user", "content": query}],
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
