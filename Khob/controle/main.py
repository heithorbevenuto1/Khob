import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import c_karnaugh
from modelo import m_karnaugh
from modelo import m_telas
#importando as funções do arquivo m_telas
from modelo.m_telas import abrir_loading, abrir_inicio

from view import inicio
from view import loading

abrir_loading()
