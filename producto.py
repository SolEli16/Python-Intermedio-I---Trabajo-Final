import sqlite3

class Producto:
    def __init__(self, id_producto=None, nombre="", precio=0.0, stock=0, id_categoria=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria

    def __str__(self):
        return f"{self.nombre} (${self.precio}) - Stock: {self.stock}"

    def guardar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Productos (nombre, precio, stock, id_categoria)
            VALUES (?, ?, ?, ?)""",
            (self.nombre, self.precio, self.stock, self.id_categoria))
        conn.commit()
        conn.close()

    def actualizar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Productos
            SET nombre = ?, precio = ?, stock = ?, id_categoria = ?
            WHERE id_producto = ?""",
            (self.nombre, self.precio, self.stock, self.id_categoria, self.id_producto))
        conn.commit()
        conn.close()

    def eliminar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Productos WHERE id_producto = ?", (self.id_producto,))
        conn.commit()
        conn.close()
        
    def descontar_stock(self, cantidad):
        self.stock -= cantidad
        self.actualizar()

    def recuperar_stock(self, cantidad):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET stock = stock + ? WHERE id_producto = ?", (cantidad, self.id_producto))
        conn.commit()
        conn.close()
    
    
    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productos")
        productos = cursor.fetchall()
        conn.close()
        return productos
    