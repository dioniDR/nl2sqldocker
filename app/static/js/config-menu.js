// Menú de configuración global para NL2SQL
document.addEventListener('DOMContentLoaded', function() {
    // Crear el elemento del menú de configuración si no existe
    if (!document.getElementById('config-menu-container')) {
        createConfigMenu();
    }
    
    // Cargar la configuración actual
    loadConfig();
    
    // Cargar los proveedores disponibles
    loadAvailableProviders();
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
            
            <!-- Selector de proveedor de IA -->
            <div class="mb-4">
                <h4 class="font-medium mb-2">Proveedor de IA</h4>
                <div id="providers-container" class="flex flex-col space-y-2">
                    <!-- Los proveedores se cargarán dinámicamente aquí -->
                    <div class="flex items-center">
                        <div class="animate-pulse bg-gray-200 h-5 w-full rounded"></div>
                    </div>
                </div>
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
                <div id="top_k_container">
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
                
                <!-- Num Thread - solo para Ollama -->
                <div id="num_thread_container">
                    <div class="flex justify-between">
                        <label for="num_thread" class="block text-sm font-medium">Hilos CPU: </label>
                        <span id="num_thread-value" class="text-sm font-mono">4</span>
                    </div>
                    <input type="range" id="num_thread" min="1" max="8" step="1" value="4" 
                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer">
                </div>
                
                <!-- Selector de modelo - se muestra según el proveedor -->
                <div id="model_selector_container" class="hidden">
                    <label for="model_selector" class="block text-sm font-medium mb-1">Modelo: </label>
                    <select id="model_selector" class="w-full p-2 border rounded text-sm">
                        <!-- Las opciones se cargarán dinámicamente según el proveedor -->
                    </select>
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
let currentProvider = 'ollama';
let config = {
    ai_provider: 'ollama',
    ollama: {
        model: 'mistral'
    },
    claude: {
        model: 'claude-3-opus-20240229'
    },
    openai: {
        model: 'gpt-4o'
    },
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

// Modelos disponibles para cada proveedor
const providerModels = {
    ollama: [
        { value: 'mistral', label: 'Mistral' },
        { value: 'llama2', label: 'Llama 2' },
        { value: 'llama3', label: 'Llama 3' }
    ],
    claude: [
        { value: 'claude-2.1', label: 'Claude 2.1' },
        { value: 'claude-2.0', label: 'Claude 2.0' },
        { value: 'claude-instant-1.2', label: 'Claude Instant 1.2' }
    ],
    openai: [
        { value: 'gpt-4o', label: 'GPT-4o' },
        { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
        { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' }
    ]
};

// Cargar los proveedores disponibles desde el servidor
async function loadAvailableProviders() {
    try {
        const response = await fetch('/api/providers');
        const data = await response.json();
        
        // Actualizar el contenedor de proveedores
        const container = document.getElementById('providers-container');
        container.innerHTML = '';
        
        // Configurar el proveedor activo
        currentProvider = data.active;
        
        // Crear botones de radio para cada proveedor
        for (const [key, provider] of Object.entries(data.providers)) {
            // Solo mostrar proveedores disponibles
            if (provider.available) {
                const radio = document.createElement('div');
                radio.className = 'flex items-center space-x-2 p-1';
                radio.innerHTML = `
                    <input type="radio" id="provider-${key}" name="provider" value="${key}" 
                           class="form-radio h-4 w-4 text-blue-600" ${key === currentProvider ? 'checked' : ''}>
                    <label for="provider-${key}" class="text-sm">${provider.name}</label>
                `;
                container.appendChild(radio);
                
                // Añadir evento de cambio
                radio.querySelector('input').addEventListener('change', function() {
                    setProvider(key);
                });
            }
        }
        
        // Actualizar la interfaz según el proveedor seleccionado
        updateProviderSpecificUI(currentProvider);
        
    } catch (error) {
        console.error('Error al cargar proveedores:', error);
    }
}

// Cargar configuración desde localStorage o servidor
function loadConfig() {
    // Intentar cargar desde localStorage
    const savedConfig = localStorage.getItem('nl2sql_config');
    if (savedConfig) {
        try {
            config = JSON.parse(savedConfig);
            console.log('Configuración cargada desde localStorage:', config);
            currentProvider = config.ai_provider || 'ollama';
        } catch (e) {
            console.error('Error al cargar configuración:', e);
        }
    } else {
        // Si no hay configuración guardada, cargar la configuración por defecto desde el servidor
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                config = data;
                currentProvider = config.ai_provider || 'ollama';
                console.log('Configuración cargada desde el servidor:', config);
                updateUIFromConfig();
                updateProviderSpecificUI(currentProvider);
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
    
    // Actualizar el selector de modelo si es necesario
    updateModelSelector();
}

// Actualizar controles específicos según el proveedor
function updateProviderSpecificUI(providerName) {
    // Mostrar/ocultar controles específicos de Ollama
    const isOllama = providerName === 'ollama';
    document.getElementById('top_k_container').style.display = isOllama ? 'block' : 'none';
    document.getElementById('num_thread_container').style.display = isOllama ? 'block' : 'none';
    
    // Mostrar/ocultar selector de modelo
    const modelContainer = document.getElementById('model_selector_container');
    modelContainer.classList.toggle('hidden', false); // Siempre mostrar el selector de modelo
    
    // Actualizar las opciones del selector de modelo
    updateModelSelector();
}

// Actualizar el selector de modelo según el proveedor actual
function updateModelSelector() {
    const modelSelector = document.getElementById('model_selector');
    modelSelector.innerHTML = '';
    
    // Obtener los modelos disponibles para el proveedor actual
    const models = providerModels[currentProvider] || [];
    
    // Obtener el modelo actual seleccionado en la configuración
    const currentModel = config[currentProvider]?.model || models[0]?.value;
    
    // Añadir opciones al selector
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = model.value;
        option.textContent = model.label;
        option.selected = model.value === currentModel;
        modelSelector.appendChild(option);
    });
    
    // Añadir evento de cambio
    modelSelector.addEventListener('change', function() {
        config[currentProvider] = config[currentProvider] || {};
        config[currentProvider].model = this.value;
    });
}

// Cambiar el tipo de configuración (SQL o Chat)
function setConfigType(type) {
    currentConfigType = type;
    updateUIFromConfig();
}

// Cambiar el proveedor de IA
function setProvider(providerName) {
    currentProvider = providerName;
    config.ai_provider = providerName;
    updateProviderSpecificUI(providerName);
}

// Restablecer a la configuración por defecto
function resetConfig() {
    // Solicitar la configuración por defecto al servidor
    fetch('/api/config/default')
        .then(response => response.json())
        .then(data => {
            config = data;
            currentProvider = config.ai_provider || 'ollama';
            localStorage.removeItem('nl2sql_config');
            updateUIFromConfig();
            updateProviderSpecificUI(currentProvider);
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
    ['temperature', 'top_p', 'num_predict'].forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            currentConfig[key] = parseFloat(input.value);
        }
    });
    
    // Añadir parámetros específicos de Ollama si es el proveedor actual
    if (currentProvider === 'ollama') {
        ['top_k', 'num_thread'].forEach(key => {
            const input = document.getElementById(key);
            if (input) {
                currentConfig[key] = parseInt(input.value);
            }
        });
    }
    
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
    
    // Crear configuración con los parámetros comunes
    const currentConfig = {
        ...config[configType],
        configType,
        provider: currentProvider
    };
    
    // Añadir configuración específica del proveedor
    if (config[currentProvider]) {
        currentConfig.model = config[currentProvider].model;
    }
    
    return currentConfig;
}

// Exponer función para obtener configuración
window.getAIConfig = getCurrentConfig;