# MACUIN — Sistema de Gestión de Autopartes

Arquitectura: **FastAPI** (API + BD) · **Flask** (frontend admin) · **Laravel** (frontend cliente) · **Docker**

## Estructura del repositorio

```
macuin/
├── api/                        ← FastAPI — toda la lógica y acceso a BD
│   ├── app/
│   │   ├── main.py
│   │   ├── data/
│   │   │   ├── db.py           ← Conexión SQLAlchemy
│   │   │   └── models.py       ← Modelos ORM
│   │   ├── schemas/
│   │   │   └── schemas.py      ← Validación Pydantic
│   │   └── routers/
│   │       ├── autopartes.py   ← CRUD autopartes
│   │       ├── usuarios.py     ← CRUD usuarios + /registro
│   │       ├── pedidos.py      ← Pedidos 1-N productos
│   │       └── reportes.py     ← PDF, XLSX, DOCX
│   ├── Dockerfile
│   └── requirements.txt
│
├── flask-frontend/             ← Flask — panel admin interno
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py           ← Rutas (consume API)
│   │   ├── services.py         ← Cliente HTTP para la API
│   │   ├── templates/
│   │   └── static/
│   ├── run.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── laravel-frontend/           ← Laravel — tienda para clientes
│   ├── app/
│   │   ├── Http/Controllers/
│   │   │   ├── CatalogoController.php
│   │   │   ├── AuthController.php
│   │   │   └── PedidoController.php
│   │   └── Services/
│   │       └── ApiService.php  ← Cliente HTTP para la API
│   ├── routes/web.php
│   └── resources/views/
│
├── docker-compose.yml          ← Levanta todo junto
└── .env.example
```

## Puertos

| Servicio      | Puerto | Descripción                        |
|---------------|--------|------------------------------------|
| FastAPI       | 8000   | API REST + Swagger en /docs        |
| Flask         | 5000   | Panel admin (autopartes, usuarios) |
| Laravel/Nginx | 8080   | Tienda para clientes               |
| PostgreSQL    | 5432   | Base de datos (solo accede la API) |

## Cómo levantar el proyecto

### Requisitos
- Docker Desktop instalado y corriendo
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/macuin.git
cd macuin

# 2. Levantar todos los contenedores
docker-compose up --build

# 3. (Primera vez) Crear base de datos SQLite para Laravel
docker exec macuin_laravel touch /tmp/laravel.sqlite
docker exec macuin_laravel php artisan migrate --force
```

### Acceder a los servicios

- **API Swagger**: http://localhost:8000/docs
- **Flask Admin**: http://localhost:5000
- **Laravel Tienda**: http://localhost:8080

## Endpoints de la API

### Autopartes
| Método | Endpoint              | Descripción         |
|--------|-----------------------|---------------------|
| GET    | /v1/autopartes/       | Listar todas        |
| GET    | /v1/autopartes/{id}   | Obtener una         |
| POST   | /v1/autopartes/       | Crear               |
| PUT    | /v1/autopartes/{id}   | Actualizar          |
| DELETE | /v1/autopartes/{id}   | Eliminar            |

### Usuarios
| Método | Endpoint              | Descripción                    |
|--------|-----------------------|--------------------------------|
| GET    | /v1/usuarios/         | Listar todos                   |
| GET    | /v1/usuarios/{id}     | Obtener uno                    |
| POST   | /v1/usuarios/         | Crear (admin)                  |
| POST   | /v1/usuarios/registro | Registro externo (desde Laravel)|
| PUT    | /v1/usuarios/{id}     | Actualizar                     |
| DELETE | /v1/usuarios/{id}     | Eliminar                       |

### Pedidos
| Método | Endpoint                        | Descripción                  |
|--------|---------------------------------|------------------------------|
| POST   | /v1/pedidos/                    | Crear pedido (1-N productos) |
| GET    | /v1/pedidos/                    | Listar todos (admin)         |
| GET    | /v1/pedidos/{id}                | Detalle de un pedido         |
| GET    | /v1/pedidos/usuario/{id}        | Pedidos por usuario          |

### Reportes (PDF, XLSX, DOCX)
| Endpoint                        | Descripción              |
|---------------------------------|--------------------------|
| /v1/reportes/inventario/{fmt}   | Inventario completo      |
| /v1/reportes/bajo-stock/{fmt}   | Stock bajo (< 10 units)  |
| /v1/reportes/ventas/{fmt}       | Historial de pedidos     |
| /v1/reportes/top-productos/{fmt}| Top 10 más vendidos      |

`{fmt}` puede ser: `pdf`, `xlsx`, `docx`
