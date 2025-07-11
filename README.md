Integrante: Carnascari Solange Elizabeth
Email: Solcarnascari@abc.gob.ar

# 📦 Gestor De Emprendimiento "Chucherías de Ensueño"

Sistema de escritorio para la gestión de productos, categorías y ventas, de un pequeño emprendimiento. 

## ✨ Características
- Interfaz gráfica intuitiva con `Tkinter`
- CRUD completo sobre las entidades: productos, ventas y categorías.
- Resumen de ventas por categoría.
- Validaciones inteligentes en la interfaz (ventas con productos eliminados, confirmaciones).
- Organización modular del código (`interfaz.py`, `models`, etc.).

## 🧰 Requisitos técnicos
- Python 3.12 (o superior recomendado)
- SQLite como motor de base de datos

Para poder ejecutar el sistema se deben guardar los archivos y carpetas de la siguiente manera:

GestorChucherriasDeEnsueño/
│
├── database/
       └── setup_db
├── requirements.txt
├── README.md
├── gui/
    ├── interfaz.py
    ├── gestor.db
    ├── crear_db
    └── models/
          ├── _init_.py
          ├── producto.py
          ├── venta.py
          ├── categoria.py
          └── _pycache_
                  ├── _init_.cpython-312.py
                  ├── producto.cpython-312.py
                  ├── categoria.cpython-312.py
                  └── venta.cpython-312
