# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import os  # Biblioteca nativa do Python (já vem instalada)
import sys  # Biblioteca nativa do Python (já vem instalada)
import customtkinter as ctk  # pip install customtkinter

# ==============================================================================
# 2. CONFIGURAÇÃO DE CAMINHOS DO SISTEMA
# ==============================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

# ==============================================================================
# 3. FUNÇÕES CENTRAIS DE TRANSIÇÃO E LIMPEZA DE JANELA
# ==============================================================================
def limpar_tela(janela_raiz: ctk.CTk) -> None:
    """
    Remove todos os widgets existentes na janela para permitir que a nova tela
    seja desenhada de forma limpa e sem sobreposição de elementos ou vazamento de memória.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela que terá os componentes destruídos.
    """
    for widget in janela_raiz.winfo_children():
        widget.destroy()


def mudar_tela(janela_raiz: ctk.CTk, funcao_construtora_tela) -> None:
    """
    Realiza a transição suave destruindo os widgets anteriores e chamando a função
    construtora da próxima tela.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela principal onde a troca ocorrerá.
        funcao_construtora_tela (função): Função responsável por montar a nova interface.
    """
    limpar_tela(janela_raiz)
    funcao_construtora_tela(janela_raiz)

# ==============================================================================
# 4. ROTAS DE NAVEGAÇÃO ENTRE AS TELAS
# ==============================================================================
def ir_para_inicio(janela_raiz: ctk.CTk) -> None:
    """Transiciona a interface para a Tela de Início (Menu Principal)."""
    from view import inicio
    mudar_tela(janela_raiz, inicio.criar)


def ir_para_karnaugh(janela_raiz: ctk.CTk) -> None:
    """Transiciona a interface para a Tela do Mapa de Karnaugh."""
    from view import karnaugh
    mudar_tela(janela_raiz, karnaugh.criar)

def ir_para_tutorial(janela_raiz: ctk.CTk) -> None:
    """Transiciona a interface para a Tela de Configurações."""
    from view import tutorial
    mudar_tela(janela_raiz, tutorial.criar)


def ir_para_configuracoes(janela_raiz: ctk.CTk) -> None:
    """Transiciona a interface para a Tela de Configurações."""
    from view import configuracoes
    mudar_tela(janela_raiz, configuracoes.criar)


def ir_para_conversor(janela_raiz: ctk.CTk) -> None:
    """Transiciona a interface para a Tela do Conversor de Bases."""
    from view import conversor
    mudar_tela(janela_raiz, conversor.criar)

# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    ir_para_inicio(aplicativo_teste)
    aplicativo_teste.mainloop()
