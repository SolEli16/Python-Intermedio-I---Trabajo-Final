import sqlite3
from datetime import datetime

class Venta:
    def __init__(self, id_venta=None, fecha=None, id_producto=None, cantidad=0, total=0.0, cliente=""):
        self.id_venta = id_venta
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.total = total
        self.cliente = cliente

    def guardar(self):
        conn = sqlite3.connect("gestor.db")  # Usá el nombre de tu base real
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ventas (fecha, id_producto, cantidad, total, cliente)
            VALUES (?, ?, ?, ?, ?)
        """, (self.fecha, self.id_producto, self.cantidad, self.total, self.cliente))
        conn.commit()
        conn.close()

    def actualizar(self):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ventas
            SET fecha = ?, id_producto = ?, cantidad = ?, total = ?, cliente = ?
            WHERE id_venta = ?
        """, (self.fecha, self.id_producto, self.cantidad, self.total, self.cliente, self.id_venta))
        conn.commit()
        conn.close()

    # En venta.py
    @staticmethod
    def eliminar(id_venta):
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventas WHERE id_venta = ?", (id_venta,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todas():
        conn = sqlite3.connect("gestor.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id_venta, fecha, id_producto, cantidad, total, cliente FROM ventas")
        ventas = cursor.fetchall()
        conn.close()
        return ventas
    
    