import pandas as pd

import json

import tkinter as tk
from tkinter import ttk
# Lee el archivo JSON y carga los datos de las reglas de las enfermedades en una variable 
with open('reglas.json', 'r') as file:
    reglas = json.load(file)
    
# Lee el archivo Excel
df = pd.read_excel("sintomas.xlsx", engine='openpyxl')

num_filas = df.shape[0]

print("Número de filas:", num_filas)

# Convierte el DataFrame en un diccionario de Python
def evaluar_reglas(sintomas, reglas):
        diagnosticos = []
        explicaciones = []
        for regla in reglas:
            if all(sintomas.get(s, False) for s in regla["sintomas_presentes"]) and \
            not any(sintomas.get(s, False) for s in regla["sintomas_ausentes"]):
                diagnosticos.append(regla["diagnostico"])
                explicaciones.append(regla["explicacion"])
            
                 
        return diagnosticos, explicaciones


diagnosticos_totales = []
explicaciones_totales = []

for i in range(num_filas):
    sintomas_entrada = df.to_dict('records')[i]
    # Evaluación de síntomas y obtención de diagnósticos y explicaciones
    diagnosticos, explicaciones = evaluar_reglas(sintomas_entrada, reglas)
    
    # Verifica si se encontraron síntomas en alguna iteración
    if diagnosticos or explicaciones:
        diagnosticos_totales.extend(diagnosticos)
        explicaciones_totales.extend(explicaciones)
    else:
        # Si no se encontraron síntomas para ninguna regla, inserta un mensaje
        diagnosticos_totales.append("No se encontraron síntomas para ninguna enfermedad.")
        explicaciones_totales.append("No hay explicacion")
    

for diagnostico, explicacion in zip(diagnosticos_totales, explicaciones_totales):
    print(f"{diagnostico} Razón: {explicacion} \n")


def mostrar_resultados():
    # Crear ventana
    ventana_resultados = tk.Tk()
    ventana_resultados.title("Resultados de diagnóstico")

    # Crear Treeview para mostrar los resultados en una tabla
    tree = ttk.Treeview(ventana_resultados)
    tree["columns"] = ("Numeros","Diagnóstico", "Explicación")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Numeros", anchor=tk.W, width=75)  
    tree.column("Diagnóstico", anchor=tk.W, width=250)
    tree.column("Explicación", anchor=tk.W, width=400)
    tree.heading("Numeros", text="No Caso")
    tree.heading("Diagnóstico", text="Diagnóstico")
    tree.heading("Explicación", text="Explicación")

    # Insertar resultados en la tabla
    num = 1
    for diagnostico, explicacion in zip(diagnosticos_totales, explicaciones_totales):
        tree.insert("", tk.END, values=(num,diagnostico, explicacion))
        num = num + 1

    # Mostrar Treeview
    tree.pack(expand=True, fill=tk.BOTH)

    ventana_resultados.mainloop()

# Llamar a la función para mostrar los resultados
mostrar_resultados()