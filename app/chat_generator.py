<script>
        // Variables para posicionar notas nuevas y llevar el z-index máximo
        let posX = 100;
        let posY = 100;
        let maxZIndex = 10;
        let currentNote = null;
        let activeConfigTag = null;
        let savedConfigs = [];
        let tasks = []; // Lista de tareas pendientes y completadas
        let taskIdCounter = 0; // Contador para generar IDs de tareas
        
        // Inicializar al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            setupDraggable();
            autoExpandTextarea();
            setupConfigSystem();
            setupTaskSystem();
            loadSavedConfigs();
            loadSavedTasks();
            
            // Configurar selectores de fuente
            document.getElementById('fontSelector').addEventListener('change', function() {
                if (!currentNote) return;
                
                // Eliminar clases de fuente anteriores
                const content = currentNote.querySelector('.nota-content');
                content.className = content.className
                    .replace(/font-\w+/g, '')
                    .trim();
                
                // Añadir nueva clase de fuente
                content.classList.add(this.value);
            });
            
            // Configurar selector de tamaño
            document.getElementById('fontSizeSelector').addEventListener('change', function() {
                if (!currentNote) return;
                
                // Eliminar clases de tamaño anteriores
                const content = currentNote.querySelector('.nota-content');
                content.className = content.className
                    .replace(/text-\w+/g, '')
                    .trim();
                
                // Añadir nueva clase de tamaño
                content.classList.add(this.value);
            });
        });
        
        // Permitir expandir el textarea automáticamente 
        function autoExpandTextarea() {
            const textarea = document.getElementById('textareaConsulta');
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                const newHeight = Math.min(this.scrollHeight, 150); // máximo 150px
                this.style.height = newHeight + 'px';
            });
        }

        // Configurar sistema de etiquetas de configuración
        function setupConfigSystem() {
            // Botón para abrir el modal de configuración
            document.getElementById('saveConfigBtn').addEventListener('click', function() {
                openConfigModal();
            });
            
            // Cerrar modal
            document.getElementById('closeConfigModal').addEventListener('click', closeConfigModal);
            document.getElementById('cancelConfigBtn').addEventListener('click', closeConfigModal);
            
            // Manejar selección de color
            const colorOptions = document.querySelectorAll('.color-option');
            colorOptions.forEach(option => {
                option.addEventListener('click', function() {
                    colorOptions.forEach(opt => opt.classList.remove('selected'));
                    this.classList.add('selected');
                });
            });
            
            // Actualizar valores de los sliders en tiempo real
            document.getElementById('tempRange').addEventListener('input', function() {
                document.getElementById('tempValue').textContent = this.value;
            });
            
            document.getElementById('maxTokensRange').addEventListener('input', function() {
                document.getElementById('maxTokensValue').textContent = this.value;
            });
            
            document.getElementById('topKRange').addEventListener('input', function() {
                document.getElementById('topKValue').textContent = this.value;
            });
            
            document.getElementById('topPRange').addEventListener('input', function() {
                document.getElementById('topPValue').textContent = this.value;
            });
            
            // Guardar configuración
            document.getElementById('saveConfigConfirmBtn').addEventListener('click', saveCurrentConfig);
        }
        
        // Configurar sistema de tareas
        function setupTaskSystem() {
            // Botón para ejecutar todas las tareas pendientes
            document.getElementById('runAllTasksBtn').addEventListener('click', runAllPendingTasks);
            
            // Botón para limpiar el historial
            document.getElementById('clearHistoryBtn').addEventListener('click', clearTaskHistory);
        }
        
        // Abrir modal de configuración
        function openConfigModal() {
            const modal = document.getElementById('configModal');
            modal.classList.add('active');
            
            // Pre-rellenar con la configuración actual si hay un tag activo
            if (activeConfigTag) {
                const config = savedConfigs.find(c => c.id === activeConfigTag);
                if (config) {
                    document.getElementById('configName').value = config.name;
                    document.querySelector(`input[name="configModel"][value="${config.model}"]`).checked = true;
                    
                    // Seleccionar el color
                    document.querySelectorAll('.color-option').forEach(opt => {
                        opt.classList.remove('selected');
                        if (opt.getAttribute('data-color') === config.color) {
                            opt.classList.add('selected');
                        }
                    });
                    
                    // Establecer valores de los sliders
                    document.getElementById('tempRange').value = config.temperature;
                    document.getElementById('tempValue').textContent = config.temperature;
                    
                    document.getElementById('maxTokensRange').value = config.maxTokens;
                    document.getElementById('maxTokensValue').textContent = config.maxTokens;
                    
                    document.getElementById('topKRange').value = config.topK;
                    document.getElementById('topKValue').textContent = config.topK;
                    
                    document.getElementById('topPRange').value = config.topP;
                    document.getElementById('topPValue').textContent = config.topP;
                }
            } else {
                // Resetear el formulario
                document.getElementById('configName').value = '';
                document.querySelector('input[name="configModel"][value="mistral"]').checked = true;
                
                document.querySelectorAll('.color-option').forEach((opt, index) => {
                    opt.classList.toggle('selected', index === 0);
                });
                
                document.getElementById('tempRange').value = 0.7;
                document.getElementById('tempValue').textContent = 0.7;
                
                document.getElementById('maxTokensRange').value = 100;
                document.getElementById('maxTokensValue').textContent = 100;
                
                document.getElementById('topKRange<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consultas Chat con IA</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Incluir Interact.js para el arrastre -->
    <script src="https://cdn.jsdelivr.net/npm/interactjs/dist/interact.min.js"></script>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Open+Sans&family=Montserrat&family=Lato&family=Source+Code+Pro&display=swap" rel="stylesheet">
    <style>
        body, html {
            height: 100%;
            margin: 0;
            overflow: hidden;
        }
        
        #tablero {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            min-width: 100vw;
            min-height: 100vh;
            overflow: auto;
        }
        
        #tablero-content {
            position: relative;
            min-width: 100%;
            min-height: 100%;
            width: 3000px;  /* Área expandible */
            height: 3000px; /* Área expandible */
        }
        
        .nota {
            cursor: move;
            position: absolute;
            min-width: 250px;
            max-width: 350px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10;
            touch-action: none; /* Importante para dispositivos táctiles */
            user-select: none;
        }
        
        .nota-header {
            cursor: move;
        }
        
        .nota-content {
            max-height: 150px;
            overflow-y: auto;
        }
        
        .entry-panel {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 600px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            z-index: 50;
            display: flex;
            flex-direction: column;
            padding: 10px;
            opacity: 0.95;
        }
        
        .entry-panel:hover {
            opacity: 1;
        }
        
        .config-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-bottom: 10px;
        }
        
        .config-tag {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s;
            color: white;
        }
        
        .config-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        .config-tag.active {
            box-shadow: 0 0 0 3px white, 0 0 0 5px currentColor;
        }
        
        .config-controls {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .entry-controls {
            display: flex;
            width: 100%;
        }
        
        .header-bar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 40;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Estilos para la lista de tareas */
        .task-list-container {
            background-color: rgba(255, 255, 255, 0.9);
            border-top: 1px solid #e5e7eb;
        }
        
        .task-list {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .task-item {
            display: flex;
            align-items: center;
            padding: 6px 8px;
            border-radius: 4px;
            transition: background-color 0.2s;
            font-size: 13px;
        }
        
        .task-item:hover {
            background-color: #f3f4f6;
        }
        
        .task-item.pending {
            border-left: 3px solid #fbbf24;
        }
        
        .task-item.processing {
            border-left: 3px solid #3b82f6;
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        .task-item.completed {
            border-left: 3px solid #10b981;
        }
        
        .task-item.error {
            border-left: 3px solid #ef4444;
        }
        
        .task-model-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 3px;
            margin-right: 8px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .task-model-badge.claude {
            background-color: #EF4444;
            color: white;
        }
        
        .task-model-badge.mistral {
            background-color: #22C55E;
            color: white;
        }
        
        .task-content {
            flex-grow: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .task-actions {
            display: flex;
            gap: 8px;
            opacity: 0.6;
        }
        
        .task-item:hover .task-actions {
            opacity: 1;
        }
        
        /* Modal de configuración */
        .config-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        
        .config-modal.active {
            opacity: 1;
            pointer-events: auto;
        }
        
        .config-modal-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 450px;
            max-height: 90vh;
            overflow-y: auto;
            transform: translateY(20px);
            transition: transform 0.3s;
        }
        
        .config-modal.active .config-modal-content {
            transform: translateY(0);
        }
        
        /* Color picker */
        .color-picker {
            display: flex;
            gap: 5px;
        }
        
        .color-option {
            width: 24px;
            height: 24px;
            border-radius: 4px;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .color-option.selected {
            border-color: #333;
        }
        
        /* Botones de tipo de consulta */
        #sqlTypeBtn, #chatTypeBtn {
            transition: all 0.2s;
        } white;
        }
        
        .task-content {
            flex-grow: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .task-actions {
            display: flex;
            gap: 8px;
            opacity: 0.6;
        }
        
        .task-item:hover .task-actions {
            opacity: 1;
        }
        
        .font-roboto { font-family: 'Roboto', sans-serif; }
        .font-opensans { font-family: 'Open Sans', sans-serif; }
        .font-montserrat { font-family: 'Montserrat', sans-serif; }
        .font-lato { font-family: 'Lato', sans-serif; }
        .font-sourcecode { font-family: 'Source Code Pro', monospace; }
        
        /* Estilos para la barra de scroll */
        .nota-content::-webkit-scrollbar {
            width: 8px;
        }
        .nota-content::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.05);
            border-radius: 4px;
        }
        .nota-content::-webkit-scrollbar-thumb {
            background: rgba(0,0,0,0.2);
            border-radius: 4px;
        }
        .nota-content::-webkit-scrollbar-thumb:hover {
            background: rgba(0,0,0,0.3);
        }
        
        /* Colores de fondo para las notas */
        .bg-yellow-light { background-color: #FFF9C4; }
        .bg-blue-light { background-color: #BBDEFB; }
        .bg-green-light { background-color: #C8E6C9; }
        .bg-pink-light { background-color: #F8BBD0; }
        .bg-purple-light { background-color: #E1BEE7; }
        .bg-orange-light { background-color: #FFE0B2; }
        .bg-teal-light { background-color: #B2DFDB; }
        
        /* Colores para los headers */
        .bg-yellow-header { background-color: #FBC02D; }
        .bg-blue-header { background-color: #42A5F5; }
        .bg-green-header { background-color: #66BB6A; }
        .bg-pink-header { background-color: #EC407A; }
        .bg-purple-header { background-color: #AB47BC; }
        .bg-orange-header { background-color: #FFA726; }
        .bg-teal-header { background-color: #26A69A; }
        
        /* Panel de personalización */
        .customization-panel {
            position: absolute;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            padding: 12px;
            z-index: 100;
            width: 180px;
            display: none;
        }
        
        /* Modal de configuración */
        .config-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }
        
        .config-modal.active {
            opacity: 1;
            pointer-events: auto;
        }
        
        .config-modal-content {
            background: white;
            padding: 20px;
            border-radius: 10px;
            width: 90%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            transform: translateY(20px);
            transition: transform 0.3s;
        }
        
        .config-modal.active .config-modal-content {
            transform: translateY(0);
        }
        
        /* Color picker */
        .color-picker {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 5px;
        }
        
        .color-option {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
        }
        
        .color-option.selected {
            border-color: #333;
        }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Barra de navegación superior -->
    <div class="header-bar">
        <h1 class="text-xl font-bold text-gray-800">Consultas Chat con IA</h1>
        <a href="/" class="text-blue-500 hover:text-blue-700">Volver a NL2SQL</a>
    </div>
    
    <!-- Tablero expandible con scroll -->
    <div id="tablero" class="bg-white">
        <div id="tablero-content">
            <!-- Las notas se añadirán aquí dinámicamente -->
        </div>
    </div>
    
    <!-- Panel de entrada persistente -->
    <div class="entry-panel">
        <!-- Etiquetas de configuración encima del área de texto -->
        <div class="config-tags" id="configTags">
            <!-- Aquí se mostrarán las etiquetas de configuración guardadas como botones de colores con letras C o M -->
        </div>
        
        <!-- Controles principales -->
        <div class="entry-controls">
            <div class="config-controls">
                <button id="configBtn" class="bg-gray-200 text-gray-700 px-3 py-2 rounded-lg hover:bg-gray-300 transition">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                </button>
            </div>
            <textarea 
                id="textareaConsulta"
                class="w-full p-2 border rounded-lg mx-2"
                placeholder="Escribe tu pregunta aquí..."
                rows="1"
            ></textarea>
            <button 
                id="botonEnviar"
                class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition whitespace-nowrap"
            >
                Enviar
            </button>
        </div>
        
        <!-- Lista de tareas pendientes / historial -->
        <div class="task-list-container mt-3 border-t pt-2">
            <div class="flex justify-between items-center mb-2">
                <h3 class="text-sm font-medium">Historial de consultas</h3>
                <div class="text-xs flex space-x-2">
                    <button id="runAllTasksBtn" class="text-blue-600 hover:text-blue-800">Ejecutar todo</button>
                    <button id="clearHistoryBtn" class="text-red-600 hover:text-red-800">Limpiar historial</button>
                </div>
            </div>
            <div id="taskList" class="task-list overflow-y-auto max-h-36">
                <!-- Tareas pendientes y completadas se mostrarán aquí -->
            </div>
        </div>
    </div>
    
    <!-- Modal para configuración -->
    <div id="configModal" class="config-modal">
        <div class="config-modal-content">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Configuración de IA</h3>
                <button id="closeConfigModal" class="text-gray-500 hover:text-gray-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-1">Proveedor de IA</label>
                <div class="flex space-x-2">
                    <label class="flex items-center">
                        <input type="radio" name="configModel" value="mistral" class="mr-1">
                        <span>Ollama (Mistral)</span>
                    </label>
                    <label class="flex items-center">
                        <input type="radio" name="configModel" value="claude" checked class="mr-1">
                        <span>Claude (Anthropic)</span>
                    </label>
                </div>
            </div>
            
            <div class="mb-4">
                <label class="block text-sm font-medium mb-1">Tipo de consulta</label>
                <div class="flex space-x-2">
                    <button id="sqlTypeBtn" class="px-4 py-1 rounded-md text-sm bg-gray-200 text-gray-700">SQL</button>
                    <button id="chatTypeBtn" class="px-4 py-1 rounded-md text-sm bg-blue-500 text-white">Chat</button>
                </div>
            </div>
            
            <div class="mb-4">
                <div class="flex justify-between">
                    <label for="tempRange" class="block text-sm font-medium mb-1">Temperatura:</label>
                    <span id="tempValue" class="text-sm font-mono">0.5</span>
                </div>
                <input type="range" id="tempRange" class="w-full" min="0" max="1" step="0.1" value="0.5">
                <div class="flex justify-between text-xs text-gray-500">
                    <span>Preciso</span>
                    <span>Creativo</span>
                </div>
            </div>
            
            <div class="mb-4">
                <div class="flex justify-between">
                    <label for="topPRange" class="block text-sm font-medium mb-1">Top P:</label>
                    <span id="topPValue" class="text-sm font-mono">0.7</span>
                </div>
                <input type="range" id="topPRange" class="w-full" min="0.1" max="1" step="0.05" value="0.7">
            </div>
            
            <div class="mb-4">
                <div class="flex justify-between">
                    <label for="maxTokensRange" class="block text-sm font-medium mb-1">Longitud máxima:</label>
                    <span id="maxTokensValue" class="text-sm font-mono">220</span>
                </div>
                <input type="range" id="maxTokensRange" class="w-full" min="10" max="500" step="10" value="220">
            </div>
            
            <div class="mb-4">
                <label for="modelVersion" class="block text-sm font-medium mb-1">Modelo:</label>
                <select id="modelVersion" class="w-full p-2 border rounded-lg">
                    <option value="claude-2.1">Claude 2.1</option>
                    <option value="claude-3-haiku">Claude 3 Haiku</option>
                    <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                    <option value="claude-3-opus">Claude 3 Opus</option>
                </select>
            </div>
            
            <div class="mb-4">
                <label for="configName" class="block text-sm font-medium mb-1">Guardar como:</label>
                <div class="flex space-x-2">
                    <input type="text" id="configName" placeholder="Nombre de la configuración" class="w-full p-2 border rounded-lg">
                    <div class="color-picker flex space-x-1">
                        <div class="color-option selected" style="background-color: #EF4444;" data-color="#EF4444"></div>
                        <div class="color-option" style="background-color: #22C55E;" data-color="#22C55E"></div>
                        <div class="color-option" style="background-color: #F59E0B;" data-color="#F59E0B"></div>
                    </div>
                </div>
            </div>
            
            <div class="flex justify-between mt-6">
                <button id="resetConfigBtn" class="text-sm text-gray-600 hover:text-red-500">
                    Restablecer
                </button>
                <div>
                    <button id="cancelConfigBtn" class="text-gray-600 mr-2 px-4 py-2 rounded-lg hover:bg-gray-100">Cancelar</button>
                    <button id="saveConfigBtn" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Guardar</button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Panel de personalización de notas -->
    <div id="customizePanel" class="customization-panel">
        <h4 class="font-semibold mb-2">Personalizar Nota</h4>
        
        <div class="mb-2">
            <label class="block text-sm mb-1">Color de fondo:</label>
            <div class="flex flex-wrap gap-1">
                <div class="w-5 h-5 bg-yellow-light cursor-pointer rounded" onclick="cambiarColor('yellow')"></div>
                <div class="w-5 h-5 bg-blue-light cursor-pointer rounded" onclick="cambiarColor('blue')"></div>
                <div class="w-5 h-5 bg-green-light cursor-pointer rounded" onclick="cambiarColor('green')"></div>
                <div class="w-5 h-5 bg-pink-light cursor-pointer rounded" onclick="cambiarColor('pink')"></div>
                <div class="w-5 h-5 bg-purple-light cursor-pointer rounded" onclick="cambiarColor('purple')"></div>
                <div class="w-5 h-5 bg-orange-light cursor-pointer rounded" onclick="cambiarColor('orange')"></div>
                <div class="w-5 h-5 bg-teal-light cursor-pointer rounded" onclick="cambiarColor('teal')"></div>
            </div>
        </div>
        
        <div class="mb-2">
            <label class="block text-sm mb-1">Tipo de fuente:</label>
            <select id="fontSelector" class="w-full text-sm p-1 border rounded">
                <option value="font-roboto">Roboto</option>
                <option value="font-opensans">Open Sans</option>
                <option value="font-montserrat">Montserrat</option>
                <option value="font-lato">Lato</option>
                <option value="font-sourcecode">Source Code</option>
            </select>
        </div>
        
        <div class="mb-2">
            <label class="block text-sm mb-1">Tamaño:</label>
            <select id="fontSizeSelector" class="w-full text-sm p-1 border rounded">
                <option value="text-xs">Pequeño</option>
                <option value="text-sm" selected>Mediano</option>
                <option value="text-base">Normal</option>
                <option value="text-lg">Grande</option>
            </select>
        </div>
    </div>

    <script>
        // Variables para posicionar notas nuevas y llevar el z-index máximo
        let posX = 100;
        let posY = 100;
        let maxZIndex = 10;
        let currentNote = null;
        
        // Configurar interact.js para hacer las notas arrastrables
        function setupDraggable() {
            interact('.nota').draggable({
                inertia: true,
                autoScroll: true,
                listeners: {
                    start: function(event) {
                        // Al empezar a arrastrar, traer al frente
                        const target = event.target;
                        bringToFront(target);
                    },
                    move: dragMoveListener,
                    end: checkTableroSize
                }
            });
        }
        
        function dragMoveListener(event) {
            const target = event.target;
            
            // Obtener posición actual
            const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
            const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
            
            // Actualizar posición
            target.style.transform = `translate(${x}px, ${y}px)`;
            
            // Almacenar posición como atributos
            target.setAttribute('data-x', x);
            target.setAttribute('data-y', y);
            
            // Auto-scroll si se acerca a los bordes
            const tablero = document.getElementById('tablero');
            const rect = target.getBoundingClientRect();
            
            if (rect.right > tablero.clientWidth - 50) {
                tablero.scrollLeft += 10;
            } else if (rect.left < 50) {
                tablero.scrollLeft -= 10;
            }
            
            if (rect.bottom > tablero.clientHeight - 50) {
                tablero.scrollTop += 10;
            } else if (rect.top < 50) {
                tablero.scrollTop -= 10;
            }
        }
        
        // Función para comprobar y ajustar el tamaño del tablero si es necesario
        function checkTableroSize() {
            const tableroContent = document.getElementById('tablero-content');
            const notas = document.querySelectorAll('.nota');
            let maxRight = 0;
            let maxBottom = 0;
            
            notas.forEach(nota => {
                const rect = nota.getBoundingClientRect();
                const x = (parseFloat(nota.getAttribute('data-x')) || 0);
                const y = (parseFloat(nota.getAttribute('data-y')) || 0);
                
                const rightEdge = x + rect.width;
                const bottomEdge = y + rect.height;
                
                maxRight = Math.max(maxRight, rightEdge);
                maxBottom = Math.max(maxBottom, bottomEdge);
            });
            
            // Añadir margen extra
            maxRight += 500;
            maxBottom += 500;
            
            // Ajustar el tamaño del tablero si es necesario
            if (maxRight > tableroContent.offsetWidth) {
                tableroContent.style.width = maxRight + 'px';
            }
            
            if (maxBottom > tableroContent.offsetHeight) {
                tableroContent.style.height = maxBottom + 'px';
            }
        }
        
        // Función para traer una nota al frente
        function bringToFront(element) {
            maxZIndex += 1;
            element.style.zIndex = maxZIndex;
        }
        
        // Función para mostrar el panel de personalización
        function mostrarPanelPersonalizacion(nota, event) {
            event.preventDefault();
            event.stopPropagation();
            
            const panel = document.getElementById('customizePanel');
            const rect = nota.getBoundingClientRect();
            
            // Posicionar el panel cerca de la nota
            panel.style.left = `${rect.right + 10}px`;
            panel.style.top = `${rect.top}px`;
            panel.style.display = 'block';
            
            currentNote = nota;
            
            // Cerrar el panel al hacer clic fuera de él
            setTimeout(() => {
                document.addEventListener('click', cerrarPanelPersonalizacion);
            }, 100);
        }
        
        function cerrarPanelPersonalizacion(event) {
            const panel = document.getElementById('customizePanel');
            if (!panel.contains(event.target)) {
                panel.style.display = 'none';
                document.removeEventListener('click', cerrarPanelPersonalizacion);
            }
        }
        
        // Función para cambiar el color de la nota
        function cambiarColor(color) {
            if (!currentNote) return;
            
            // Eliminar clases de color anteriores
            currentNote.className = currentNote.className
                .replace(/bg-\w+-light/g, '')
                .trim();
                
            // Obtener el header
            const header = currentNote.querySelector('.nota-header');
            header.className = header.className
                .replace(/bg-\w+-header/g, '')
                .trim();
            
            // Añadir nuevas clases de color
            currentNote.classList.add(`bg-${color}-light`);
            header.classList.add(`bg-${color}-header`);
        }
        
        // Permitir expandir el textarea automáticamente 
        function autoExpandTextarea() {
            const textarea = document.getElementById('textareaConsulta');
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                const newHeight = Math.min(this.scrollHeight, 150); // máximo 150px
                this.style.height = newHeight + 'px';
            });
        }
        
        // Inicializar al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            setupDraggable();
            autoExpandTextarea();
            
            // Configurar selectores de fuente
            document.getElementById('fontSelector').addEventListener('change', function() {
                if (!currentNote) return;
                
                // Eliminar clases de fuente anteriores
                const content = currentNote.querySelector('.nota-content');
                content.className = content.className
                    .replace(/font-\w+/g, '')
                    .trim();
                
                // Añadir nueva clase de fuente
                content.classList.add(this.value);
            });
            
            // Configurar selector de tamaño
            document.getElementById('fontSizeSelector').addEventListener('change', function() {
                if (!currentNote) return;
                
                // Eliminar clases de tamaño anteriores
                const content = currentNote.querySelector('.nota-content');
                content.className = content.className
                    .replace(/text-\w+/g, '')
                    .trim();
                
                // Añadir nueva clase de tamaño
                content.classList.add(this.value);
            });
        });

        // Permitir enviar con Enter
        document.getElementById('textareaConsulta').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const pregunta = this.value.trim();
                if (pregunta) {
                    agregarConsultaACola(pregunta);
                }
            }
        });
        
        // Cola de consultas pendientes
        let consultasPendientes = [];
        let procesandoConsulta = false;
        
        // Función para añadir una consulta a la cola
        function agregarConsultaACola(texto) {
            if (texto.trim() === '') return;
            
            consultasPendientes.push(texto);
            procesarSiguienteConsulta();
        }
        
        // Función para procesar la siguiente consulta en la cola
        function procesarSiguienteConsulta() {
            if (procesandoConsulta || consultasPendientes.length === 0) return;
            
            procesandoConsulta = true;
            const siguienteConsulta = consultasPendientes.shift();
            enviarConsultaChatStream(siguienteConsulta);
        }
        
        async function enviarConsultaChatStream(preguntaTexto = null) {
            // Si no se proporciona texto, usar el del textarea
            const pregunta = preguntaTexto || document.getElementById('textareaConsulta').value.trim();
            
            if (!pregunta) {
                procesandoConsulta = false;
                return;
            }
            
            // Limpiar el textarea inmediatamente después de obtener el texto
            if (!preguntaTexto) {
                document.getElementById('textareaConsulta').value = '';
                document.getElementById('textareaConsulta').style.height = 'auto';
                document.getElementById('textareaConsulta').focus();
            }
            
            const button = document.getElementById('botonEnviar');
            button.disabled = true;
            button.innerText = 'Enviando...';
            
            // Obtener el modelo seleccionado
            const modeloSeleccionado = document.getElementById('modelSelector').value;

            try {
                // Obtener la configuración actual
                const config = window.getAIConfig ? window.getAIConfig() : {};
                
                // Crear un contenedor para la nota antes de empezar el streaming
                const id = 'nota_' + Date.now();
                const nota = document.createElement('div');
                nota.id = id;
                nota.className = 'nota bg-yellow-light rounded-lg overflow-hidden';
                nota.style.left = `${posX}px`;
                nota.style.top = `${posY}px`;
                nota.style.zIndex = maxZIndex;
                
                // Determinar el título según el modelo
                const modeloTitulo = modeloSeleccionado === 'claude' ? 'Claude' : 'Mistral';
                
                nota.innerHTML = `
                    <div class="nota-header bg-yellow-header p-2 flex justify-between items-center">
                        <span class="font-semibold">Consulta (${modeloTitulo})</span>
                        <div class="flex space-x-2">
                            <button class="personalizar-nota text-blue-600 hover:text-blue-800">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                                </svg>
                            </button>
                            <button class="eliminar-nota text-red-500 hover:text-red-700">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>
                    </div>
                    <div class="p-3">
                        <div class="text-sm font-medium mb-2">${pregunta}</div>
                        <div class="border-t border-yellow-300 my-2"></div>
                        <div id="response-${id}" class="nota-content text-sm font-roboto whitespace-pre-wrap">Generando respuesta...</div>
                    </div>
                `;
                
                document.getElementById('tablero-content').appendChild(nota);
                
                // Configurar click para traer al frente
                nota.addEventListener('mousedown', function() {
                    bringToFront(nota);
                });
                
                // Configurar el botón de personalización
                nota.querySelector('.personalizar-nota').addEventListener('click', function(event) {
                    mostrarPanelPersonalizacion(nota, event);
                });
                
                // Configurar eliminación
                nota.querySelector('.eliminar-nota').addEventListener('click', function() {
                    document.getElementById(id).remove();
                });
                
                // Actualizar posición para la próxima nota
                posX += 30;
                posY += 30;
                if (posX > 300) {
                    posX = 100;
                    posY = 100;
                }
                
                // Incrementar el z-index máximo
                maxZIndex++;
                
                // Hacer la nota arrastrable
                setupDraggable();
                
                // Verificar el tamaño del tablero
                checkTableroSize();
                
                // Determinar el endpoint según el modelo seleccionado
                let endpoint = '/consulta_chat_stream/';
                
                // Si es Claude, se debería usar otro endpoint (ajustar según la API real)
                if (modeloSeleccionado === 'claude') {
                    // Aquí deberías tener un endpoint para Claude, por ahora usamos el mismo
                    endpoint = '/consulta_chat_stream/';
                    // Añadir indicación de que es para Claude en el cuerpo
                    config.useClaudeModel = true;
                }
                
                // Iniciar streaming
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        pregunta: pregunta,
                        config: config,
                        modelo: modeloSeleccionado
                    })
                });

                const responseElem = document.getElementById(`response-${id}`);
                responseElem.textContent = ""; // Limpiar mensaje de "Generando..."
                
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const {value, done} = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    responseElem.textContent += chunk;
                    // Auto-scroll al fondo de la nota
                    responseElem.scrollTop = responseElem.scrollHeight;
                }
                
            } catch (error) {
                alert('Error de conexión: ' + error.message);
            } finally {
                button.disabled = false;
                button.innerText = 'Enviar';
                procesandoConsulta = false;
                
                // Procesar la siguiente consulta en la cola, si hay alguna
                procesarSiguienteConsulta();
            }
        }

        // Usar la versión streaming con manejo de cola
        document.getElementById('botonEnviar').addEventListener('click', function() {
            const pregunta = document.getElementById('textareaConsulta').value.trim();
            if (pregunta) {
                agregarConsultaACola(pregunta);
            }
        });
    </script>
    
    <!-- Incluir el menú de configuración global -->
    <script src="/static/js/config-menu.js"></script>
</body>
</html>