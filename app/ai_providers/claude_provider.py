# app/ai_providers/claude_provider.py
import os
import re
import anthropic
from typing import Dict, Any, AsyncGenerator, Optional
from .base_provider import AIProvider
from config_handler import config_handler

class ClaudeProvider(AIProvider):
    """Implementación del proveedor de IA basado en Claude de Anthropic."""
    
    def __init__(self):
        # Obtener API key de variables de entorno o archivo de configuración
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key de Anthropic no encontrada. Configure ANTHROPIC_API_KEY en el entorno")
        
        # Crear cliente para Claude
        self.client = anthropic.Anthropic(api_key=self.api_key)
        # Modelo por defecto - actualizable desde la configuración
        self.default_model = "claude-2.1"  # Cambiar a Claude 2.1
    
    async def generate_sql(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una consulta SQL utilizando Claude.
        """
        print(f"Texto recibido en Claude: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_sql_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        # Seleccionar modelo según la configuración
        model = config.get('model', self.default_model) if config else self.default_model
        
        try:
            # Crear el mensaje para Claude con instrucciones específicas para SQL
            prompt = f"""Genera SOLO una consulta SQL para MariaDB, sin explicaciones ni texto adicional. 
            La consulta debe resolver esta petición: {query}
            
            Reglas:
            - Genera SOLO código SQL, sin comentarios introductorios ni explicaciones
            - La consulta debe comenzar con SELECT
            - Termina la consulta con punto y coma (;)
            - Utiliza la sintaxis compatible con MariaDB
            - NO incluyas comillas, markdown, ni otros formatos alrededor del SQL"""
            
            completion = self.client.completions.create(
                model=model,
                max_tokens_to_sample=params.get('num_predict', 200),  # Cambiado aquí
                temperature=params.get('temperature', 0.2),
                top_p=params.get('top_p', 0.9),
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:"
            )

            # Extraer la respuesta
            contenido = completion.completion
            
            # Extraer solo la consulta SQL (la primera línea que empiece con SELECT)
            match = re.search(r'SELECT\s+.*?;', contenido, re.IGNORECASE | re.DOTALL)
            if match:
                consulta_sql = match.group(0)
                print(f"SQL generado por Claude: {consulta_sql}")
                return {"sql": consulta_sql}
            else:
                print(f"No se encontró una consulta SQL válida en Claude: {contenido}")
                return {"error": "No se pudo generar una consulta SQL válida"}
                
        except Exception as e:
            print(f"Error al generar SQL con Claude: {str(e)}")
            return {"error": f"Error al generar SQL con Claude: {str(e)}"}
    
    async def generate_chat_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de chat utilizando Claude.
        """
        print(f"Texto recibido en chat Claude: {query}")
        
        # Obtener parámetros de configuración
        params = config_handler.get_chat_params()
        
        # Actualizar con los parámetros personalizados
        if config:
            params.update(config)
        
        # Seleccionar modelo según la configuración
        model = config.get('model', self.default_model) if config else self.default_model
        
        try:
            completion = self.client.completions.create(
                model=model,
                # Usar max_tokens_to_sample en lugar de max_tokens
                max_tokens_to_sample=params.get('num_predict', 1024),
                temperature=params.get('temperature', 0.7),
                top_p=params.get('top_p', 0.9),
                prompt=f"\n\nHuman: {query}\n\nAssistant:"
            )

            # Extraer la respuesta
            contenido = completion.completion
            print(f"Respuesta generada Claude: {contenido[:50]}...")
            
            return {
                "pregunta": query,
                "respuesta": contenido
            }
                
        except Exception as e:
            print(f"Error al generar respuesta con Claude: {str(e)}")
            return {"error": f"Error al generar respuesta con Claude: {str(e)}"}
    
    async def generate_stream_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Versión simplificada para streaming (usa la API regular)
        """
        try:
            # Obtener una respuesta completa y devolverla
            respuesta = await self.generate_chat_response(query, config)
            
            # Si hay un error, devolver el mensaje de error
            if "error" in respuesta:
                yield respuesta["error"]
            else:
                # Sino, devolver la respuesta completa
                yield respuesta["respuesta"]
                
        except Exception as e:
            error_msg = f"Error al comunicarse con Claude: {str(e)}"
            print(error_msg)
            yield error_msg