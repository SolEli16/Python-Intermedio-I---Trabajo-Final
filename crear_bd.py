import sqlite3

def crear_tablas():
    conn = sqlite3.connect("gestor.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL,
        id_categoria INTEGER,
        FOREIGN KEY(id_categoria) REFERENCES Categorias(id_categoria)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        id_producto INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        total REAL NOT NULL,
        cliente TEXT,
        FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
    )
    """)

    conn.commit()
    conn.close()
    print("✔ Tablas creadas correctamente.")

crear_tablas()