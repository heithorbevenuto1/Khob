import io
import os
import tkinter as tk
from contextlib import redirect_stdout
from view.estilo import aplicar_css, classe

# Raiz do projeto (a pasta acima de view/) e os nomes aceitos para o back end.
RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOMES_BACKEND = ("m_karnaugh.py", "m-karnaugh.py")

# Tamanhos que o usuário pode escolher e quantas casas cada um tem.
# "Auto" deixa o back end decidir pelo tamanho do que foi digitado.
TAMANHOS = {"Auto": None, "2x2": 4, "2x4": 8, "4x4": 16}


def achar_backend():
    """Procura o back end em qualquer subpasta do projeto, então não importa
    em qual pasta ele está."""
    for pasta, _, arquivos in os.walk(RAIZ_PROJETO):
        for nome in NOMES_BACKEND:
            if nome in arquivos:
                return os.path.join(pasta, nome)
    raise FileNotFoundError(f"não achei {NOMES_BACKEND[0]} dentro de {RAIZ_PROJETO}")


def carregar_backend():
    """Carrega a função karnaugh() do m_karnaugh.py SEM alterar o arquivo.

    O back end chama karnaugh_loop() no final do arquivo, que fica esperando
    o usuário digitar no terminal. Para isso não travar a janela, trocamos o
    input() por uma versão falsa que interrompe o loop assim que ele começa.
    A função karnaugh() já está definida nesse ponto, então ela fica disponível."""

    def input_falso(*args):
        raise EOFError  # corta o karnaugh_loop() antes de ele esperar digitação

    espaco = {"__name__": "m_karnaugh", "input": input_falso}

    caminho = achar_backend()
    with open(caminho, "r", encoding="utf-8") as f:
        codigo = f.read()

    with redirect_stdout(io.StringIO()):  # esconde o banner que o loop imprime
        try:
            exec(compile(codigo, caminho, "exec"), espaco)
        except EOFError:
            pass  # esperado: foi o input_falso interrompendo o loop

    return espaco["karnaugh"]


def pegar_mapa(karnaugh, texto):
    """Chama o back end e transforma o que ele imprime numa lista de linhas.
    Ex.: "01X1" -> [["0", "1"], ["X", "1"]]"""
    saida = io.StringIO()
    with redirect_stdout(saida):  # captura o print() do back end
        karnaugh(texto)

    # cada linha impressa é do tipo "0 | 1"; ignoramos o título e as linhas vazias
    linhas = [l for l in saida.getvalue().splitlines()
              if l.strip() and "Mapa de Karnaugh" not in l]
    mapa = [l.split(" | ") for l in linhas]

    # o back end imprime 1 variável com um valor por linha; juntamos numa linha só
    if len(texto) <= 2:
        mapa = [[l[0] for l in mapa]]
    return mapa


def criar(raiz):
    """Monta a tela inicial (com o Karnaugh) dentro da janela raiz."""
    raiz.title("Programa Principal")

    ltela = raiz.winfo_screenwidth()
    atela = raiz.winfo_screenheight()
    largura = ltela - 300
    altura = atela - 300
    px = (ltela - largura) // 2
    py = (atela - altura) // 2
    raiz.geometry(f"{largura}x{altura}+{px}+{py}")

    escolhido = "Auto"   # tamanho selecionado no momento

    # ---------- widgets fixos (não mudam quando gera outro mapa) ----------
    # botão da calculadora: fica fixo no rodapé (side="bottom")
    tk.Button(raiz, text="Ir para a calculadora",
              command=lambda: abrir_calculadora()).pack(side="bottom", pady=20)

    classe(tk.Label(raiz, text="Mapa de Karnaugh"), "titulo").pack(pady=20)
    tk.Label(raiz, text="Digite a saída (apenas 0, 1 e X):").pack()

    entrada = tk.Entry(raiz, font=("Consolas", 14), justify="center", width=24)
    entrada.pack(pady=10)
    entrada.focus()

    # linha de botões para escolher o tamanho do mapa
    linha_tamanhos = tk.Frame(raiz)
    linha_tamanhos.pack(pady=5)
    botoes_tamanho = {}
    for nome in TAMANHOS:
        # "ativa" = botão selecionado, "opcao" = os outros (cores no tema.css)
        classe_inicial = "ativa" if nome == escolhido else "opcao"
        b = classe(tk.Button(linha_tamanhos, text=nome,
                             command=lambda n=nome: escolher(n)), classe_inicial)
        b.pack(side="left", padx=5)
        botoes_tamanho[nome] = b

    # linha com os botões de ação
    linha_acoes = tk.Frame(raiz)
    linha_acoes.pack(pady=10)
    tk.Button(linha_acoes, text="Gerar mapa", command=lambda: gerar()).pack(side="left", padx=10)
    tk.Button(linha_acoes, text="Limpar", command=lambda: limpar()).pack(side="left", padx=10)

    # mensagem de erro (fica vazia quando está tudo certo)
    erro = tk.Label(raiz, text="", fg="#c0392b")
    erro.pack()

    # frame onde o mapa é desenhado (é limpo a cada novo mapa)
    quadro = tk.Frame(raiz)
    quadro.pack(pady=20)

    # ---------- carrega o back end ----------
    try:
        karnaugh = carregar_backend()
    except (OSError, KeyError) as e:
        karnaugh = None
        erro.config(text=f"Não consegui carregar o m_karnaugh.py: {e}")

    # ---------- lógica da tela ----------
    def escolher(nome):
        """Marca o tamanho escolhido e destaca o botão dele."""
        nonlocal escolhido
        escolhido = nome
        for n, b in botoes_tamanho.items():
            b.css_class = "ativa" if n == nome else "opcao"
        aplicar_css(raiz)   # reaplica o tema para atualizar as cores

    def apagar_mapa():
        for w in quadro.winfo_children():
            w.destroy()

    def limpar():
        """Limpa a entrada, a mensagem de erro e o mapa, pronto para outro."""
        entrada.delete(0, tk.END)
        erro.config(text="")
        apagar_mapa()
        entrada.focus()

    def gerar():
        if karnaugh is None:
            return

        texto = entrada.get().upper().replace(" ", "")

        # validações simples antes de chamar o back end
        if not texto:
            erro.config(text="Entrada vazia.")
            return
        if not all(c in "01X" for c in texto):
            erro.config(text="Use apenas 0, 1 e X.")
            return
        if len(texto) > 32:
            erro.config(text="Entrada grande demais (máx. 32).")
            return

        # se um tamanho foi escolhido, completa com X até ele (o back end
        # escolhe o mapa pelo tamanho do texto, então isso força o tamanho certo)
        alvo = TAMANHOS[escolhido]
        if alvo is not None:
            if len(texto) > alvo:
                erro.config(text=f"{escolhido} comporta só {alvo} casas, mas você digitou {len(texto)}.")
                return
            texto = texto.ljust(alvo, "X")

        erro.config(text="")
        desenhar(pegar_mapa(karnaugh, texto))

    def desenhar(mapa):
        apagar_mapa()   # apaga o mapa anterior

        # cria uma célula (Label com borda) para cada valor do mapa
        for i, linha in enumerate(mapa):
            for j, valor in enumerate(linha):
                celula = tk.Label(quadro, text=valor, width=4, height=2,
                                  relief="solid", bd=1)
                celula.grid(row=i, column=j)

        aplicar_css(raiz)  # reaplica o tema nos widgets novos

    def abrir_calculadora():
        """Abre a calculadora. Quando você criar o view/calculadora.py com uma
        função criar(raiz), este botão passa a funcionar sozinho."""
        try:
            from view import calculadora
        except ImportError:
            erro.config(text="AURA MAIS EGO!!!!!!!!.")
            return
        calculadora.criar(raiz)

    # Enter também gera o mapa
    raiz.bind("<Return>", lambda e: gerar())

    raiz.deiconify()   # mostra a raiz (ela começa escondida durante o loading)
    aplicar_css(raiz)

    # F5 recarrega o CSS sem fechar o programa
    raiz.bind("<F5>", lambda e: aplicar_css(raiz))
