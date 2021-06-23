# Interfaz gráfica
from tkinter import *


# Creación de la interfaz
raiz = Tk()
raiz.title("BuscaTRÓN")

busqueda = StringVar()
numBusquedas = IntVar()

miFrame = Frame(raiz, width=350, height=200)
miFrame.pack()

cuadroBusqueda = Entry(miFrame, textvariable=busqueda)
cuadroBusqueda.grid(row=0, column=1, padx=5, pady=5)

cuadroNumBusquedas = Entry(miFrame, textvariable=numBusquedas)
cuadroNumBusquedas.grid(row=1, column=1, padx=5, pady=5)

busquedaLabel = Label(miFrame, text="Introduce lo que quieres buscar: ")
busquedaLabel.grid(row=0, column=0, sticky="e", padx=5, pady=5)

numBusquedasLabel = Label(miFrame, text="Introduce el número de búsquedas: ")
numBusquedasLabel.grid(row=1, column=0, sticky="e", padx=5, pady=5)



# Al final del todo, para mantener la ventana de búsqueda abierta
raiz.mainloop()