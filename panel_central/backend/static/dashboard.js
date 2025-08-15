// Configuración global
const API_BASE = '';
let currentUser = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupNavigation();
    updateCurrentDate();
    loadOverviewData();
});

// Verificar autenticación
async function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    try {
        const response = await fetchWithAuth('/users/me');
        if (response.ok) {
            currentUser = await response.json();
            document.getElementById('userInfo').textContent = `Bienvenido, ${currentUser.username}`;
        } else {
            throw new Error('Token inválido');
        }
    } catch (error) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    }
}

// Función auxiliar para fetch con autenticación
async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    return fetch(url, {
        ...options,
        headers
    });
}

// Configurar navegación entre tabs
function setupNavigation() {
    document.querySelectorAll('[data-tab]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Actualizar enlaces activos
            document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
            
            // Mostrar tab correspondiente
            const tabName = this.dataset.tab;
            showTab(tabName);
            
            // Actualizar título
            const titles = {
                'overview': 'Resumen del Sistema',
                'inventario': 'Gestión de Inventario',
                'partidos': 'Partidos - API Sergio',
                'eventos': 'Eventos - API Andrea',
                'weather': 'Información Meteorológica'
            };
            document.getElementById('pageTitle').textContent = titles[tabName];
        });
    });
}

// Mostrar tab específico
function showTab(tabName) {
    // Ocultar todos los tabs
    document.querySelectorAll('.tab-pane').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar tab seleccionado
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Cargar datos específicos del tab
    switch(tabName) {
        case 'inventario':
            loadProductos();
            break;
        case 'partidos':
            loadPartidos();
            break;
        case 'eventos':
            loadEventos();
            break;
    }
}

// Actualizar fecha actual
function updateCurrentDate() {
    const now = new Date();
    document.getElementById('currentDate').textContent = now.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Cargar datos del resumen
async function loadOverviewData() {
    try {
        const response = await fetchWithAuth('/inventario/productos');
        if (response.ok) {
            const productos = await response.json();
            document.getElementById('totalProductos').textContent = productos.length;
        }
    } catch (error) {
        console.error('Error cargando datos del resumen:', error);
    }
}

// Gestión de productos
async function loadProductos() {
    try {
        const response = await fetchWithAuth('/inventario/productos');
        if (response.ok) {
            const productos = await response.json();
            const tbody = document.querySelector('#productosTable tbody');
            tbody.innerHTML = productos.map(producto => `
                <tr>
                    <td>${producto.id}</td>
                    <td>${producto.nombre}</td>
                    <td>$${producto.precio}</td>
                    <td>${producto.stock}</td>
                    <td>${producto.categoria || '-'}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="editProduct(${producto.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="deleteProduct(${producto.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        showAlert('Error cargando productos: ' + error.message);
    }
}

// Formulario de productos
document.getElementById('productoForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const productoData = {
        nombre: document.getElementById('prod-nombre').value,
        descripcion: document.getElementById('prod-descripcion').value,
        precio: parseFloat(document.getElementById('prod-precio').value),
        stock: parseInt(document.getElementById('prod-stock').value),
        categoria: document.getElementById('prod-categoria').value,
        proveedor: document.getElementById('prod-proveedor').value,
        codigo_barras: document.getElementById('prod-codigo').value
    };
    
    try {
        const response = await fetchWithAuth('/inventario/productos', {
            method: 'POST',
            body: JSON.stringify(productoData)
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('productoModal')).hide();
            document.getElementById('productoForm').reset();
            loadProductos();
            loadOverviewData();
            showAlert('Producto agregado exitosamente', 'success');
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Error al agregar producto');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message);
    }
});

// Eliminar producto
async function deleteProduct(productId) {
    if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        try {
            const response = await fetchWithAuth(`/inventario/productos/${productId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadProductos();
                loadOverviewData();
                showAlert('Producto eliminado exitosamente', 'success');
            }
        } catch (error) {
            showAlert('Error al eliminar producto: ' + error.message);
        }
    }
}

// Cargar partidos (API Sergio)
async function loadPartidos() {
    try {
        const response = await fetchWithAuth('/api/sergio/partidos/');
        if (response.ok) {
            const partidos = await response.json();
            const tbody = document.querySelector('#partidosTable tbody');
            tbody.innerHTML = partidos.map(partido => `
                <tr>
                    <td>${partido.id}</td>
                    <td>${partido.equipo_local}</td>
                    <td>${partido.equipo_visitante}</td>
                    <td>${partido.fecha}</td>
                    <td>${partido.estadio}</td>
                    <td>${partido.resultado || 'Por jugar'}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        showAlert('Error cargando partidos: ' + error.message);
    }
}

// Cargar eventos (API Andrea)
async function loadEventos() {
    try {
        const response = await fetchWithAuth('/api/andrea/eventos/');
        if (response.ok) {
            const eventos = await response.json();
            const tbody = document.querySelector('#eventosTable tbody');
            tbody.innerHTML = eventos.map(evento => `
                <tr>
                    <td>${evento.id}</td>
                    <td>${evento.nombre}</td>
                    <td>${evento.fecha}</td>
                    <td>${evento.lugar}</td>
                    <td>${evento.artista_principal || '-'}</td>
                    <td>$${evento.precio}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        showAlert('Error cargando eventos: ' + error.message);
    }
}


// Mostrar alertas
function showAlert(message, type = 'danger') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.content-area').insertBefore(alertDiv, document.querySelector('.content-area').firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Cerrar sesión
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}
