# execução do arquivo:
# python Khob/controle/main.py
# 




# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import sys  # Biblioteca nativa do Python (já vem instalada)
import os  # Biblioteca nativa do Python (já vem instalada)

# ==============================================================================
# 2. CONFIGURAÇÃO DE CAMINHOS DO SISTEMA
# ==============================================================================
# Garante que todos os módulos internos do Khob sejam resolvidos sem erros de importação
DIRETORIO_CONTROLE = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_CONTROLE, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_CONTROLE, DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

# ==============================================================================
# 3. IMPORTAÇÃO DOS MÓDULOS INTERNOS DO KHOB
# ==============================================================================
import c_karnaugh  # Módulo local de controle
from modelo import m_karnaugh  # Módulo local de cálculo do Karnaugh
from modelo import m_telas  # Módulo local de gerenciamento de telas
from modelo.m_telas import abrir_loading, abrir_inicio, abrir_karnaugh  # Funções de abertura

from view import inicio  # Módulo da tela inicial
from view import karnaugh  # Módulo da tela do Mapa de Karnaugh
from view import loading  # Módulo da tela de carregamento (splash)

# ==============================================================================
# 4. PONTO DE ENTRADA PRINCIPAL DA APLICAÇÃO
# ==============================================================================
if __name__ == "__main__":
    # Inicia o fluxo completo da aplicação pelo splash de carregamento
    abrir_loading()
