# Pokédex Django (Python)

Este es un proyecto web construido como challenge tecnico creado con Django que simula una Pokédex. Incluye gestión de usuarios con roles (admin, editor, viewer) y un reproductor de audio que suena en el fondo.

---

## 🚀 Tecnologías utilizadas

- Python 3.12+
- Django 5.2.3
- MySQL (mediante Laragon)
- HTML5 / CSS3
- JavaScript (mínimo)
- phpMyAdmin (para gestión de la base de datos)
- Entorno: VS Code

---

## ✨ Características

- Registro, login y logout de usuarios.
- Roles de usuario: admin, editor y viewer.
- Panel de administración para crear, editar, listar y eliminar usuarios (solo admins).
- Gestión de permisos para mostrar opciones según rol.
- Reproductor de audio que puede activarse/desactivarse en cualquier página.
- Visualización de Pokémon en un grid responsive.
- Uso de sesiones para mantener la información del usuario.
- Manejo de mensajes de error y éxito con Django messages framework.
- Estilo simple y limpio con CSS integrado.

---

## 🛠️ Requisitos previos

1. Tener instalado **Laragon** o bien:
   - MySQL 8+
   - PHP + phpMyAdmin (si no usás Laragon)
2. Tener Python 3.12 o superior
3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   pip install django mysqlclient
   ```

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/alexnoire89/pokedex.git
   cd pokedex
   ```

2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv env

   # En Windows
   env\Scripts\activate

   # En Linux / Mac
   source env/bin/activate
   ```

---

## 🧩 Configuración de la base de datos

0. Instalar Laragon: https://github.com/leokhoa/laragon/releases/download/8.2.1/laragon-wamp.exe
1. Abrir Laragon y asegurarse de que MySQL y Apache estén encendidos.
2. Ir a http://localhost/phpmyadmin
3. Crear una base de datos llamada **pokedex**
4. Asegurarse de que `settings.py` tenga la siguiente configuración:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pokedex',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

5. Ejecutar las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Iniciar el servidor:
   ```bash
   python manage.py runserver
   ```

7. Abrir el navegador en http://localhost:8000/inicio/

---

## 📁 Estructura del proyecto

```
pokedex/
├── usuarios/               # App principal (usuarios y autenticación)
├── templates/              # Plantillas HTML
├── static/
│   └── audio/              # Contiene pokemon_song.mp3
├── pokedex/settings.py     # Configuración general
└── ...
```

---

## 🔎 Notas

- 🎵 El audio puede no reproducirse automáticamente con sonido en algunos navegadores (por restricciones de autoplay).
- 🔐 El sistema de permisos es simple y se basa en roles y sesiones guardados en la base de datos.
- 🧪 Se recomienda usar un entorno virtual para manejar las dependencias correctamente.

---

## 👤 Autor

**Alex Noire**  
Proyecto creado como Challenge Técnico.  
Repositorio: [https://github.com/alexnoire89/pokedex](https://github.com/alexnoire89/pokedex)
