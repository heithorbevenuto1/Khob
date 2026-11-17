# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import os  # Biblioteca nativa do Python (já vem instalada)
import sys  # Biblioteca nativa do Python (já vem instalada)

# ==============================================================================
# 2. CONFIGURAÇÃO DE CAMINHOS DO SISTEMA
# ==============================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

import customtkinter as ctk  # pip install customtkinter
from view import loading, inicio, karnaugh, configuracoes, conversor
from modelo import transicao

# Instância global da janela raiz do CustomTkinter
janela_raiz_aplicacao = None

# ==============================================================================
# 3. GERENCIADOR DO CICLO DE VIDA DA JANELA PRINCIPAL
# ==============================================================================
def abrir_loading() -> None:
    """
    Inicializa a janela raiz oculta do CustomTkinter e exibe o splash de carregamento.
    Ao concluir os 3 segundos do splash, transiciona automaticamente para o Início.
    """
    global janela_raiz_aplicacao
    ctk.set_appearance_mode("System")  # Adapta automaticamente ao tema Claro/Escuro do Windows
    ctk.set_default_color_theme("blue")

    janela_raiz_aplicacao = ctk.CTk()
    janela_raiz_aplicacao.withdraw()  # Mantém a janela raiz escondida durante o splash

    # Inicia o splash passando como callback a abertura do menu inicial
    loading.criar(janela_raiz_aplicacao, ao_terminar=abrir_inicio)
    janela_raiz_aplicacao.mainloop()


def abrir_inicio() -> None:
    """Abre a tela inicial principal da aplicação."""
    transicao.ir_para_inicio(janela_raiz_aplicacao)


def abrir_karnaugh() -> None:
    """Abre a tela do Mapa de Karnaugh."""
    transicao.ir_para_karnaugh(janela_raiz_aplicacao)


def abrir_configuracoes() -> None:
    """Abre a tela de Configurações."""
    transicao.ir_para_configuracoes(janela_raiz_aplicacao)


def abrir_conversor() -> None:
    """Abre a tela do Conversor de Bases."""
    transicao.ir_para_conversor(janela_raiz_aplicacao)

# ==============================================================================
# 4. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    abrir_loading()
