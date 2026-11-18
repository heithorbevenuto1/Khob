# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import io  # Biblioteca nativa do Python (já vem instalada)
import os  # Biblioteca nativa do Python (já vem instalada)
import sys  # Biblioteca nativa do Python (já vem instalada)
from contextlib import redirect_stdout  # Biblioteca nativa do Python (já vem instalada)
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

NOMES_ARQUIVOS_BACKEND = ("m_karnaugh.py", "m-karnaugh.py")

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES DE TAMANHO
# ==============================================================================
# Quantidade de casas aceitas por cada dimensão do mapa de Karnaugh

TAMANHOS_MAPA = {
    "Auto": None,
    "2x2": 4,
    "2x4": 8,
    "4x4": 16,
    "4x8": 32,
    "8x8": 64,
    "8x16": 128
}

# Cores nos modos Claro e Escuro: ("Modo Claro", "Modo Escuro")
COR_FUNDO_CARTAO = ("#FFFFFA", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_DESTAQUE_PRINCIPAL = ("#F33D65", "#F03D64")
COR_TEXTO_PRINCIPAL = ("#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#2F2F33", "#A0A0A6")
COR_MENSAGEM_ERRO = ("#D32F2F", "#FF6B6B")
COR_FUNDO_CELULA = ("#E8F1FC", "#1E2A38")
COR_BORDA_CELULA = ("#CF274B")
COR_BOTAO = ("#F03D64")
COR_BOTAO_HOVER = ("#CF274B")

# ==============================================================================
# 4. INTEGRAÇÃO COM O BACK-END (MODELO DE KARNAUGH)
# ==============================================================================
def localizar_arquivo_backend() -> str:
    """
    Pesquisa recursivamente pelo arquivo de lógica m_karnaugh.py nas pastas do projeto.
    
    Retorno:
        str: Caminho absoluto para o arquivo do back-end.
    """
    for pasta_atual, _, lista_arquivos in os.walk(DIRETORIO_RAIZ_KHOB):
        for nome_procurado in NOMES_ARQUIVOS_BACKEND:
            if nome_procurado in lista_arquivos:
                return os.path.join(pasta_atual, nome_procurado)
    raise FileNotFoundError(f"Não foi possível encontrar {NOMES_ARQUIVOS_BACKEND[0]} em {DIRETORIO_RAIZ_KHOB}")


def carregar_funcao_backend():
    """
    Lê dinamicamente o arquivo m_karnaugh.py e extrai a função de cálculo karnaugh().
    Utiliza um input simulado para evitar que o loop infinito de terminal trave a interface.
    
    Retorno:
        function: A função de processamento de Karnaugh.
    """
    def entrada_falsa(*argumentos):
        raise EOFError  # Interrompe o loop de console de forma segura

    espaco_nomes = {"__name__": "m_karnaugh", "input": entrada_falsa}
    caminho_backend = localizar_arquivo_backend()

    with open(caminho_backend, "r", encoding="utf-8") as arquivo_codigo:
        codigo_fonte = arquivo_codigo.read()

    # Silencia impressões indesejadas durante a compilação do módulo
    with redirect_stdout(io.StringIO()):
        try:
            exec(compile(codigo_fonte, caminho_backend, "exec"), espaco_nomes)
        except EOFError:
            pass

    return espaco_nomes["karnaugh"]


def extrair_matriz_mapa(funcao_karnaugh, texto_saida: str):
    """
    Executa o back-end capturando sua saída em texto e a convertendo em uma matriz 2D.
    
    Parâmetros:
        funcao_karnaugh: Referência à função de cálculo do Karnaugh.
        texto_saida (str): String com a sequência lógica inserida pelo usuário (ex: '01X1').
        
    Retorno:
        list: Lista de linhas contendo os valores de cada célula do mapa.
    """
    fluxo_saida = io.StringIO()
    with redirect_stdout(fluxo_saida):
        funcao_karnaugh(texto_saida)

    linhas_filtradas = [
        linha for linha in fluxo_saida.getvalue().splitlines()
        if linha.strip() and "Mapa de Karnaugh" not in linha
    ]
    matriz_mapa = [linha.split(" | ") for linha in linhas_filtradas]

    # Para mapas de 1 ou 2 variáveis, organiza como linha única
    if len(texto_saida) <= 2:
        matriz_mapa = [[linha[0] for linha in matriz_mapa]]
        
    return matriz_mapa

# ==============================================================================
# 5. CONSTRUÇÃO DA INTERFACE GRÁFICA (MAPA DE KARNAUGH)
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """
    Monta a interface completa da ferramenta do Mapa de Karnaugh dentro da janela raiz.
    
    Parâmetros:
        janela_raiz (ctk.CTk): A janela principal onde a tela será renderizada.
    """
    # --------------------------------------------------------------------------
    # 5.1 Configuração básica e responsividade
    # --------------------------------------------------------------------------
    janela_raiz.title("Khob - Mapa de Karnaugh")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 200, 950)
    altura_janela = min(altura_monitor - 150, 750)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(680, 560)

    # Estado interno da seleção de tamanho
    tamanho_selecionado = "Auto"

    # --------------------------------------------------------------------------
    # 5.2 Container Rolável Principal
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
    container_rolavel.pack(fill="both", expand=True, padx=20, pady=20)

    # --------------------------------------------------------------------------
    # 5.3 Barra Superior (Navegação de Retorno)
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
    # 5.4 Cabeçalho e Instruções
    # --------------------------------------------------------------------------
    rotulo_titulo = ctk.CTkLabel(
        container_rolavel,
        text="Mapa de Karnaugh",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color=COR_TEXTO_PRINCIPAL
    )
    rotulo_titulo.pack(pady=(10, 5))

    rotulo_instrucao = ctk.CTkLabel(
        container_rolavel,
        text="Digite a saída lógica desejada (apenas 0, 1 e X):",
        font=ctk.CTkFont(size=14),
        text_color=COR_TEXTO_SECUNDARIO
    )
    rotulo_instrucao.pack(pady=(0, 10))

    # Campo de Entrada de Dados
    campo_entrada = ctk.CTkEntry(
        container_rolavel,
        font=ctk.CTkFont(family="Consolas", size=16),
        justify="center",
        width=320,
        height=40,
        corner_radius=8,
        placeholder_text="Ex: 01X1 ou 01011010"
    )
    campo_entrada.pack(pady=5)
    campo_entrada.focus()

    # --------------------------------------------------------------------------
    # 5.5 Seletor de Tamanho do Mapa
    # --------------------------------------------------------------------------
    rotulo_seletor = ctk.CTkLabel(
        container_rolavel,
        text="Tamanho do mapa:",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=COR_TEXTO_SECUNDARIO,
    )
    rotulo_seletor.pack(pady=(12, 4))

    def atualizar_tamanho_escolhido(novo_valor: str) -> None:
        nonlocal tamanho_selecionado
        tamanho_selecionado = novo_valor

    seletor_tamanhos = ctk.CTkSegmentedButton(
        container_rolavel,
        values=list(TAMANHOS_MAPA.keys()),
        command=atualizar_tamanho_escolhido,
        font=ctk.CTkFont(size=13, weight="bold"),
        height=34,


        #OLHAR AQUI
        
        selected_color=COR_BOTAO,
        selected_hover_color=COR_BOTAO_HOVER,
        
    )
    seletor_tamanhos.set("Auto")
    seletor_tamanhos.pack(pady=5)

    # --------------------------------------------------------------------------
    # 5.6 Botões de Ação (Gerar e Limpar)
    # --------------------------------------------------------------------------
    linha_acoes = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    linha_acoes.pack(pady=15)

    botao_gerar = ctk.CTkButton(
        linha_acoes,
        text="Gerar Mapa",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=130,
        height=38,
        corner_radius=8,
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: acao_gerar_mapa()
    )
    botao_gerar.pack(side="left", padx=8)

    botao_limpar = ctk.CTkButton(
        linha_acoes,
        text="Limpar",
        font=ctk.CTkFont(size=14, weight="bold"),
        width=100,
        height=38,
        corner_radius=8,
        fg_color=COR_BOTAO,
        hover_color=COR_BOTAO_HOVER,
        text_color=COR_TEXTO_PRINCIPAL,
        command=lambda: acao_limpar_tudo()
    )
    botao_limpar.pack(side="left", padx=8)

    # Mensagens de Erro e Validação
    rotulo_erro = ctk.CTkLabel(
        container_rolavel,
        text="",
        font=ctk.CTkFont(size=13, weight="bold"),
        text_color=COR_MENSAGEM_ERRO
    )
    rotulo_erro.pack(pady=2)

    # Área onde as células do mapa serão renderizadas
    quadro_celulas_mapa = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    quadro_celulas_mapa.pack(pady=15)

    # --------------------------------------------------------------------------
    # 5.7 Botão de Rodapé para Calculadora
    # --------------------------------------------------------------------------
    botao_configuracao = ctk.CTkButton(
        janela_raiz,
        text="configurações",
        font=ctk.CTkFont(size=13),
        height=34,
        corner_radius=8,
        fg_color="transparent",
        border_width=2,
        hover_color=COR_BOTAO_HOVER,
        border_color=COR_BORDA_CARTAO,
        text_color=COR_TEXTO_SECUNDARIO,
        command=lambda:transicao.ir_para_configuracoes(janela_raiz)
    )
    botao_configuracao.pack(side="bottom", pady=10)

    # --------------------------------------------------------------------------
    # 5.8 Inicialização do Back-End
    # --------------------------------------------------------------------------
    try:
        funcao_karnaugh_backend = carregar_funcao_backend()
    except (OSError, KeyError) as erro_carregamento:
        funcao_karnaugh_backend = None
        rotulo_erro.configure(text=f"Erro ao carregar o back-end: {erro_carregamento}")

    # --------------------------------------------------------------------------
    # 5.9 Funções de Lógica da Tela
    # --------------------------------------------------------------------------
    def acao_apagar_celulas() -> None:
        """Limpa visualmente todas as células do mapa anterior."""
        for filho in quadro_celulas_mapa.winfo_children():
            filho.destroy()

    def acao_limpar_tudo() -> None:
        """Limpa o campo de texto, a mensagem de erro e o mapa atual."""
        campo_entrada.delete(0, "end")
        rotulo_erro.configure(text="")
        acao_apagar_celulas()
        campo_entrada.focus()

    def acao_gerar_mapa() -> None:
        """Valida a entrada do usuário e gera o mapa de Karnaugh."""
        if funcao_karnaugh_backend is None:
            rotulo_erro.configure(text="O módulo de cálculo não está disponível.")
            return

        sequencia_digitada = campo_entrada.get().upper().replace(" ", "")

        # Validações de entrada
        if not sequencia_digitada:
            rotulo_erro.configure(text="Entrada vazia. Digite ao menos um valor.")
            return
        if not all(caractere in "01X" for caractere in sequencia_digitada):
            rotulo_erro.configure(text="Use apenas os caracteres válidos: 0, 1 e X.")
            return
        if len(sequencia_digitada) > 32:
            rotulo_erro.configure(text="Entrada muito longa (limite máximo de 32 bits).")
            return

        limite_tamanho = TAMANHOS_MAPA[tamanho_selecionado]
        if limite_tamanho is not None:
            if len(sequencia_digitada) > limite_tamanho:
                rotulo_erro.configure(
                    text=f"O tamanho {tamanho_selecionado} suporta {limite_tamanho} casas, mas foram digitadas {len(sequencia_digitada)}."
                )
                return
            sequencia_digitada = sequencia_digitada.ljust(limite_tamanho, "X")

        rotulo_erro.configure(text="")
        matriz_resultado = extrair_matriz_mapa(funcao_karnaugh_backend, sequencia_digitada)
        acao_desenhar_celulas(matriz_resultado)

    def acao_desenhar_celulas(matriz_mapa: list) -> None:
        """Renderiza cada célula da matriz como um cartão elegante."""
        acao_apagar_celulas()

        for indice_linha, linha in enumerate(matriz_mapa):
            for indice_coluna, valor_celula in enumerate(linha):
                cartao_celula = ctk.CTkFrame(
                    quadro_celulas_mapa,
                    width=54,
                    height=54,
                    corner_radius=8,
                    fg_color=COR_FUNDO_CELULA,
                    border_width=2,
                    border_color=COR_BORDA_CELULA,
                )
                cartao_celula.grid(row=indice_linha, column=indice_coluna, padx=4, pady=4)
                cartao_celula.grid_propagate(False)

                rotulo_valor = ctk.CTkLabel(
                    cartao_celula,
                    text=valor_celula,
                    font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
                    text_color=COR_TEXTO_PRINCIPAL
                )
                rotulo_valor.place(relx=0.5, rely=0.5, anchor="center")

    def acao_abrir_calculadora() -> None:
        """Abre a calculadora quando implementada."""
        try:
            from view import calculadora
            calculadora.criar(janela_raiz)
        except ImportError:
            rotulo_erro.configure(text="A tela da calculadora ainda não foi implementada.")

    # Atalho de teclado: Tecla Enter gera o mapa
    janela_raiz.bind("<Return>", lambda evento: acao_gerar_mapa())

    janela_raiz.deiconify()


# ==============================================================================
# 6. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()
