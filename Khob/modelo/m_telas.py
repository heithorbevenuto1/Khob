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
from view import inicio

#==========================================================================
#                               bibliotecas
#==========================================================================

import tkinter as tk
import time


#==========================================================================
#                                funções
#==========================================================================
#consertar: é para fechar a de loading apos 3s e abrir a de inicio
def abrir_loading():
    janela_load = loading.Loading()
    janela_inicio = inicio.Inicio()
    janela_inicio.withdraw()
    janela_load.deiconfig()
    time.sleep(3)
    janela_load.withdraw()
    janela_inicio.deiconify()
    
    
    


    
