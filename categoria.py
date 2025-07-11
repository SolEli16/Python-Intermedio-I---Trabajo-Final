import sqlite3

class Categoria:
    def __init__(self, id_categoria=None, nombre=""):
        self.id_categoria = id_categoria
        self.nombre = nombre

    def __str__(self):
        return f"{self.nombre}"

    def guardar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Categorias (nombre) VALUES (?)", (self.nombre,))
        conn.commit()
        conn.close()

    def actualizar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE Categorias SET nombre = ? WHERE id_categoria = ?", (self.nombre, self.id_categoria))
        conn.commit()
        conn.close()

    def eliminar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categorias WHERE id_categoria = ?", (self.id_categoria,))
        conn.commit()
        conn.close()

    @staticmethod
    def resumen_ventas_por_categoria():
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, COUNT(v.id_venta), SUM(v.total)
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            JOIN categorias c ON p.id_categoria = c.id_categoria
            GROUP BY c.nombre
            ORDER BY SUM(v.total) DESC
        """)
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    @staticmethod
    def obtener_todas():
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        conn.close()
        return categorias
    
   