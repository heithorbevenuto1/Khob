# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import os
import sys
import customtkinter as ctk

# ==============================================================================
# 2. CONFIGURAÇÃO DE CAMINHOS DO SISTEMA
# ==============================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_RAIZ_KHOB = os.path.abspath(os.path.join(DIRETORIO_ATUAL, ".."))
DIRETORIO_RAIZ_PROJETO = os.path.abspath(os.path.join(DIRETORIO_RAIZ_KHOB, ".."))

for caminho_pasta in (DIRETORIO_RAIZ_KHOB, DIRETORIO_RAIZ_PROJETO):
    if caminho_pasta not in sys.path:
        sys.path.insert(0, caminho_pasta)

# Importações dos módulos de negócio (Back-end) e navegação
from modelo import transicao
from modelo import m_karnaugh
from modelo import m_tabela_verdade

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
TAMANHOS_MAPA = {
    "Auto": None,
    "1x2": 2,
    "2x2": 4,
    "2x4": 8,
    "4x4": 16,
    "4x8": 32,
    "8x8": 64,
    "8x16": 128
}

COR_FUNDO_CARTAO = ("#FFFFFA", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_DESTAQUE_PRINCIPAL = ("#F33D65", "#F03D64")
COR_TEXTO_PRINCIPAL = ("#1A1A1E", "#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#5A5A60", "#A0A0A6")
COR_MENSAGEM_ERRO = ("#D32F2F", "#FF6B6B")

COR_BOTAO = ("#F03D64", "#F03D64")
COR_BOTAO_HOVER = ("#CF274B", "#CF274B")

# Cores para os Painéis Lado a Lado
COR_FUNDO_PAINEL = ("#F7F8FA", "#1D1D20")
COR_BORDA_PAINEL = ("#E2E4E8", "#323236")

# Cores do Mapa de Karnaugh
COR_FUNDO_CELULA = ("#E8F1FC", "#1E2A38")
COR_BORDA_CELULA = ("#CF274B", "#CF274B")
COR_TEXTO_CELULA = ("#1A1A1E", "#F5F5F7")
COR_CELULA_UM_FUNDO = ("#FDECEF", "#341B23")
COR_FUNDO_CABECALHO_MAPA = ("#EAECEF", "#2A2A2E")
COR_BORDA_CABECALHO_MAPA = ("#D0D5DD", "#3E3E44")
COR_TEXTO_CABECALHO_MAPA = ("#C82348", "#FF5277")

# Cores da Tabela Verdade
COR_FUNDO_CABECALHO_TABELA = ("#E2E5E9", "#2A2A2E")
COR_LINHA_PAR = ("#FFFFFF", "#232326")
COR_LINHA_IMPAR = ("#F4F5F7", "#1E1E21")
COR_TEXTO_SAIDA_1 = ("#E02653", "#FF4D79")
COR_TEXTO_SAIDA_0 = ("#1A1A1E", "#DCDCE0")
COR_TEXTO_SAIDA_X = ("#8E8E93", "#8E8E93")


# ==============================================================================
# 4. CONSTRUÇÃO DA INTERFACE GRÁFICA (MAPA DE KARNAUGH & TABELA VERDADE)
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """
    Constrói a interface com a Tabela Verdade à esquerda e o Mapa de Karnaugh à direita,
    com suporte completo a rótulos de variáveis (A/B, AB/CD...) e Gray code (00, 01...).
    
    Parâmetros:
        janela_raiz (ctk.CTk): Janela principal da aplicação.
    """
    janela_raiz.title("Khob - Mapa de Karnaugh & Tabela Verdade")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 100, 1080)
    altura_janela = min(altura_monitor - 100, 780)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(820, 580)

    # Estado da seleção de tamanho
    tamanho_selecionado = "Auto"

    # --------------------------------------------------------------------------
    # 4.1 Container Rolável Principal
    # --------------------------------------------------------------------------
    container_rolavel = ctk.CTkScrollableFrame(
        janela_raiz,
        corner_radius=12,
        fg_color=COR_FUNDO_CARTAO,
        scrollbar_button_color=COR_BOTAO,
        scrollbar_button_hover_color=COR_BOTAO_HOVER,
        border_width=1,
        border_color=COR_BORDA_CARTAO
    )
    container_rolavel.pack(fill="both", expand=True, padx=20, pady=(20, 10))

    # --------------------------------------------------------------------------
    # 4.2 Barra Superior (Voltar ao Início)
    # --------------------------------------------------------------------------
    barra_topo = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    barra_topo.pack(fill="x", padx=10, pady=(10, 0))

    botao_voltar = ctk.CTkButton(
        barra_topo,
        text="← Voltar ao Início",
        width=130,
        height=32,
        corner_radius=8,
        fg_color="transparent",
        border_width=2,
        border_color=COR_BORDA_CARTAO,
        text_color=COR_TEXTO_SECUNDARIO,
        hover_color=COR_BOTAO_HOVER,
        command=lambda: transicao.ir_para_inicio(janela_raiz)
    )
    botao_voltar.pack(side="left")

    # --------------------------------------------------------------------------
    # 4.3 Cabeçalho e Instruções
    # --------------------------------------------------------------------------
    rotulo_titulo = ctk.CTkLabel(
        container_rolavel,
        text="Mapa de Karnaugh & Tabela Verdade",
        font=ctk.CTkFont(size=25, weight="bold"),
        text_color=COR_BOTAO,
    )
    rotulo_titulo.pack(pady=(8, 4))

    rotulo_instrucao = ctk.CTkLabel(
        container_rolavel,
        text="Digite a sequência lógica de saída desejada (apenas 0, 1 e X):",
        font=ctk.CTkFont(size=14),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_instrucao.pack(pady=(0, 8))

    # Campo de Entrada de Dados
    campo_entrada = ctk.CTkEntry(
        container_rolavel,
        font=ctk.CTkFont(family="Consolas", size=16),
        justify="center",
        width=350,
        height=40,
        corner_radius=8,
        placeholder_text="Ex: 01X1 ou 01011010"
    )
    campo_entrada.pack(pady=4)
    campo_entrada.focus()

    # --------------------------------------------------------------------------
    # 4.4 Seletor de Tamanho
    # --------------------------------------------------------------------------
    rotulo_seletor = ctk.CTkLabel(
        container_rolavel,
        text="Tamanho do mapa:",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=COR_TEXTO_SECUNDARIO,
    )
    rotulo_seletor.pack(pady=(8, 2))

    def atualizar_tamanho_escolhido(novo_valor: str) -> None:
        nonlocal tamanho_selecionado
        tamanho_selecionado = novo_valor

    seletor_tamanhos = ctk.CTkSegmentedButton(
        container_rolavel,
        values=list(TAMANHOS_MAPA.keys()),
        command=atualizar_tamanho_escolhido,
        font=ctk.CTkFont(size=12, weight="bold"),
        height=32,
        selected_color=COR_BOTAO,
        selected_hover_color=COR_BOTAO_HOVER,
    )
    seletor_tamanhos.set("Auto")
    seletor_tamanhos.pack(pady=4)

    # --------------------------------------------------------------------------
    # 4.5 Botões de Ação
    # --------------------------------------------------------------------------
    linha_acoes = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    linha_acoes.pack(pady=10)

    botao_gerar = ctk.CTkButton(
        linha_acoes,
        text="Gerar Mapa",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=130,
        height=36,
        corner_radius=8,
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: acao_gerar()
    )
    botao_gerar.pack(side="left", padx=8)

    botao_limpar = ctk.CTkButton(
        linha_acoes,
        text="Limpar",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=100,
        height=36,
        corner_radius=8,
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: acao_limpar_tudo()
    )
    botao_limpar.pack(side="left", padx=8)

    # Rótulo de Erros / Alertas
    rotulo_erro = ctk.CTkLabel(
        container_rolavel,
        text="",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=COR_MENSAGEM_ERRO
    )
    rotulo_erro.pack(pady=2)

    # --------------------------------------------------------------------------
    # 4.6 Área Central Dividida: Esquerda (Tabela Verdade) / Direita (Karnaugh)
    # --------------------------------------------------------------------------
    quadro_paineis = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    quadro_paineis.pack(fill="both", expand=True, padx=10, pady=10)

    # Configuração de grid responsivo: Coluna 0 (Tabela) e Coluna 1 (Karnaugh)
    quadro_paineis.grid_columnconfigure(0, weight=2)
    quadro_paineis.grid_columnconfigure(1, weight=3)
    quadro_paineis.grid_rowconfigure(0, weight=1)

    # --------------------------------------------------------------------------
    # Painel Esquerdo: Tabela Verdade
    # --------------------------------------------------------------------------
    cartao_esquerdo = ctk.CTkFrame(
        quadro_paineis,
        corner_radius=12,
        fg_color=COR_FUNDO_PAINEL,
        border_width=1,
        border_color=COR_BORDA_PAINEL
    )
    cartao_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=5)

    rotulo_titulo_tabela = ctk.CTkLabel(
        cartao_esquerdo,
        text="Tabela Verdade",
        font=ctk.CTkFont(size=17, weight="bold"),
        text_color=COR_BOTAO
    )
    rotulo_titulo_tabela.pack(pady=(12, 2))

    rotulo_info_tabela = ctk.CTkLabel(
        cartao_esquerdo,
        text="Entradas binárias e respectiva saída (S)",
        font=ctk.CTkFont(size=12),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_info_tabela.pack(pady=(0, 8))

    frame_scroll_tabela = ctk.CTkScrollableFrame(
        cartao_esquerdo,
        height=380,
        fg_color="transparent",
        scrollbar_button_color=COR_BOTAO,
        scrollbar_button_hover_color=COR_BOTAO_HOVER
    )
    frame_scroll_tabela.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Placeholder inicial da Tabela Verdade
    rotulo_placeholder_tabela = ctk.CTkLabel(
        frame_scroll_tabela,
        text="Aguardando sequência lógica...\nDigite os valores e clique em 'Gerar Mapa'.",
        font=ctk.CTkFont(size=13),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_placeholder_tabela.pack(pady=40)

    # --------------------------------------------------------------------------
    # Painel Direito: Mapa de Karnaugh
    # --------------------------------------------------------------------------
    cartao_direito = ctk.CTkFrame(
        quadro_paineis,
        corner_radius=12,
        fg_color=COR_FUNDO_PAINEL,
        border_width=1,
        border_color=COR_BORDA_PAINEL
    )
    cartao_direito.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=5)

    rotulo_titulo_karnaugh = ctk.CTkLabel(
        cartao_direito,
        text="Mapa de Karnaugh",
        font=ctk.CTkFont(size=17, weight="bold"),
        text_color=COR_BOTAO
    )
    rotulo_titulo_karnaugh.pack(pady=(12, 2))

    rotulo_info_karnaugh = ctk.CTkLabel(
        cartao_direito,
        text="Agrupamentos e minimização booleana",
        font=ctk.CTkFont(size=12),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_info_karnaugh.pack(pady=(0, 8))

    frame_scroll_karnaugh = ctk.CTkScrollableFrame(
        cartao_direito,
        height=380,
        fg_color="transparent",
        scrollbar_button_color=COR_BOTAO,
        scrollbar_button_hover_color=COR_BOTAO_HOVER
    )
    frame_scroll_karnaugh.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Container interno onde o grid com rótulos e células será desenhado
    quadro_grade_karnaugh = ctk.CTkFrame(frame_scroll_karnaugh, fg_color="transparent")
    quadro_grade_karnaugh.pack(pady=15, padx=10)

    rotulo_placeholder_karnaugh = ctk.CTkLabel(
        quadro_grade_karnaugh,
        text="O Mapa de Karnaugh com rótulos\n(ex: AB \\ CD e 00, 01...) aparecerá aqui.",
        font=ctk.CTkFont(size=13),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_placeholder_karnaugh.pack(pady=40)

    # --------------------------------------------------------------------------
    # 4.7 Botão Inferior (Configurações)
    # --------------------------------------------------------------------------
    botao_configuracao = ctk.CTkButton(
        janela_raiz,
        text="Configurações",
        font=ctk.CTkFont(size=13),
        height=34,
        corner_radius=8,
        fg_color="transparent",
        border_width=2,
        hover_color=COR_BOTAO_HOVER,
        border_color=COR_BORDA_CARTAO,
        text_color=COR_TEXTO_SECUNDARIO,
        command=lambda: transicao.ir_para_configuracoes(janela_raiz)
    )
    botao_configuracao.pack(side="bottom", pady=8)

    # --------------------------------------------------------------------------
    # 4.8 Funções de Lógica e Renderização da Tela
    # --------------------------------------------------------------------------
    def acao_limpar_tabela() -> None:
        """Remove todos os componentes desenhados na tabela verdade."""
        for filho in frame_scroll_tabela.winfo_children():
            filho.destroy()

    def acao_limpar_karnaugh() -> None:
        """Remove todos os componentes desenhados no mapa de Karnaugh."""
        for filho in quadro_grade_karnaugh.winfo_children():
            filho.destroy()

    def acao_limpar_tudo() -> None:
        """Limpa entrada, erros e restaura placeholders em ambos os lados."""
        campo_entrada.delete(0, "end")
        rotulo_erro.configure(text="")
        rotulo_info_tabela.configure(text="Entradas binárias e respectiva saída (S)")
        rotulo_info_karnaugh.configure(text="Agrupamentos e minimização booleana")

        acao_limpar_tabela()
        rotulo_novo_placeholder_tab = ctk.CTkLabel(
            frame_scroll_tabela,
            text="Aguardando sequência lógica...\nDigite os valores e clique em 'Gerar Mapa'.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SECUNDARIO
        )
        rotulo_novo_placeholder_tab.pack(pady=40)

        acao_limpar_karnaugh()
        rotulo_novo_placeholder_kar = ctk.CTkLabel(
            quadro_grade_karnaugh,
            text="O Mapa de Karnaugh com rótulos\n(ex: AB \\ CD e 00, 01...) aparecerá aqui.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SECUNDARIO
        )
        rotulo_novo_placeholder_kar.pack(pady=40)

        campo_entrada.focus()

    def acao_desenhar_tabela(dados_tabela: dict) -> None:
        """
        Renderiza visualmente a Tabela Verdade completa com mintermos, bits e saída.
        """
        acao_limpar_tabela()

        container_grade_tabela = ctk.CTkFrame(frame_scroll_tabela, fg_color="transparent")
        container_grade_tabela.pack(pady=5, padx=5)

        cabecalho = dados_tabela["cabecalho"]
        linhas = dados_tabela["linhas"]

        # Cabeçalho da Tabela
        for col_idx, nome_coluna in enumerate(cabecalho):
            is_saida = (nome_coluna == "S")
            cor_texto_cabecalho = COR_BOTAO if is_saida else COR_TEXTO_PRINCIPAL

            celula_cabecalho = ctk.CTkFrame(
                container_grade_tabela,
                fg_color=COR_FUNDO_CABECALHO_TABELA,
                corner_radius=6,
                height=30
            )
            celula_cabecalho.grid(row=0, column=col_idx, padx=2, pady=3, sticky="nsew")

            rotulo_col = ctk.CTkLabel(
                celula_cabecalho,
                text=nome_coluna,
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=cor_texto_cabecalho
            )
            rotulo_col.pack(padx=8, pady=4)

        # Linhas da Tabela
        for row_idx, info_linha in enumerate(linhas):
            cor_fundo_linha = COR_LINHA_PAR if row_idx % 2 == 0 else COR_LINHA_IMPAR

            # Coluna 0: Índice / Mintermo
            celula_indice = ctk.CTkFrame(
                container_grade_tabela,
                fg_color=cor_fundo_linha,
                corner_radius=4,
                height=26
            )
            celula_indice.grid(row=row_idx + 1, column=0, padx=2, pady=1, sticky="nsew")
            ctk.CTkLabel(
                celula_indice,
                text=str(info_linha["indice"]),
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=COR_TEXTO_SECUNDARIO
            ).pack(padx=6, pady=2)

            # Colunas de Variáveis (Bits)
            for bit_idx, bit_val in enumerate(info_linha["bits"]):
                celula_bit = ctk.CTkFrame(
                    container_grade_tabela,
                    fg_color=cor_fundo_linha,
                    corner_radius=4,
                    height=26
                )
                celula_bit.grid(row=row_idx + 1, column=bit_idx + 1, padx=2, pady=1, sticky="nsew")
                ctk.CTkLabel(
                    celula_bit,
                    text=bit_val,
                    font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
                    text_color=COR_TEXTO_PRINCIPAL
                ).pack(padx=8, pady=2)

            # Coluna Final: Saída S
            valor_saida = info_linha["saida"]
            if valor_saida == "1":
                cor_saida = COR_TEXTO_SAIDA_1
            elif valor_saida == "0":
                cor_saida = COR_TEXTO_SAIDA_0
            else:
                cor_saida = COR_TEXTO_SAIDA_X

            celula_saida = ctk.CTkFrame(
                container_grade_tabela,
                fg_color=cor_fundo_linha,
                corner_radius=4,
                height=26
            )
            celula_saida.grid(
                row=row_idx + 1,
                column=len(info_linha["bits"]) + 1,
                padx=2,
                pady=1,
                sticky="nsew"
            )
            ctk.CTkLabel(
                celula_saida,
                text=valor_saida,
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=cor_saida
            ).pack(padx=10, pady=2)

    def acao_desenhar_karnaugh(dados_karnaugh: dict) -> None:
        """
        Renderiza o Mapa de Karnaugh com:
        - Célula de canto com as variáveis (ex: AB \\ CD)
        - Cabeçalho de colunas com Gray code (ex: 00, 01, 11, 10)
        - Cabeçalho de linhas com Gray code (ex: 00, 01, 11, 10)
        - Células internas contendo os valores calculados
        """
        acao_limpar_karnaugh()

        matriz = dados_karnaugh["matriz"]
        rotulos_colunas = dados_karnaugh["rotulos_colunas"]
        rotulos_linhas = dados_karnaugh["rotulos_linhas"]
        rotulo_canto = dados_karnaugh["rotulo_canto"]

        total_linhas = len(matriz)
        total_colunas = len(matriz[0]) if total_linhas > 0 else 0

        # Ajuste dinâmico das dimensões das células para manter proporção agradável
        if total_colunas <= 2 and total_linhas <= 2:
            largura_celula, altura_celula, tamanho_fonte = 64, 64, 22
            largura_canto = 80
        elif total_colunas <= 4 and total_linhas <= 4:
            largura_celula, altura_celula, tamanho_fonte = 54, 54, 20
            largura_canto = 84
        elif total_colunas <= 8 and total_linhas <= 4:
            largura_celula, altura_celula, tamanho_fonte = 48, 48, 17
            largura_canto = 92
        elif total_colunas <= 8 and total_linhas <= 8:
            largura_celula, altura_celula, tamanho_fonte = 42, 42, 15
            largura_canto = 100
        else:
            # Mapas 8x16 (128 casas)
            largura_celula, altura_celula, tamanho_fonte = 36, 36, 13
            largura_canto = 110

        # ----------------------------------------------------------------------
        # 1. Célula de Canto: Rótulo das Variáveis (ex: A \ B, AB \ CD, etc.)
        # ----------------------------------------------------------------------
        cartao_canto = ctk.CTkFrame(
            quadro_grade_karnaugh,
            width=largura_canto,
            height=36,
            corner_radius=6,
            fg_color=COR_FUNDO_CABECALHO_MAPA,
            border_width=1,
            border_color=COR_BORDA_CABECALHO_MAPA
        )
        cartao_canto.grid(row=0, column=0, padx=4, pady=4)
        cartao_canto.grid_propagate(False)

        rotulo_var_canto = ctk.CTkLabel(
            cartao_canto,
            text=rotulo_canto,
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=COR_TEXTO_CABECALHO_MAPA
        )
        rotulo_var_canto.place(relx=0.5, rely=0.5, anchor="center")

        # ----------------------------------------------------------------------
        # 2. Cabeçalho das Colunas: Gray Code (00, 01, 11, 10...)
        # ----------------------------------------------------------------------
        for col_idx, rotulo_coluna in enumerate(rotulos_colunas):
            cartao_col = ctk.CTkFrame(
                quadro_grade_karnaugh,
                width=largura_celula,
                height=36,
                corner_radius=6,
                fg_color=COR_FUNDO_CABECALHO_MAPA,
                border_width=1,
                border_color=COR_BORDA_CABECALHO_MAPA
            )
            cartao_col.grid(row=0, column=col_idx + 1, padx=3, pady=4)
            cartao_col.grid_propagate(False)

            rotulo_txt_col = ctk.CTkLabel(
                cartao_col,
                text=rotulo_coluna,
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=COR_TEXTO_CABECALHO_MAPA
            )
            rotulo_txt_col.place(relx=0.5, rely=0.5, anchor="center")

        # ----------------------------------------------------------------------
        # 3. Cabeçalho das Linhas (Gray Code) e Células do Mapa
        # ----------------------------------------------------------------------
        for row_idx, linha in enumerate(matriz):
            rotulo_linha = rotulos_linhas[row_idx] if row_idx < len(rotulos_linhas) else ""

            # Cabeçalho da Linha (Esquerda da grade)
            cartao_lin = ctk.CTkFrame(
                quadro_grade_karnaugh,
                width=largura_canto,
                height=altura_celula,
                corner_radius=6,
                fg_color=COR_FUNDO_CABECALHO_MAPA,
                border_width=1,
                border_color=COR_BORDA_CABECALHO_MAPA
            )
            cartao_lin.grid(row=row_idx + 1, column=0, padx=4, pady=3)
            cartao_lin.grid_propagate(False)

            rotulo_txt_lin = ctk.CTkLabel(
                cartao_lin,
                text=rotulo_linha,
                font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
                text_color=COR_TEXTO_CABECALHO_MAPA
            )
            rotulo_txt_lin.place(relx=0.5, rely=0.5, anchor="center")

            # Células de Dados da Linha
            for col_idx, valor_celula in enumerate(linha):
                # Destaca sutilmente células com '1'
                cor_bg = COR_CELULA_UM_FUNDO if valor_celula == "1" else COR_FUNDO_CELULA
                cor_txt = COR_TEXTO_SAIDA_1 if valor_celula == "1" else COR_TEXTO_CELULA

                cartao_celula = ctk.CTkFrame(
                    quadro_grade_karnaugh,
                    width=largura_celula,
                    height=altura_celula,
                    corner_radius=8,
                    fg_color=cor_bg,
                    border_width=2,
                    border_color=COR_BORDA_CELULA
                )
                cartao_celula.grid(row=row_idx + 1, column=col_idx + 1, padx=3, pady=3)
                cartao_celula.grid_propagate(False)

                rotulo_valor = ctk.CTkLabel(
                    cartao_celula,
                    text=valor_celula,
                    font=ctk.CTkFont(family="Consolas", size=tamanho_fonte, weight="bold"),
                    text_color=cor_txt
                )
                rotulo_valor.place(relx=0.5, rely=0.5, anchor="center")

    def acao_gerar() -> None:
        """
        Orquestra a chamada aos modelos de Karnaugh e Tabela Verdade
        e atualiza ambas as exibições gráficas lado a lado.
        """
        sequencia_digitada = campo_entrada.get()
        limite_tamanho = TAMANHOS_MAPA.get(tamanho_selecionado)

        # Validação centralizada através do modelo
        sucesso, mensagem_erro, sequencia_limpa = m_karnaugh.validar_entrada_karnaugh(
            sequencia_digitada,
            limite_tamanho
        )

        if not sucesso:
            rotulo_erro.configure(text=mensagem_erro)
            return

        rotulo_erro.configure(text="")

        # 1. Processa os dados do Mapa de Karnaugh pelo modelo
        dados_karnaugh = m_karnaugh.gerar_dados_karnaugh(sequencia_limpa, limite_tamanho)

        # 2. Processa os dados da Tabela Verdade pelo modelo
        dados_tabela = m_tabela_verdade.gerar_tabela_verdade(
            dados_karnaugh["saida_completa"],
            quantidade_variaveis=dados_karnaugh["num_variaveis"]
        )

        # Atualiza subtítulos com informações úteis
        qtd_vars = dados_karnaugh["num_variaveis"]
        vars_nomes = ", ".join(dados_tabela["variaveis"])
        rotulo_info_tabela.configure(
            text=f"{dados_tabela['total_linhas']} combinações ({qtd_vars} variáveis: {vars_nomes})"
        )
        rotulo_info_karnaugh.configure(
            text=f"Dimensão: {dados_karnaugh['dimensao']} ({dados_karnaugh['alvo']} células) | Eixos: {dados_karnaugh['rotulo_canto']}"
        )

        # Renderiza ambos os lados
        acao_desenhar_tabela(dados_tabela)
        acao_desenhar_karnaugh(dados_karnaugh)

    # Atalho: Enter no teclado aciona a geração
    janela_raiz.bind("<Return>", lambda evento: acao_gerar())

    janela_raiz.deiconify()


# ==============================================================================
# 5. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()
