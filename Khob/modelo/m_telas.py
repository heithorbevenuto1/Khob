import tkinter as tk
from view import loading, inicio

_raiz = None


def abrir_loading():
    global _raiz
    _raiz = tk.Tk()
    _raiz.withdraw()                                   # esconde a raiz durante o loading
    loading.criar(_raiz, ao_terminar=abrir_inicio)
    _raiz.mainloop()


def abrir_inicio():
    inicio.criar(_raiz)
