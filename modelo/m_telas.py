#==========================================================================
#                               descrição
#==========================================================================
'''
aqui sera configurado as funções de abertura das telas do programa, como a tela de loading, tela de inicio, tela de cadastro e etc.
'''
#==========================================================================
#                               importar arquivos
#==========================================================================
from view import loading

#==========================================================================
#                               bibliotecas
#==========================================================================

import tkinter as tk


#==========================================================================
#                                funções
#==========================================================================

def abrir_loading():
    janela_load = loading.Loading()
    janela_load.janewithdraw()

abrir_loading()
if __name__ == "__main__":
    janela_principal = abrir_loading()
    janela_principal.mainloop()