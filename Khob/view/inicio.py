# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import os  # Biblioteca nativa do Python (já vem instalada)
import sys  # Biblioteca nativa do Python (já vem instalada)
import customtkinter as ctk  # pip install customtkinter
from PIL import Image  # pip install Pillow

# ==============================================================================
# 2. CONFIGURAÇÃO DE CAMINHOS DO SISTEMA
# ==============================================================================
# Garante que as pastas do projeto sejam localizadas independentemente do diretório atual
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

# Importa o módulo responsável pela troca e transição limpa entre telas
from modelo import transicao

# Caminho absoluto da imagem do logotipo da aplicação
CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_KHOB, "img-e-visuais", "KhobLogo.png"))
if not os.path.exists(CAMINHO_LOGO):
    CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_PROJETO, "KhobLogo.png"))

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
# Tuplas com duas cores no formato: ("Cor Modo Claro", "Cor Modo Escuro")
COR_FUNDO_CARTAO = ("#F1F1F1", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_BOTAO_DESTAQUE = ("#F03D64", "#F03D64")
COR_LOGO =("#1D010E")
COR_TEXTO_PRINCIPAL = ( "#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#5A5A60", "#A0A0A6")
COR_BOTAO_NEUTRO = ("#E03E61", "#E03E61")
COR_BOTAO_NEUTRO_HOVER = ("#A71A39", "#A71A39")

# ==============================================================================
# 4. CONSTRUÇÃO DA INTERFACE GRÁFICA (TELA DE INÍCIO)
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """
    Constrói e exibe a Tela de Início (Menu Principal do Khob) dentro da janela raiz.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela principal onde a interface será desenhada.
    """
    # --------------------------------------------------------------------------
    # 4.1 Configuração básica da Janela
    # --------------------------------------------------------------------------
    janela_raiz.title("Khob - Painel Inicial")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 200, 850)
    altura_janela = min(altura_monitor - 150, 650)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(650, 500)

    # --------------------------------------------------------------------------
    # 4.2 Cartão Central (Container com Cantos Arredondados)
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
    # 4.3 Logotipo e Cabeçalho
    # --------------------------------------------------------------------------
    if os.path.exists(CAMINHO_LOGO):
        try:
            imagem_redimensionada = Image.open(CAMINHO_LOGO).convert("RGBA").resize((90, 90))
            imagem_custom = ctk.CTkImage(
                light_image=imagem_redimensionada,
                dark_image=imagem_redimensionada,
                size=(120, 120)
            )
            rotulo_logo = ctk.CTkLabel(cartao_principal, image=imagem_custom, text="")
            rotulo_logo.pack(pady=(25, 5))
        except Exception as erro_carregamento:
            print(f"[Aviso] Não foi possível renderizar a logo: {erro_carregamento}")
    '''
    rotulo_titulo = ctk.CTkLabel(
        cartao_principal,
        text="Khob",
        font=ctk.CTkFont(size=30, weight="bold"),
        text_color=COR_LOGO
    )
    rotulo_titulo.pack(pady=(5, 2))
    '''

    rotulo_subtitulo = ctk.CTkLabel(
        cartao_principal,
        text="Selecione uma das ferramentas abaixo para iniciar:",
        font=ctk.CTkFont(size=14),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_subtitulo.pack(pady=(0, 25))

    # --------------------------------------------------------------------------
    # 4.4 Botões de Navegação do Menu
    # --------------------------------------------------------------------------
    quadro_menu = ctk.CTkFrame(cartao_principal, fg_color="transparent")
    quadro_menu.pack(pady=10)

    # Botão de Acesso ao Mapa de Karnaugh
    botao_karnaugh = ctk.CTkButton(
        quadro_menu,
        text="Mapa de Karnaugh",
        font=ctk.CTkFont(size=15, weight="bold"),
        width=260,
        height=45,
        corner_radius=10,
        fg_color=COR_BOTAO_NEUTRO,
        hover_color=COR_BOTAO_NEUTRO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_karnaugh(janela_raiz)
    )
    botao_karnaugh.pack(pady=10)

    # Botão de Acesso ao Conversor de Bases
    botao_conversor = ctk.CTkButton(
        quadro_menu,
        text="Conversor de Bases",
        font=ctk.CTkFont(size=15, weight="bold"),
        width=260,
        height=45,
        corner_radius=10,
        fg_color=COR_BOTAO_NEUTRO,
        hover_color=COR_BOTAO_NEUTRO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_conversor(janela_raiz)
    )
    botao_conversor.pack(pady=10)



    #botão para o tutorial

    botao_tutorial = ctk.CTkButton(
        quadro_menu,
        text="Modulo de treinamento",
        font=ctk.CTkFont(size=15, weight="bold"),
        width=260,
        height=45,
        corner_radius=10,
        fg_color=COR_BOTAO_NEUTRO,
        hover_color=COR_BOTAO_NEUTRO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_tutorial(janela_raiz)
    )
    botao_tutorial.pack(pady=10)


    # Botão de Acesso às Configurações
    botao_configuracoes = ctk.CTkButton(
        quadro_menu,
        text="Configurações",
        font=ctk.CTkFont(size=15, weight="bold"),
        width=260,
        height=42,
        corner_radius=10,
        fg_color=COR_BOTAO_NEUTRO,
        hover_color=COR_BOTAO_NEUTRO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_configuracoes(janela_raiz)
    )
    botao_configuracoes.pack(pady=10)

    # --------------------------------------------------------------------------
    # 4.5 Exibição da Janela
    # --------------------------------------------------------------------------
    janela_raiz.deiconify()


# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()
