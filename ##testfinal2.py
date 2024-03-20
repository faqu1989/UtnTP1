##testfinal2
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Función para crear tabla
def crear_tabla():
    con = conectar()
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS access_points (
                      id INTEGER PRIMARY KEY,
                      marca TEXT,
                      modelo TEXT,
                      cantidad INTEGER)''')
    con.commit()
    con.close()

# funcion para conectar a la base de datos
def conectar():   
    con = sqlite3.connect("inventario_access_points.db")
    return con

# funcion para agregar un access point al inventario
def agregar_access_point():
    marca = marca_entry.get()
    modelo = modelo_entry.get()
    cantidad = int(cantidad_entry.get())
    con = conectar()
    cursor = con.cursor()
    cursor.execute("INSERT INTO access_points (marca, modelo, cantidad) VALUES (?, ?, ?)", (marca, modelo, cantidad))
    con.commit()
    con.close()
    messagebox.showinfo("Éxito", "Access Point agregado al inventario.")
    mostrar_access_points()

# funcion para eliminar un access point del inventario
def eliminar_access_point():
    marca = marca_entry.get()
    modelo = modelo_entry.get()
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM access_points WHERE marca=? AND modelo=?", (marca, modelo))
    con.commit()
    con.close()
    messagebox.showinfo("Éxito", "Access Point eliminado del inventario.")
    mostrar_access_points()

# funcion para modificar un access point del inventario
def modificar_access_point():
    marca = marca_entry.get()
    modelo = modelo_entry.get()
    cantidad = int(cantidad_entry.get())
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE access_points SET cantidad=? WHERE marca=? AND modelo=?", (cantidad, marca, modelo))
    con.commit()
    con.close()
    messagebox.showinfo("Éxito", "Cantidad de Access Point modificada en el inventario.")
    mostrar_access_points()

# funcion para consultar un access point en el inventario
def consultar_access_point():
    marca = marca_entry.get()
    modelo = modelo_entry.get()
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM access_points WHERE marca=? AND modelo=?", (marca, modelo))
    access_point = cursor.fetchone()
    con.close()
    if access_point:
        messagebox.showinfo("Detalle del Access Point", 
            f"Marca: {access_point[1]}\nModelo: {access_point[2]}\nCantidad: {access_point[3]}")
    else:
        messagebox.showerror("Error", "El access point no se encontró en el inventario.")

# funcion para mostrar los access points en el Treeview
def mostrar_access_points():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM access_points")
    access_points = cursor.fetchall()
    con.close()
    limpiar_treeview()
    for access_point in access_points:
        treeview.insert("", "end", values=access_point)

# funcion para limpiar el contenido del Treeview
def limpiar_treeview():
    for i in treeview.get_children():
        treeview.delete(i)

# crear ventana principal
root = tk.Tk()
root.title("Sistema de Inventario de Access Points")

# crear etiquetas y campos de entrada
marca_label = tk.Label(root, text="Marca:")
marca_label.grid(row=0, column=0, padx=5, pady=5)
marca_entry = tk.Entry(root)
marca_entry.grid(row=0, column=1, padx=5, pady=5)

modelo_label = tk.Label(root, text="Modelo:")
modelo_label.grid(row=1, column=0, padx=5, pady=5)
modelo_entry = tk.Entry(root)
modelo_entry.grid(row=1, column=1, padx=5, pady=5)

cantidad_label = tk.Label(root, text="Cantidad:")
cantidad_label.grid(row=2, column=0, padx=5, pady=5)
cantidad_entry = tk.Entry(root)
cantidad_entry.grid(row=2, column=1, padx=5, pady=5)

# crear botones
crear_tabla()  # Llamamos a esta función para crear la tabla al inicio
agregar_button = tk.Button(root, text="Agregar", command=agregar_access_point)
agregar_button.grid(row=3, column=0, padx=5, pady=5)

eliminar_button = tk.Button(root, text="Eliminar", command=eliminar_access_point)
eliminar_button.grid(row=3, column=1, padx=5, pady=5)

modificar_button = tk.Button(root, text="Modificar", command=modificar_access_point)
modificar_button.grid(row=3, column=2, padx=5, pady=5)

consultar_button = tk.Button(root, text="Consultar", command=consultar_access_point)
consultar_button.grid(row=3, column=3, padx=5, pady=5)

# crear treeview para mostrar los access points
treeview = ttk.Treeview(root, columns=("ID", "Marca", "Modelo", "Cantidad"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Marca", text="Marca")
treeview.heading("Modelo", text="Modelo")
treeview.heading("Cantidad", text="Cantidad")
treeview.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

# Mostrar los access points al inicio
mostrar_access_points()

# Ejecutar el bucle de eventos
root.mainloop()