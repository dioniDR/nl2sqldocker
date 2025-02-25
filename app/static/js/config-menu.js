// Menú de configuración global para NL2SQL
document.addEventListener('DOMContentLoaded', function() {
    // Crear el elemento del menú de configuración si no existe
    if (!document.getElementById('config-menu-container')) {
        createConfigMenu();
    }
    
    // Cargar la configuración actual
    loadConfig();
});

// Crear el menú de configuración
function createConfigMenu() {
    const menuHTML = `
    <div id="config-menu-container" class="fixed bottom-4 left-4 z-50">
        <button id="config-toggle-btn" class="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
        </button>
        
        <div id="config-panel" class="hidden bg-white rounded-lg shadow-xl p-6 absolute bottom-16 left-0 w-80">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Configuración de IA</h3>
                <button id="close-config-btn" class="text-gray-500 hover:text-gray-700">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            
            <div class="mb-4">
                <div class="flex justify-between">
                    <h4 class="font-medium mb-2">Tipo de consulta</h4>
                    <span id="config-type-indicator" class="text-xs text-blue-500">SQL</span>
                </div>
                <div class="flex space-x-2 mb-4">
                    <button id="sql-config-btn" class="bg-blue-500 text-white px-4 py-1 rounded-md text-sm">SQL</button>
                    <button id="chat-config-btn" class="bg-gray-200 text-gray-700 px-4 py-1 rounded-md text-sm">Chat</button>
                </div>
            </div>
            
            <!-- Controles de configuración -->
            <div class="space-y-4">
                <!-- Temperatura -->
                <div>
                    <div class="flex justify-between">
                        <label for="temperature" class="block text-sm font-medium">Temperatura: </label>
                        <span id="temperature-value" class="text-sm font-mono">0.2</span>
                    </div>
                    <input type="range" id="temperature" min="0" max="1" step="0.1" value="0.2" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                    <div class="flex justify-between text-xs text-gray-500">
                        <span>Preciso</span>
                        <span>Creativo</span>
                    </div>
                </div>
                
                <!-- Top K -->
                <div>
                    <div class="flex justify-between">
                        <label for="top_k" class="block text-sm font-medium">Top K: </label>
                        <span id="top_k-value" class="text-sm font-mono">40</span>
                    </div>
                    <input type="range" id="top_k" min="1" max="100" step="1" value="40" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                </div>
                
                <!-- Top P -->
                <div>
                    <div class="flex justify-between">
                        <label for="top_p" class="block text-sm font-medium">Top P: </label>
                        <span id="top_p-value" class="text-sm font-mono">0.9</span>
                    </div>
                    <input type="range" id="top_p" min="0.1" max="1" step="0.05" value="0.9" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                </div>
                
                <!-- Num Predict -->
                <div>
                    <div class="flex justify-between">
                        <label for="num_predict" class="block text-sm font-medium">Longitud máxima: </label>
                        <span id="num_predict-value" class="text-sm font-mono">50</span>
                    </div>
                    <input type="range" id="num_predict" min="10" max="500" step="10" value="50" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                </div>
                
                <!-- Num Thread -->
                <div>
                    <div class="flex justify-between">
                        <label for="num_thread" class="block text-sm font-medium">Hilos CPU: </label>
                        <span id="num_thread-value" class="text-sm font-mono">4</span>
                    </div>
                    <input type="range" id="num_thread" min="1" max="8" step="1" value="4" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                </div>
            </div>
            
            <div class="flex justify-between mt-6">
                <button id="reset-config-btn" class="text-sm text-gray-600 hover:text-red-500">
                    Restablecer
                </button>
                <button id="save-config-btn" class="bg-blue-500 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-600">
                    Guardar
                </button>
            </div>
        </div>
    </div>
    `;
    
    // Insertar el menú en el documento
    const div = document.createElement('div');
    div.innerHTML = menuHTML;
    document.body.appendChild(div.firstElementChild);
    
    // Configurar eventos
    setupConfigEvents();
}

// Configurar los eventos del menú
function setupConfigEvents() {
    // Mostrar/ocultar el panel de configuración
    document.getElementById('config-toggle-btn').addEventListener('click', function() {
        const panel = document.getElementById('config-panel');
        panel.classList.toggle('hidden');
    });
    
    // Cerrar el panel
    document.getElementById('close-config-btn').addEventListener('click', function() {
        document.getElementById('config-panel').classList.add('hidden');
    });
    
    // Cambiar entre configuración SQL y Chat
    document.getElementById('sql-config-btn').addEventListener('click', function() {
        setConfigType('sql');
    });
    
    document.getElementById('chat-config-btn').addEventListener('click', function() {
        setConfigType('chat');
    });
    
    // Actualizar valores en tiempo real
    document.querySelectorAll('#config-panel input[type="range"]').forEach(input => {
        input.addEventListener('input', function() {
            document.getElementById(`${this.id}-value`).textContent = this.value;
        });
    });
    
    // Botón de restablecer
    document.getElementById('reset-config-btn').addEventListener('click', function() {
        resetConfig();
    });
    
    // Botón de guardar
    document.getElementById('save-config-btn').addEventListener('click', function() {
        saveConfig();
    });
}

// Variables globales para la configuración
let currentConfigType = 'sql';
let config = {
    sql: {
        temperature: 0.2,
        top_k: 40,
        top_p: 0.9,
        num_predict: 50,
        num_thread: 4
    },
    chat: {
        temperature: 0.7,
        top_k: 40,
        top_p: 0.9,
        num_predict: 100,
        num_thread: 4
    }
};

// Cargar configuración desde localStorage o servidor
function loadConfig() {
    // Intentar cargar desde localStorage
    const savedConfig = localStorage.getItem('nl2sql_config');
    if (savedConfig) {
        try {
            config = JSON.parse(savedConfig);
            console.log('Configuración cargada desde localStorage:', config);
        } catch (e) {
            console.error('Error al cargar configuración:', e);
        }
    } else {
        // Si no hay configuración guardada, cargar la configuración por defecto desde el servidor
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                config = data;
                console.log('Configuración cargada desde el servidor:', config);
                updateUIFromConfig();
            })
            .catch(error => {
                console.error('Error al cargar configuración desde el servidor:', error);
            });
    }
    
    // Actualizar la UI con la configuración cargada
    updateUIFromConfig();
}

// Actualizar la UI con la configuración actual
function updateUIFromConfig() {
    const currentConfig = config[currentConfigType];
    
    // Actualizar cada control con su valor correspondiente
    for (const [key, value] of Object.entries(currentConfig)) {
        const input = document.getElementById(key);
        const valueDisplay = document.getElementById(`${key}-value`);
        
        if (input && valueDisplay) {
            input.value = value;
            valueDisplay.textContent = value;
        }
    }
    
    // Actualizar los botones de tipo
    document.getElementById('sql-config-btn').className = 
        currentConfigType === 'sql' ? 'bg-blue-500 text-white px-4 py-1 rounded-md text-sm' : 'bg-gray-200 text-gray-700 px-4 py-1 rounded-md text-sm';
    
    document.getElementById('chat-config-btn').className = 
        currentConfigType === 'chat' ? 'bg-blue-500 text-white px-4 py-1 rounded-md text-sm' : 'bg-gray-200 text-gray-700 px-4 py-1 rounded-md text-sm';
    
    // Actualizar el indicador de tipo
    document.getElementById('config-type-indicator').textContent = currentConfigType.toUpperCase();
}

// Cambiar el tipo de configuración (SQL o Chat)
function setConfigType(type) {
    currentConfigType = type;
    updateUIFromConfig();
}

// Restablecer a la configuración por defecto
function resetConfig() {
    // Solicitar la configuración por defecto al servidor
    fetch('/api/config/default')
        .then(response => response.json())
        .then(data => {
            config = data;
            localStorage.removeItem('nl2sql_config');
            updateUIFromConfig();
            alert('Configuración restablecida a valores predeterminados');
        })
        .catch(error => {
            console.error('Error al restablecer configuración:', error);
            alert('Error al restablecer la configuración');
        });
}

// Guardar la configuración actual
function saveConfig() {
    // Obtener los valores actuales de todos los controles
    const currentConfig = {};
    ['temperature', 'top_k', 'top_p', 'num_predict', 'num_thread'].forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            currentConfig[key] = parseFloat(input.value);
        }
    });
    
    // Actualizar el objeto de configuración
    config[currentConfigType] = currentConfig;
    
    // Guardar en localStorage
    localStorage.setItem('nl2sql_config', JSON.stringify(config));
    
    // Enviar al servidor
    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Configuración guardada:', data);
        alert('Configuración guardada correctamente');
    })
    .catch(error => {
        console.error('Error al guardar configuración:', error);
        alert('Configuración guardada localmente, pero no se pudo sincronizar con el servidor');
    });
}

// Obtener la configuración actual para usarla en las consultas
function getCurrentConfig() {
    // Determinar el tipo de configuración según la página actual
    const isChat = window.location.href.includes('consultas_chat');
    const configType = isChat ? 'chat' : 'sql';
    
    return {
        ...config[configType],
        configType
    };
}

// Exponer función para obtener configuración
window.getAIConfig = getCurrentConfig;