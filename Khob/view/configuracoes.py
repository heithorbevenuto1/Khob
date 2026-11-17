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

# Importa o módulo responsável pela troca e transição limpa entre telas
from modelo import transicao

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
COR_FUNDO_CARTAO = ("#FFFFFF", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_TEXTO_PRINCIPAL = ("#1A1A1E", "#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#5A5A60", "#A0A0A6")
COR_FUNDO_PAINEL_SOBRE = ("gray92", "gray18")

# ==============================================================================
# 4. CONSTRUÇÃO DA INTERFACE GRÁFICA (TELA DE CONFIGURAÇÕES)
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """
    Constrói e exibe a Tela de Configurações dentro da janela raiz.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela principal onde a interface será desenhada.
    """
    # --------------------------------------------------------------------------
    # 4.1 Configuração básica e responsividade
    # --------------------------------------------------------------------------
    janela_raiz.title("Khob - Configurações")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 200, 850)
    altura_janela = min(altura_monitor - 150, 650)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(650, 500)

    # --------------------------------------------------------------------------
    # 4.2 Cartão Central Principal
    # --------------------------------------------------------------------------
    cartao_principal = ctk.CTkFrame(
        janela_raiz,
        corner_radius=12,
        fg_color=COR_FUNDO_CARTAO,
        border_width=1,
        border_color=COR_BORDA_CARTAO
    )
    cartao_principal.pack(fill="both", expand=True, padx=30, pady=30)

    # --------------------------------------------------------------------------
    # 4.3 Barra Superior (Retorno ao Início)
    # --------------------------------------------------------------------------
    barra_topo = ctk.CTkFrame(cartao_principal, fg_color="transparent")
    barra_topo.pack(fill="x", padx=20, pady=(20, 10))

    botao_voltar = ctk.CTkButton(
        barra_topo,
        text="← Voltar ao Início",
        width=130,
        height=32,
        corner_radius=8,
        fg_color="transparent",
        border_width=1,
        border_color=COR_BORDA_CARTAO,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_inicio(janela_raiz)
    )
    botao_voltar.pack(side="left")

    # --------------------------------------------------------------------------
    # 4.4 Títulos e Cabeçalho
    # --------------------------------------------------------------------------
    rotulo_titulo = ctk.CTkLabel(
        cartao_principal,
        text="Configurações",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_titulo.pack(pady=(10, 5))

    rotulo_subtitulo = ctk.CTkLabel(
        cartao_principal,
        text="Personalize a aparência e preferências do aplicativo:",
        font=ctk.CTkFont(size=14),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_subtitulo.pack(pady=(0, 25))

    # --------------------------------------------------------------------------
    # 4.5 Seção: Modo de Aparência / Tema
    # --------------------------------------------------------------------------
    quadro_tema = ctk.CTkFrame(cartao_principal, fg_color="transparent")
    quadro_tema.pack(pady=15)

    rotulo_tema = ctk.CTkLabel(
        quadro_tema,
        text="Tema do aplicativo:",
        font=ctk.CTkFont(size=15, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_tema.pack(side="left", padx=15)

    def acao_alterar_tema(opcao_selecionada: str) -> None:
        """Altera a paleta da aplicação em tempo real."""
        mapa_modos = {
            "Sistema": "System",
            "Claro": "Light",
            "Escuro": "Dark"
        }
        ctk.set_appearance_mode(mapa_modos.get(opcao_selecionada, "System"))

    menu_selecao_tema = ctk.CTkOptionMenu(
        quadro_tema,
        values=["Sistema", "Claro", "Escuro"],
        command=acao_alterar_tema,
        width=150,
        height=36,
        corner_radius=8
    )
    menu_selecao_tema.set("Sistema")
    menu_selecao_tema.pack(side="left", padx=10)

    # --------------------------------------------------------------------------
    # 4.6 Seção Informativa (Sobre o Sistema)
    # --------------------------------------------------------------------------
    painel_sobre = ctk.CTkFrame(cartao_principal, corner_radius=10, fg_color=COR_FUNDO_PAINEL_SOBRE)
    painel_sobre.pack(fill="x", padx=40, pady=30)

    rotulo_informacoes = ctk.CTkLabel(
        painel_sobre,
        text="Khob - Versão 1.0\nDesenvolvido com CustomTkinter para Python",
        font=ctk.CTkFont(size=13),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_informacoes.pack(pady=15)

    janela_raiz.deiconify()


# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()
