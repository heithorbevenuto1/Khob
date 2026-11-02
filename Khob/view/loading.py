#==========================================================================
#                               bibliotecas
#==========================================================================

import tkinter as tk
from tkinter import messagebox


#==========================================================================
#                     Tamanho e centralização da janela
#==========================================================================
#variavel para a janela
janela= tk.Tk()

#pega o tamanho da tela em pixeis
ltela = janela.winfo_screenwidth()
atela = janela.winfo_screenheight()
print(ltela,atela)

#tamanho da janela
largura = ltela-300
altura = atela-300
#posicionar no meio
px = (ltela - largura) // 2
py= (atela - altura) // 2

janela.geometry(f"{largura}x{altura}+{px}+{py}")

janela.config(bg= "#C9BAC1") #fundo da tela


janela.mainloop()

