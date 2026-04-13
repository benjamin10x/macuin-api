# Macuin Laravel

Aplicación web desarrollada con **Laravel** que se ejecuta mediante **contenedores Docker**, lo que permite levantar el entorno completo de desarrollo de forma rápida y consistente.

El sistema utiliza múltiples servicios para su funcionamiento, incluyendo **Nginx como servidor web, PHP para la ejecución de Laravel, PostgreSQL como base de datos y Node.js para la compilación de assets del frontend**.

---

# Tecnologías utilizadas

* Laravel
* PHP 8.3
* Nginx
* PostgreSQL
* Node.js
* Docker
* Docker Compose

---

# Arquitectura del sistema

El proyecto está compuesto por los siguientes contenedores Docker:

| Servicio    | Descripción                                        |
| ----------- | -------------------------------------------------- |
| Nginx       | Servidor web que gestiona las peticiones HTTP      |
| Laravel App | Contenedor que ejecuta PHP y la aplicación Laravel |
| PostgreSQL  | Base de datos del sistema                          |
| Node        | Entorno para compilar assets frontend              |

---

# Requisitos

Antes de ejecutar el proyecto es necesario tener instalado:

* Docker
* Docker Desktop
* Docker Compose
* Git

---

# Instalación del proyecto

## 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/macuin-laravel.git
cd macuin-laravel
```

---

## 2. Construir y levantar los contenedores

Ejecutar el siguiente comando para construir las imágenes y levantar los servicios:

```bash
docker compose up -d --build
```

Este proceso descargará las imágenes necesarias y creará los contenedores definidos en `docker-compose.yml`.

---

# Configuración de Laravel

Una vez levantados los contenedores es necesario configurar la aplicación Laravel.

## 1. Acceder al contenedor de la aplicación

```bash
docker exec -it laravel_app bash
```

---

## 2. Instalar dependencias

```bash
composer install
```

---

## 3. Crear archivo de variables de entorno

```bash
cp .env.example .env
```

---

## 4. Generar la clave de la aplicación

```bash
php artisan key:generate
```

---

## 5. Ejecutar migraciones

```bash
php artisan migrate
```

---

# Acceso a la aplicación

Una vez que todos los contenedores estén ejecutándose correctamente, la aplicación puede visualizarse en:

http://localhost:8000

---

# Servicios Docker

El proyecto utiliza los siguientes servicios y puertos:

| Servicio    | Imagen             | Puerto  |
| ----------- | ------------------ | ------- |
| Nginx       | nginx:1.27-alpine  | 8000    |
| PostgreSQL  | postgres:16-alpine | 5432    |
| Node        | node:22-alpine     | 5173    |
| Laravel App | php:8.3-fpm        | interno |

---

# Comandos útiles

## Ver contenedores activos

```bash
docker ps
```

## Ver logs de un contenedor

```bash
docker logs laravel_nginx
```

## Acceder al contenedor de Laravel

```bash
docker exec -it laravel_app bash
```

---

# Detener el proyecto

Para detener todos los contenedores ejecutar:

```bash
docker compose down
```

---

# Autor

Proyecto académico desarrollado utilizando **Laravel y Docker** para demostrar la implementación de aplicaciones web con entornos containerizados.
