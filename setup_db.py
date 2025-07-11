import sqlite3

def crear_tablas():
    conn = sqlite3.connect("gestor.db")
    cursor = conn.cursor()

    # Crear tabla Categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        );
    """)

    # Crear tabla Productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            id_categoria INTEGER NOT NULL,
            FOREIGN KEY (id_categoria) REFERENCES Categorias(id_categoria)
        );
    """)

    # Crear tabla Ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada correctamente.")

# Ejecutar la función al correr el script
if __name__ == "__main__":
    crear_tablas()