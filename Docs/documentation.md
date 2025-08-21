# 📦 Documentación de la Base de Datos – Asset Management System

## 📌 Descripción General
Este sistema de gestión de activos utiliza **PostgreSQL** como base de datos relacional.  
La estructura está diseñada para manejar **activos** de diferentes categorías, permitiendo almacenar información específica para cada tipo (computadoras, impresoras, periféricos) y mantener un **historial de cambios**.  
Además, incluye **gestión de usuarios** con roles y permisos.

---

## 🗂️ Diagrama ER (Mermaid)

```mermaid
erDiagram
    categorias_asset {
        int id_categoria PK
        varchar nombre
        text descripcion
    }

    assets {
        int id_asset PK
        int id_categoria FK
        varchar nombre_identificador
        date fecha_alta
        date fecha_baja
        varchar ubicacion
        text observaciones
    }

    assets_computadoras {
        int id_asset PK, FK
        varchar ip
        varchar motherboard
        varchar procesador
        varchar ram_tipo
        int ram_cantidad
        varchar ssd
        varchar hdd
        varchar placa_red_ext
    }

    assets_impresoras {
        int id_asset PK, FK
        varchar marca
        varchar modelo
        varchar nro_serie
        varchar ip
    }

    assets_perifericos {
        int id_asset PK, FK
        varchar tipo
        varchar marca
        date fecha_registro
        date fecha_entrega
    }

    usuarios {
        int id_usuario PK
        varchar nombre
        varchar email
        varchar password_hash
        varchar rol
    }

    historial_cambios {
        int id_historial PK
        int id_asset FK
        int id_usuario FK
        date fecha_cambio
        text descripcion_cambio
    }

    categorias_asset ||--o{ assets : "clasifica"
    assets ||--o{ assets_computadoras : "detalles si es computadora"
    assets ||--o{ assets_impresoras : "detalles si es impresora"
    assets ||--o{ assets_perifericos : "detalles si es periférico"
    assets ||--o{ historial_cambios : "registra"
    usuarios ||--o{ historial_cambios : "realiza"




## 📋 Tablas y Relaciones
1. categorias_asset
Contiene las categorías principales de activos.
Cada activo pertenece a una categoría.

Campo	Tipo	Descripción
id_categoria	PK, int	Identificador único de categoría
nombre	varchar	Nombre de la categoría
descripcion	text	Detalles de la categoría

2. assets (genérica)
Tabla principal para todos los activos.

Campo	Tipo	Descripción
id_asset	PK, int	Identificador único del activo
id_categoria	FK	Referencia a categorias_asset
nombre_identificador	varchar	Nombre o identificador del activo
fecha_alta	date	Fecha de alta (por defecto NOW)
fecha_baja	date	Fecha de baja (NULL si activo)
ubicacion	varchar	Ubicación física
observaciones	text	Comentarios

3. Tablas específicas de activos
Estas tablas extienden la información de assets según el tipo.

assets_computadoras
Campo	Tipo	Descripción
id_asset	PK, FK	Activo asociado
ip	varchar	Dirección IP
motherboard	varchar	Placa base
procesador	varchar	CPU
ram_tipo	varchar	Tipo de RAM
ram_cantidad	int	Cantidad de RAM
ssd	varchar	Capacidad SSD
hdd	varchar	Capacidad HDD
placa_red_ext	varchar	Tarjeta de red externa

assets_impresoras
Campo	Tipo	Descripción
id_asset	PK, FK	Activo asociado
marca	varchar	Marca
modelo	varchar	Modelo
nro_serie	varchar	Número de serie
ip	varchar	Dirección IP

assets_perifericos
Campo	Tipo	Descripción
id_asset	PK, FK	Activo asociado
tipo	varchar	Tipo de periférico
marca	varchar	Marca
fecha_registro	date	Fecha de registro
fecha_entrega	date	Fecha de entrega

4. usuarios
Maneja la autenticación y permisos.

Campo	Tipo	Descripción
id_usuario	PK, int	Identificador único
nombre	varchar	Nombre
email	varchar	Correo electrónico
password_hash	varchar	Contraseña cifrada
rol	varchar	Rol del usuario (lectura, lectura-escritura, admin)

5. historial_cambios
Registro de todas las modificaciones realizadas sobre los activos.

Campo	Tipo	Descripción
id_historial	PK, int	Identificador único
id_asset	FK	Activo afectado
id_usuario	FK	Usuario que hizo el cambio
fecha_cambio	date	Fecha del cambio
descripcion_cambio	text	Descripción de lo modificado

🔗 Relaciones Clave
1 categoría → N activos.

1 activo → 1 registro en tabla específica según categoría.

1 activo → N registros en historial de cambios.

1 usuario → N registros en historial de cambios.


--------------------------------------------------------------------------------

## Estructura propuesta para el proyecto

/mi_proyecto_assets
│
├── main.py                    # Punto de entrada
│
├── /database
│   ├── connection.py          # Conexión a SQLite
│   ├── create_db.py           # Crea las tablas
│   ├── create_admin.py        # Inserta el usuario admin por defecto
│
├── /ui
│   ├── login.py               # Pantalla de login
│   ├── main_window.py         # Pantalla principal
│   └── components/            # Widgets o pantallas reutilizables
│
├── data.db                    # Archivo SQLite (se crea en primera ejecución)
└── /Doc
    └── DB_Documentacion.md    # Documentación con diagrama ER y explicación
