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
from modelo import m_conversor

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
COR_FUNDO_CARTAO = ("#FFFFFF", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_TEXTO_PRINCIPAL = ("#1A1A1E", "#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#5A5A60", "#A0A0A6")
COR_MENSAGEM_ERRO = ("#F03D64", "#FF6B6B")
COR_PAINEL_RESULTADOS = ("gray92", "gray18")
COR_BOTAO_HOVER=("#CF274B")
COR_BOTAO = ("#F03D64")

# ==============================================================================
# 4. CONSTRUÇÃO DA INTERFACE GRÁFICA (TELA DO CONVERSOR)
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """
    Constrói e exibe a Tela de Conversão Numérica dentro da janela raiz.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela principal onde a interface será desenhada.
    """
    # --------------------------------------------------------------------------
    # 4.1 Configuração básica e responsividade
    # --------------------------------------------------------------------------
    janela_raiz.title("Khob - Conversor de Bases")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 200, 850)
    altura_janela = min(altura_monitor - 150, 650)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(650, 500)

    # --------------------------------------------------------------------------
    # 4.2 Cartão Central Rolável
    # --------------------------------------------------------------------------
    cartao_rolavel = ctk.CTkScrollableFrame(
        janela_raiz,
        corner_radius=12,
        fg_color=COR_FUNDO_CARTAO,
        scrollbar_button_color=COR_BOTAO,
        scrollbar_button_hover_color=COR_BOTAO_HOVER,
        border_width=1,
        border_color=COR_BORDA_CARTAO
    )
    cartao_rolavel.pack(fill="both", expand=True, padx=30, pady=30)

    # --------------------------------------------------------------------------
    # 4.3 Barra Superior (Retorno ao Início)
    # --------------------------------------------------------------------------
    barra_topo = ctk.CTkFrame(cartao_rolavel, fg_color="transparent")
    barra_topo.pack(fill="x", padx=10, pady=(10, 5))

    botao_voltar = ctk.CTkButton(
        barra_topo,
        text="← Voltar ao Início",
        width=130,
        height=32,
        corner_radius=8,
        fg_color="transparent",
        border_width=1,
        border_color=COR_BORDA_CARTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: transicao.ir_para_inicio(janela_raiz)
    )
    botao_voltar.pack(side="left")

    # --------------------------------------------------------------------------
    # 4.4 Cabeçalho e Título
    # --------------------------------------------------------------------------
    rotulo_titulo = ctk.CTkLabel(
        cartao_rolavel,
        text="Conversor de Bases",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_titulo.pack(pady=(10, 5))

    rotulo_subtitulo = ctk.CTkLabel(
        cartao_rolavel,
        text="Converta números entre Decimal, Binário e Hexadecimal:",
        font=ctk.CTkFont(size=14),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_subtitulo.pack(pady=(0, 20))

    # --------------------------------------------------------------------------
    # 4.5 Campo de Entrada e Seletor de Base
    # --------------------------------------------------------------------------
    campo_entrada = ctk.CTkEntry(
        cartao_rolavel,
        font=ctk.CTkFont(family="Consolas", size=15),
        justify="center",
        width=320,
        height=40,
        corner_radius=8,
        placeholder_text="Digite o valor a ser convertido..."
    )
    campo_entrada.pack(pady=10)

    seletor_base_origem = ctk.CTkSegmentedButton(
        cartao_rolavel,
        values=["Decimal", "Binário", "Octal", "Hexadecimal"],
        font=ctk.CTkFont(size=13, weight="bold"),
        selected_color=COR_BOTAO,
        selected_hover_color=COR_BOTAO_HOVER,
        height=34
    )
    seletor_base_origem.set("Decimal")
    seletor_base_origem.pack(pady=5)

    # --------------------------------------------------------------------------
    # 4.6 Painel de Resultados da Conversão
    # --------------------------------------------------------------------------
    painel_resultados = ctk.CTkFrame(cartao_rolavel, corner_radius=10, fg_color=COR_PAINEL_RESULTADOS)
    painel_resultados.pack(fill="x", padx=40, pady=20)

    rotulo_resultado_binario = ctk.CTkLabel(
        painel_resultados,
        text="Binário: -",
        font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_resultado_binario.pack(pady=6)


    rotulo_resultado_octal = ctk.CTkLabel(
        painel_resultados,
        text="Octal: -",
        font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_resultado_octal.pack(pady=6)


    rotulo_resultado_decimal = ctk.CTkLabel(
        painel_resultados,
        text="Decimal: -",
        font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_resultado_decimal.pack(pady=6)

    rotulo_resultado_hexadecimal = ctk.CTkLabel(
        painel_resultados,
        text="Hexadecimal: -",
        font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_resultado_hexadecimal.pack(pady=6)

    rotulo_erro = ctk.CTkLabel(
        cartao_rolavel,
        text="",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=COR_MENSAGEM_ERRO
    )
    rotulo_erro.pack(pady=2)

    # --------------------------------------------------------------------------
    # 4.7 Lógica de Conversão
    # --------------------------------------------------------------------------
    def acao_executar_conversao() -> None:
        """Lê o valor digitado, aciona o back-end (m_conversor) e atualiza os resultados."""
        valor_digitado = campo_entrada.get()
        base_selecionada = seletor_base_origem.get()
        rotulo_erro.configure(text="")

        try:
            resultados = m_conversor.converter_bases(valor_digitado, base_selecionada)
            rotulo_resultado_binario.configure(text=f"Binário: {resultados['binario']}")
            rotulo_resultado_decimal.configure(text=f"Decimal: {resultados['decimal']}")
            rotulo_resultado_octal.configure(text=f"Octal: {resultados['octal']}")
            rotulo_resultado_hexadecimal.configure(text=f"Hexadecimal: {resultados['hexadecimal']}")
        except ValueError as erro_conversao:
            rotulo_erro.configure(text=str(erro_conversao))

    botao_converter = ctk.CTkButton(
        cartao_rolavel,
        text="Converter",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=140,
        height=38,
        hover_color=COR_BOTAO_HOVER,
        fg_color=COR_BOTAO,
        corner_radius=8,
        command=acao_executar_conversao
    )
    botao_converter.pack(pady=10)

    # Permite pressionar Enter para acionar a conversão
    janela_raiz.bind("<Return>", lambda evento: acao_executar_conversao())

    janela_raiz.deiconify()


# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()
