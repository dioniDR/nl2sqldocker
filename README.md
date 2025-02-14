# NL2SQL - Consultas SQL con Lenguaje Natural

Aplicación web que convierte consultas en lenguaje natural a SQL usando Ollama y MariaDB.

## 🚀 Inicio Rápido

1. **Iniciar los servicios con Docker**
```bash
docker compose up -d
Esto iniciará:

MariaDB (Puerto 3306)
Ollama (Puerto 11434)
Interfaz Web (Puerto 8000)


Descargar el modelo de Ollama

bashCopydocker exec -it ollama-service ollama pull mistral
💡 Ejemplo de Uso

Abre el navegador en http://localhost:8000
Escribe tu consulta en lenguaje natural, por ejemplo:

"muéstrame todos los usuarios"
"usuarios activos"
"buscar por email"


La aplicación convertirá tu consulta a SQL y mostrará los resultados

📊 Base de Datos
La aplicación usa MariaDB con una tabla de usuarios que incluye:

id
nombre
email
fecha_registro
estado

🔧 Puertos

MariaDB: 3306
Ollama: 11434
Interfaz Web: 8000

📝 Estado Actual

✅ Consultas básicas funcionando
✅ Interfaz web simple
✅ Integración con MariaDB
✅ Procesamiento de lenguaje natural