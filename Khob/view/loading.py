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
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

# Localização dinâmica e segura do arquivo da logo
CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_KHOB, "img-e-visuais", "KhobLogo.png"))
if not os.path.exists(CAMINHO_LOGO):
    CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_PROJETO, "KhobLogo.png"))

# Carregamento prévio da imagem da logo com suporte à transparência
IMAGEM_ORIGINAL_LOGO = Image.open(CAMINHO_LOGO).convert("RGBA")

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
# Tuplas com duas cores no formato: ("Cor Modo Claro", "Cor Modo Escuro")
COR_FUNDO_SPLASH = ("#F5F5F7", "#1A1A1E")
COR_TEXTO_SPLASH = ("#1A1A1E", "#F5F5F7")
COR_BARRA_PROGRESSO = ("#F03D64", "#D96A8A")
DURACAO_SPLASH_MILISSEGUNDOS = 3000

# ==============================================================================
# 4. CONSTRUÇÃO DA TELA DE CARREGAMENTO (SPLASH SCREEN)
# ==============================================================================
def criar(janela_raiz: ctk.CTk, ao_terminar=None) -> None:
    """
    Exibe a tela de carregamento (splash) com logo e barra de progresso animada.
    Após a conclusão do tempo estipulado, destrói o splash e dispara a função ao_terminar().
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela raiz oculta da aplicação.
        ao_terminar (função, opcional): Callback chamado ao concluir o carregamento.
    """
    # Cria janela secundária sem barra de título padrão (Splash Screen)
    janela_splash = ctk.CTkToplevel(janela_raiz)
    janela_splash.title("Carregando Sistema...")

    # Dimensões e centralização na tela do usuário
    largura_monitor = janela_splash.winfo_screenwidth()
    altura_monitor = janela_splash.winfo_screenheight()
    largura_splash = largura_monitor - int((largura_monitor // 2) * 1.4)
    altura_splash = altura_monitor - int((altura_monitor // 2) * 1.4)
    posicao_horizontal = (largura_monitor - largura_splash) // 2
    posicao_vertical = (altura_monitor - altura_splash) // 2

    janela_splash.geometry(f"{largura_splash}x{altura_splash}+{posicao_horizontal}+{posicao_vertical}")
    janela_splash.overrideredirect(True)  # Remove as bordas do sistema operacional
    janela_splash.configure(fg_color=COR_FUNDO_SPLASH)

    # --------------------------------------------------------------------------
    # 4.1 Logotipo Central
    # --------------------------------------------------------------------------
    imagem_redimensionada = IMAGEM_ORIGINAL_LOGO.resize((200, 200))
    imagem_customizada = ctk.CTkImage(
        light_image=imagem_redimensionada,
        dark_image=imagem_redimensionada,
        size=(200, 200)
    )

    rotulo_imagem = ctk.CTkLabel(janela_splash, image=imagem_customizada, text="")
    rotulo_imagem.pack(pady=20)

    # --------------------------------------------------------------------------
    # 4.2 Texto Informativo
    # --------------------------------------------------------------------------
    rotulo_texto = ctk.CTkLabel(
        janela_splash,
        text="Carregando o sistema...",
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=COR_TEXTO_SPLASH
    )
    rotulo_texto.pack(pady=5)

    # --------------------------------------------------------------------------
    # 4.3 Barra de Progresso Animada
    # --------------------------------------------------------------------------
    barra_progresso = ctk.CTkProgressBar(janela_splash, width=280, progress_color=COR_BARRA_PROGRESSO)
    barra_progresso.pack(pady=15)
    barra_progresso.set(0.0)

    def animar_progresso(progresso_atual: float = 0.0) -> None:
        """Incrementa gradualmente a barra de progresso durante o tempo da animação."""
        if progresso_atual >= 1.0:
            return
        progresso_atual += 0.01
        barra_progresso.set(progresso_atual)
        janela_splash.after(30, lambda: animar_progresso(progresso_atual))

    animar_progresso()

    # --------------------------------------------------------------------------
    # 4.4 Finalização e Fechamento
    # --------------------------------------------------------------------------
    def finalizar_splash() -> None:
        janela_splash.destroy()
        if ao_terminar:
            ao_terminar()

    janela_splash.after(DURACAO_SPLASH_MILISSEGUNDOS, finalizar_splash)


# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    aplicativo_teste.withdraw()  # Oculta a raiz para visualizar apenas o splash
    criar(aplicativo_teste, ao_terminar=lambda: aplicativo_teste.destroy())
    aplicativo_teste.mainloop()
