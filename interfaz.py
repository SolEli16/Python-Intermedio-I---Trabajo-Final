import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk, messagebox
from models.categoria import Categoria
from models.producto import Producto
from models.venta import Venta
from tkinter import *

class GestorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Chucherías de Ensueño")
        self.root.geometry("800x600")  # Ajustalo al tamaño deseado

        label_titulo = tk.Label(self.root, text="Resumen de Ventas", font=("Calibri", 18), bg="white")
        label_titulo.place(x=100, y=30)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Crear pestañas
        self.tab_categorias = tk.Frame(self.notebook, bg="blue")
        self.tab_productos = tk.Frame(self.notebook, bg="blue")
        self.tab_eliminar = tk.Frame(self.notebook, bg="blue")
        self.tab_ventas = tk.Frame(self.notebook, bg="blue")
        self.tab_resumen = tk.Frame(self.notebook, bg="blue")

        
        self.notebook.add(self.tab_categorias, text="Categorías")
        self.notebook.add(self.tab_productos, text="Productos")
        self.notebook.add(self.tab_eliminar, text="Eliminar productos")
        self.notebook.add(self.tab_ventas, text="Ventas")
        self.notebook.add(self.tab_resumen, text="Resumen por Categoría")
        
        self.formulario_categorias()
        self.formulario_productos()
        self.formulario_ventas()
        self.formulario_resumen_categoria()
    # ---------------- CATEGORÍAS ----------------
    def formulario_categorias(self):
        lbl = tk.Label(self.tab_categorias, text="Nombre de la categoría:")
        lbl.pack(pady=5)

        self.entry_cat_nombre = tk.Entry(self.tab_categorias)
        self.entry_cat_nombre.pack(pady=5)

        btn_guardar = tk.Button(self.tab_categorias, text="Guardar", command=self.guardar_categoria)
        btn_guardar.pack(pady=5)

        self.lista_categorias = tk.Listbox(self.tab_categorias)
        self.lista_categorias.pack(pady=10, fill="both", expand=True)
        self.lista_categorias.bind("<<ListboxSelect>>", self.seleccionar_categoria)

        btn_actualizar = tk.Button(self.tab_categorias, text="Actualizar", command=self.actualizar_categoria)
        btn_actualizar.pack(pady=3)

        btn_eliminar = tk.Button(self.tab_categorias, text="Eliminar", command=self.eliminar_categoria)
        btn_eliminar.pack(pady=3)

        self.recargar_lista_categorias()

    def guardar_categoria(self):
        nombre = self.entry_cat_nombre.get()
        if nombre:
            cat = Categoria(nombre=nombre)
            cat.guardar()
            messagebox.showinfo("✔", "Categoría guardada.")
            self.entry_cat_nombre.delete(0, tk.END)
            self.recargar_lista_categorias()
            self.cargar_categorias_combo()
        else:
            messagebox.showwarning("⚠️", "Ingresá un nombre.")

    def seleccionar_categoria(self, event):
        seleccion = self.lista_categorias.curselection()
        if seleccion:
            texto = self.lista_categorias.get(seleccion[0])
            id_cat = int(texto.split(" - ")[0])
            datos = [c for c in Categoria.obtener_todas() if c[0] == id_cat][0]
            self.entry_cat_nombre.delete(0, tk.END)
            self.entry_cat_nombre.insert(0, datos[1])
            self.cat_seleccionada = Categoria(*datos)

    def actualizar_categoria(self):
        if hasattr(self, "cat_seleccionada"):
            self.cat_seleccionada.nombre = self.entry_cat_nombre.get()
            self.cat_seleccionada.actualizar()
            messagebox.showinfo("✔", "Categoría actualizada.")
            self.entry_cat_nombre.delete(0, tk.END)
            self.recargar_lista_categorias()
            self.cargar_categorias_combo()

    def eliminar_categoria(self):
        if hasattr(self, "cat_seleccionada"):
            confirmar = messagebox.askyesno("Eliminar", "¿Eliminar esta categoría?")
            if confirmar:
                self.cat_seleccionada.eliminar()
                self.entry_cat_nombre.delete(0, tk.END)
                self.recargar_lista_categorias()
                self.cargar_categorias_combo()
                del self.cat_seleccionada

    def recargar_lista_categorias(self):
        self.lista_categorias.delete(0, tk.END)
        for c in Categoria.obtener_todas():
            self.lista_categorias.insert(tk.END, f"{c[0]} - {c[1]}")

    # ---------------- PRODUCTOS ----------------
    def formulario_productos(self):
        lbl_cat = tk.Label(self.tab_productos, text="Categoría:")
        lbl_cat.pack(pady=3)

        self.combo_categoria = ttk.Combobox(self.tab_productos, state="readonly")
        self.combo_categoria.pack(pady=3)

        self.categorias_dict = {}
        self.cargar_categorias_combo()

        campos = [("Nombre del producto", "entry_nombre"), ("Precio", "entry_precio"), ("Stock", "entry_stock")]
        for texto, attr in campos:
            lbl = tk.Label(self.tab_productos, text=texto)
            lbl.pack(pady=3)
            entry = tk.Entry(self.tab_productos)
            entry.pack(pady=3)
            setattr(self, attr, entry)

        btn_guardar = tk.Button(self.tab_productos, text="Guardar producto", command=self.guardar_producto)
        btn_guardar.pack(pady=5)

        btn_ir_eliminar = tk.Button(self.tab_productos, text="¿Eliminar producto?", command=self.ir_a_eliminar_tab)
        btn_ir_eliminar.pack(pady=5)

        for campo in [self.entry_nombre, self.entry_precio, self.entry_stock]:
            campo.delete(0, tk.END)
        self.combo_categoria.set("")

    def cargar_categorias_combo(self):
        categorias = Categoria.obtener_todas()
        nombres = []
        for c in categorias:
            self.categorias_dict[c[1]] = c[0]
            nombres.append(c[1])
        self.combo_categoria["values"] = nombres
        if nombres:
            self.combo_categoria.current(0)

    def guardar_producto(self):
        try:
            nombre = self.entry_nombre.get()
            precio = float(self.entry_precio.get())
            stock = int(self.entry_stock.get())
            categoria_id = self.categorias_dict.get(self.combo_categoria.get())

            if not nombre or categoria_id is None:
                raise ValueError("Faltan datos")

            # Uso de argumentos nombrados para evitar desorden
            producto = Producto(
                nombre=nombre,
                precio=precio,
                stock=stock,
                id_categoria=categoria_id
            )
            producto.guardar()
            messagebox.showinfo("✔", "Producto guardado correctamente.")

            # Limpieza de campos
            for campo in [self.entry_nombre, self.entry_precio, self.entry_stock]:
                campo.delete(0, tk.END)
            self.combo_categoria.set("")
        except ValueError:
            messagebox.showerror("❌", "Completá todos los campos correctamente.")
            self.productos_dict = {}  # Limpiar por si hay duplicados
            self.cargar_productos_combo()  # Vuelve a llenar el dict y los nombres

            self.combo_venta_producto["values"] = list(self.productos_dict.keys())  # Refresca visualmente
            self.combo_venta_producto.set("")  # Borra selección anterior


    def ir_a_eliminar_tab(self):
        self.notebook.select(self.tab_eliminar)
        self.mostrar_lista_para_eliminar()

    def mostrar_lista_para_eliminar(self):
        for widget in self.tab_eliminar.winfo_children():
            widget.destroy()

        lbl_info = tk.Label(self.tab_eliminar, text="Seleccioná un producto para eliminar:")
        lbl_info.pack(pady=5)

        lista_eliminar = tk.Listbox(self.tab_eliminar)
        lista_eliminar.pack(padx=10, pady=10, fill="both", expand=True)

        productos = Producto.obtener_todos()
        for p in productos:
            lista_eliminar.insert(tk.END, f"{p[0]} - {p[1]} (${p[2]}) | Stock: {p[3]}")

        def confirmar_eliminacion():
            seleccion = lista_eliminar.curselection()
            if seleccion:
                texto = lista_eliminar.get(seleccion[0])
                id_prod = int(texto.split(" - ")[0])
                producto_datos = [p for p in productos if p[0] == id_prod][0]
                prod_obj = Producto(*producto_datos)

                confirm = messagebox.askyesno("⚠️ Confirmar", f"¿Eliminar el producto '{prod_obj.nombre}'?")
                if confirm:
                    prod_obj.eliminar()
                    messagebox.showinfo("✔", "Producto eliminado.")
                    self.mostrar_lista_para_eliminar()
            else:
                messagebox.showwarning("❗", "Seleccioná un producto primero.")

        btn_confirmar = tk.Button(self.tab_eliminar, text="Eliminar seleccionado", command=confirmar_eliminacion)
        btn_confirmar.pack(pady=10)

    # ---------------- VENTAS ----------------
    def formulario_ventas(self):
        lbl_cliente = tk.Label(self.tab_ventas, text="Cliente:")
        lbl_cliente.pack(pady=3)
        self.entry_cliente = tk.Entry(self.tab_ventas)
        self.entry_cliente.pack(pady=3)

        lbl_prod = tk.Label(self.tab_ventas, text="Producto:")
        lbl_prod.pack(pady=3)

        self.combo_venta_producto = ttk.Combobox(self.tab_ventas, state="readonly")
        self.combo_venta_producto.pack(pady=3)
        self.productos_dict = {}
        self.cargar_productos_combo()

        lbl_stock = tk.Label(self.tab_ventas, text="Stock disponible:")
        lbl_stock.pack(pady=3)
        self.label_stock_valor = tk.Label(self.tab_ventas, text="-")
        self.label_stock_valor.pack(pady=3)

        lbl_cant = tk.Label(self.tab_ventas, text="Cantidad:")
        lbl_cant.pack(pady=3)
        self.entry_venta_cant = tk.Entry(self.tab_ventas)
        self.entry_venta_cant.pack(pady=3)
        self.entry_venta_cant.bind("<KeyRelease>", self.calcular_total_venta)

        lbl_total = tk.Label(self.tab_ventas, text="Total:")
        lbl_total.pack(pady=3)
        self.entry_venta_total = tk.Entry(self.tab_ventas)
        self.entry_venta_total.pack(pady=3)

        self.combo_venta_producto.bind("<<ComboboxSelected>>", self.calcular_total_venta)

        # Carrito visual
        btn_agregar = tk.Button(self.tab_ventas, text="Agregar al pedido", command=self.agregar_al_pedido)
        btn_agregar.pack(pady=3)

        self.lista_carrito = tk.Listbox(self.tab_ventas, height=5)
        self.lista_carrito.pack(pady=5, fill="both", expand=True)

        btn_guardar = tk.Button(self.tab_ventas, text="Registrar pedido", command=self.guardar_venta_multiple)
        btn_guardar.pack(pady=3)

        # Botón para eliminar venta
        btn_eliminar_venta = tk.Button(self.tab_ventas, text="🗑️ Eliminar venta", command=self.eliminar_venta)
        btn_eliminar_venta.pack(pady=5)

        # Botón para actualizar venta
        btn_actualizar_venta = tk.Button(self.tab_ventas, text="🔄 Actualizar venta", command=self.actualizar_venta)
        btn_actualizar_venta.pack(pady=5)

        btn_resumen = tk.Button(self.tab_ventas, text="Ver resumen de ventas", command=self.mostrar_resumen_ventas)
        btn_resumen.pack(pady=3)

        self.texto_resumen = tk.Text(self.tab_ventas, height=6)
        self.texto_resumen.pack(pady=10, fill="both", expand=True)

        self.lista_ventas = tk.Listbox(self.tab_ventas)
        self.lista_ventas.pack(pady=10, fill="both", expand=True)
        self.lista_ventas.bind("<<ListboxSelect>>", self.seleccionar_venta)

        self.carrito_ventas = []
        self.recargar_lista_ventas()

    def cargar_productos_combo(self):
        productos = Producto.obtener_todos()
        nombres = []
        for p in productos:
            nombre = p[1]  # ← nombre del producto
            self.productos_dict[nombre] = p[0]  # clave = nombre, valor = id
            nombres.append(nombre)
        self.combo_venta_producto["values"] = nombres
        if nombres:
            self.combo_venta_producto.current(0)

    def calcular_total_venta(self, event=None):
        try:
            nombre_prod = self.combo_venta_producto.get()
            id_prod = self.productos_dict.get(nombre_prod)
            producto = [p for p in Producto.obtener_todos() if p[0] == id_prod][0]
            precio = producto[2]
            stock = producto[3]
            cantidad = int(self.entry_venta_cant.get())
            total = precio * cantidad

            self.label_stock_valor.config(text=str(stock))
            self.entry_venta_total.delete(0, tk.END)
            self.entry_venta_total.insert(0, f"{total:.2f}")
        except:
            self.entry_venta_total.delete(0, tk.END)
            self.label_stock_valor.config(text="-")

    def agregar_al_pedido(self):
        try:
            nombre_prod = self.combo_venta_producto.get()
            id_prod = self.productos_dict.get(nombre_prod)
            cantidad = int(self.entry_venta_cant.get())
            producto = [p for p in Producto.obtener_todos() if p[0] == id_prod][0]

            if cantidad > producto[3]:
                messagebox.showwarning("🚫", f"No hay suficiente stock. Disponible: {producto[3]}")
                return

            total = float(self.entry_venta_total.get())
            self.carrito_ventas.append({
                "id_producto": id_prod,
                "nombre": nombre_prod,
                "cantidad": cantidad,
                "total": total
            })

            self.lista_carrito.insert(tk.END, f"{nombre_prod} x{cantidad} - ${total:.2f}")
            self.entry_venta_cant.delete(0, tk.END)
            self.entry_venta_total.delete(0, tk.END)
            self.label_stock_valor.config(text="-")
        except ValueError:
            messagebox.showerror("❌", "Datos inválidos.")

    def guardar_venta_multiple(self):
        cliente = self.entry_cliente.get()
        if not cliente:
            messagebox.showwarning("⚠️", "Ingresá el nombre del cliente.")
            return

        if not self.carrito_ventas:
            messagebox.showwarning("⚠️", "No hay productos en el pedido.")
            return

        for item in self.carrito_ventas:
            producto = [p for p in Producto.obtener_todos() if p[0] == item["id_producto"]][0]

            venta = Venta(
                id_producto=item["id_producto"],
                cantidad=item["cantidad"],
                total=item["total"],
                cliente=cliente
            )
            venta.guardar()
            Producto(*producto).descontar_stock(item["cantidad"])

        self.carrito_ventas.clear()
        self.lista_carrito.delete(0, tk.END)
        self.entry_cliente.delete(0, tk.END)
        self.recargar_lista_ventas()
        self.cargar_productos_combo()
        messagebox.showinfo("✔", "Pedido registrado con éxito.")

    def seleccionar_venta(self, event):
        seleccion = self.lista_ventas.curselection()
        if seleccion:
            texto = self.lista_ventas.get(seleccion[0])
            id_venta = int(texto.split(" - ")[0])
            datos = [v for v in Venta.obtener_todas() if v[0] == id_venta][0]

            self.entry_venta_cant.delete(0, tk.END)
            self.entry_venta_total.delete(0, tk.END)
            self.entry_cliente.delete(0, tk.END)

            producto_id = datos[2]
            producto_nombre = None
            for nombre, pid in self.productos_dict.items():
                if pid == producto_id:
                    self.combo_venta_producto.set(nombre)
                    producto_nombre = nombre
                    break

            coincidentes = [p for p in Producto.obtener_todos() if p[0] == producto_id]
            if coincidentes:
                producto = coincidentes[0]
                self.label_stock_valor.config(text=str(producto[3]))  # Stock
            else:
                self.label_stock_valor.config(text="(No disponible)")
                if not producto_nombre:
                    self.combo_venta_producto.set("(Producto eliminado)")
                messagebox.showwarning("⚠️", f"El producto con ID {producto_id} no existe o fue eliminado.")

            self.entry_venta_cant.insert(0, datos[3])
            self.entry_venta_total.insert(0, datos[4])
            self.entry_cliente.insert(0, datos[5])
            self.venta_seleccionada = Venta(*datos)

    def recargar_lista_ventas(self):
        self.lista_ventas.delete(0, tk.END)
        productos = Producto.obtener_todos()
        for v in Venta.obtener_todas():
            producto_coincidente = [p for p in productos if p[0] == v[2]]
            if producto_coincidente:
                nombre_prod = producto_coincidente[0][1]
            else:
                nombre_prod = "(Producto no disponible)"
            self.lista_ventas.insert(tk.END, f"{v[0]} - {v[1]} | Cliente: {v[5]} | {nombre_prod} x{v[3]} | Total: ${v[4]:.2f}")

    def resumen_ventas_por_producto(self):
        resumen = {}
        productos = Producto.obtener_todos()

        for v in Venta.obtener_todas():
            producto_id = v[2]
            cantidad = v[3]
            total = v[4]

            coincidente = [p for p in productos if p[0] == producto_id]
            if coincidente:
                nombre = coincidente[0][1]  # p[1] es el nombre del producto
            else:
                nombre = "(Producto no disponible)"

            if nombre not in resumen:
                resumen[nombre] = {"cantidad": 0, "total": 0.0}
            resumen[nombre]["cantidad"] += cantidad
            resumen[nombre]["total"] += total

        return resumen

    def mostrar_resumen_ventas(self):
        resumen = self.resumen_ventas_por_producto()
        self.texto_resumen.delete(1.0, tk.END)
        if not resumen:
            self.texto_resumen.insert(tk.END, "No hay datos de ventas.")
            return
        for nombre, datos in resumen.items():
            linea = f"{nombre}: {datos['cantidad']} unidades vendidas - Total: ${datos['total']:.2f}\n"
            self.texto_resumen.insert(tk.END, linea)
            
    def actualizar_venta(self):
        if hasattr(self, "venta_seleccionada"):
            try:
                nombre_prod = self.combo_venta_producto.get()
                id_prod = self.productos_dict.get(nombre_prod)
                producto = [p for p in Producto.obtener_todos() if p[0] == id_prod][0]
                nueva_cantidad = int(self.entry_venta_cant.get())
                nuevo_total = float(self.entry_venta_total.get())
                nuevo_cliente = self.entry_cliente.get()

                stock_actual = producto[3]
                cantidad_original = self.venta_seleccionada.cantidad
                diferencia = nueva_cantidad - cantidad_original

                if diferencia > stock_actual:
                    messagebox.showwarning("🚫", f"Stock insuficiente para actualizar. Disponible: {stock_actual}")
                    return

                Producto(*producto).descontar_stock(diferencia)

                self.venta_seleccionada.id_producto = id_prod
                self.venta_seleccionada.cantidad = nueva_cantidad
                self.venta_seleccionada.total = nuevo_total
                self.venta_seleccionada.cliente = nuevo_cliente
                self.venta_seleccionada.actualizar()

                self.recargar_lista_ventas()
                messagebox.showinfo("✔", "Venta actualizada.")
            except ValueError:
                messagebox.showerror("❌", "Datos inválidos.")    
        
    def eliminar_venta(self):
        seleccion = self.lista_ventas.curselection()
        if not seleccion:
            messagebox.showwarning("⚠️", "Seleccioná una venta para eliminar.")
            return

        texto = self.lista_ventas.get(seleccion[0])
        id_venta = int(texto.split(" - ")[0])
        datos_venta = [v for v in Venta.obtener_todas() if v[0] == id_venta]

        if not datos_venta:
            messagebox.showerror("❌", "No se encontró la venta seleccionada.")
            return

        venta = datos_venta[0]
        id_producto = venta[2]  # ← acá se define correctamente

        confirmar = messagebox.askyesno("¿Eliminar?", f"¿Querés eliminar la venta #{venta[0]}?")
        if confirmar:
            Venta.eliminar(venta[0])
            messagebox.showinfo("✔️", f"Venta #{venta[0]} eliminada correctamente.")
            self.recargar_lista_ventas()
            self.mostrar_resumen_ventas()  # si tenés resumen en pantalla

            # Opcional: actualizar el stock visual si el producto existe
            coincidentes = [p for p in Producto.obtener_todos() if p[0] == id_producto]
            if coincidentes:
                producto = coincidentes[0]
                self.label_stock_valor.config(text=str(producto[3]))
            else:
                self.label_stock_valor.config(text="(No disponible)")
        
        
    def formulario_resumen_categoria(self):
        label_titulo = tk.Label(self.tab_resumen, text="Resumen de Ventas por Categoría", font=("Arial", 16), bg="white")
        label_titulo.pack(pady=10)

        self.lista_resumen = tk.Listbox(self.tab_resumen, width=60, height=10)
        self.lista_resumen.pack(pady=10)

        btn_actualizar = tk.Button(self.tab_resumen, text="🔄 Actualizar resumen", command=self.mostrar_resumen_por_categoria)
        btn_actualizar.pack(pady=5)

        self.mostrar_resumen_por_categoria()  # Muestra el resumen al ingresar
    
    def mostrar_resumen_por_categoria(self):
        self.lista_resumen.delete(0, tk.END)
        resumen = Categoria.resumen_ventas_por_categoria()
        for categoria, cantidad, monto in resumen:
            linea = f"🍬 {categoria} — {cantidad} ventas — $ {monto:.2f}"
            self.lista_resumen.insert(tk.END, linea)
            
if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = GestorApp(root)
    root.mainloop()
            
            
    