# app/ai_providers/openai_provider.py
import os
import re
from openai import AsyncOpenAI
from typing import Dict, Any, AsyncGenerator, Optional
from .base_provider import AIProvider
from config_handler import config_handler

class OpenAIProvider(AIProvider):
    """Implementación del proveedor de IA basado en OpenAI."""
    
    def __init__(self):
        # Obtener API key de variables de entorno o archivo de configuración
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key de OpenAI no encontrada. Configure OPENAI_API_KEY en el entorno")
        
        # Crear cliente para OpenAI
        self.client = AsyncOpenAI(api_key=self.api_key)
        # Modelo por defecto - actualizable desde la configuración
        self.default_model = "gpt-4o"
    
    async def generate_sql(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una consulta SQL utilizando OpenAI.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para OpenAI
            
        Returns:
            Un diccionario con la consulta SQL o un mensaje de error
        """
        print(f"Texto recibido en OpenAI: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_sql_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        # Seleccionar modelo según la configuración
        model = config.get('model', self.default_model) if config else self.default_model
        
        try:
            # Crear el mensaje para OpenAI con instrucciones específicas para SQL
            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=params.get('num_predict', 200),
                temperature=params.get('temperature', 0.2),
                top_p=params.get('top_p', 0.9),
                messages=[
                    {"role": "system", "content": "Eres un generador de consultas SQL preciso. Genera SOLO código SQL sin explicaciones adicionales."},
                    {"role": "user", "content": f"Genera una consulta SQL para MariaDB que resuelva la siguiente petición: {query}. Solo devuelve el código SQL, sin comentarios ni explicaciones."}
                ]
            )

            # Extraer la respuesta
            contenido = response.choices[0].message.content.strip()
            
            # Limpiar posibles backticks de markdown
            contenido = re.sub(r'^```sql\s*', '', contenido)
            contenido = re.sub(r'```$', '', contenido)
            
            # Extraer solo la consulta SQL (la primera línea que empiece con SELECT)
            match = re.search(r'SELECT\s+.*?;', contenido, re.IGNORECASE | re.DOTALL)
            if match:
                consulta_sql = match.group(0)
                print(f"SQL generado por OpenAI: {consulta_sql}")
                return {"sql": consulta_sql}
            else:
                print(f"No se encontró una consulta SQL válida en OpenAI: {contenido}")
                return {"error": "No se pudo generar una consulta SQL válida"}
                
        except Exception as e:
            print(f"Error al generar SQL con OpenAI: {str(e)}")
            return {"error": f"Error al generar SQL con OpenAI: {str(e)}"}
    
    async def generate_chat_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de chat utilizando OpenAI.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para OpenAI
            
        Returns:
            Un diccionario con la respuesta
        """
        print(f"Texto recibido en chat OpenAI: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_chat_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        # Seleccionar modelo según la configuración
        model = config.get('model', self.default_model) if config else self.default_model
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                max_tokens=params.get('num_predict', 1024),
                temperature=params.get('temperature', 0.7),
                top_p=params.get('top_p', 0.9),
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y amigable."},
                    {"role": "user", "content": query}
                ]
            )

            # Extraer la respuesta
            contenido = response.choices[0].message.content
            print(f"Respuesta generada OpenAI: {contenido[:50]}...")
            
            return {
                "pregunta": query,
                "respuesta": contenido
            }
                
        except Exception as e:
            print(f"Error al generar respuesta con OpenAI: {str(e)}")
            return {"error": f"Error al generar respuesta con OpenAI: {str(e)}"}
    
    async def generate_stream_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Genera una respuesta de chat en modo streaming usando OpenAI.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional para OpenAI
            
        Returns:
            Un generador asíncrono que produce fragmentos de texto
        """
        # Obtener parámetros de configuración
        params = config_handler.get_chat_params()
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        # Seleccionar modelo según la configuración
        model = config.get('model', self.default_model) if config else self.default_model
        
        try:
            # Crear una sesión de streaming con OpenAI
            stream = await self.client.chat.completions.create(
                model=model,
                max_tokens=params.get('num_predict', 1024),
                temperature=params.get('temperature', 0.7),
                top_p=params.get('top_p', 0.9),
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y amigable."},
                    {"role": "user", "content": query}
                ],
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error al comunicarse con OpenAI: {str(e)}"
