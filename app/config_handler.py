# app/config_handler.py
import yaml
import os
from typing import Dict, Any

# Clase para manejar la configuración
class ConfigHandler:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigHandler, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Carga la configuración desde el archivo YAML."""
        config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            print(f"Error al cargar la configuración: {str(e)}")
            # Configuración por defecto en caso de error
            self.config = {
                'ai_provider': 'ollama',
                'ollama': {'modelo': 'mistral', 'host': 'http://ollama:11434'},
                'claude': {'model': 'claude-3-opus-20240229'},
                'openai': {'model': 'gpt-4o'},
                'sql': {
                    'num_predict': 50,
                    'temperature': 0.2,
                    'top_k': 40,
                    'top_p': 0.9,
                    'num_gpu': 1,
                    'num_thread': 4
                },
                'chat': {
                    'num_predict': 100,
                    'temperature': 0.7,
                    'top_k': 40,
                    'top_p': 0.9,
                    'num_gpu': 1,
                    'num_thread': 4
                }
            }
    
    def get_config(self) -> Dict[str, Any]:
        """Devuelve la configuración completa."""
        return self.config
    
    def get_sql_params(self) -> Dict[str, Any]:
        """Devuelve los parámetros para generación de SQL."""
        return self.config.get('sql', {})
    
    def get_chat_params(self) -> Dict[str, Any]:
        """Devuelve los parámetros para generación de chat."""
        return self.config.get('chat', {})
    
    def get_active_provider(self) -> str:
        """Devuelve el proveedor de IA activo."""
        return self.config.get('ai_provider', 'ollama')
    
    def get_provider_config(self, provider_name=None) -> Dict[str, Any]:
        """Devuelve la configuración para un proveedor específico."""
        if provider_name is None:
            provider_name = self.get_active_provider()
        
        return self.config.get(provider_name, {})
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """Actualiza la configuración con nuevos valores."""
        # Actualizamos solo los campos que vienen en new_config
        if 'sql' in new_config:
            self.config['sql'].update(new_config['sql'])
        if 'chat' in new_config:
            self.config['chat'].update(new_config['chat'])
        if 'ai_provider' in new_config:
            self.config['ai_provider'] = new_config['ai_provider']
        
        # Actualizamos configuraciones específicas de proveedores
        for provider in ['ollama', 'claude', 'openai']:
            if provider in new_config:
                self.config.setdefault(provider, {})
                self.config[provider].update(new_config[provider])
    
    def save_config(self) -> None:
        """Guarda la configuración actual en el archivo YAML."""
        config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
        try:
            with open(config_path, 'w') as file:
                yaml.dump(self.config, file, default_flow_style=False)
            print("Configuración guardada correctamente")
        except Exception as e:
            print(f"Error al guardar la configuración: {str(e)}")

# Instancia global
config_handler = ConfigHandler()
