# app/ai_providers/base_provider.py
from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator, Optional

class AIProvider(ABC):
    """Clase base abstracta para todos los proveedores de IA."""
    
    @abstractmethod
    async def generate_sql(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una consulta SQL a partir de una consulta en lenguaje natural.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional específica para el proveedor
            
        Returns:
            Un diccionario con la consulta SQL o un mensaje de error
        """
        pass
    
    @abstractmethod
    async def generate_chat_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una respuesta de chat a partir de una consulta en lenguaje natural.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional específica para el proveedor
            
        Returns:
            Un diccionario con la respuesta
        """
        pass
    
    @abstractmethod
    async def generate_stream_response(self, query: str, config: Optional[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        Genera una respuesta de chat en modo streaming.
        
        Args:
            query: La consulta en lenguaje natural
            config: Configuración opcional específica para el proveedor
            
        Returns:
            Un generador asíncrono que produce fragmentos de texto
        """
        pass
    
    @staticmethod
    def get_provider(provider_name: str) -> 'AIProvider':
        """
        Factory method para obtener el proveedor adecuado.
        
        Args:
            provider_name: Nombre del proveedor ('ollama', 'claude', 'openai')
            
        Returns:
            Una instancia del proveedor solicitado
        """
        if provider_name == "ollama":
            from .ollama_provider import OllamaProvider
            return OllamaProvider()
        elif provider_name == "claude":
            from .claude_provider import ClaudeProvider
            return ClaudeProvider()
        elif provider_name == "openai":
            from .openai_provider import OpenAIProvider
            return OpenAIProvider()
        else:
            raise ValueError(f"Proveedor de IA no reconocido: {provider_name}")
