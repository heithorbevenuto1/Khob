# ==============================================================================
# 1. IMPORTAÇÕES E BIBLIOTECAS
# ==============================================================================
import os  # Biblioteca nativa do Python
import re  # Expressões regulares para interpretar markdown/HTML
import sys  # Biblioteca nativa do Python
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

from modelo import transicao

CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_KHOB, "img-e-visuais", "KhobLogo.png"))
if not os.path.exists(CAMINHO_LOGO):
    CAMINHO_LOGO = os.path.normpath(os.path.join(DIRETORIO_RAIZ_PROJETO, "KhobLogo.png"))

CAMINHO_MDTUTORIAL = os.path.normpath(os.path.join(DIRETORIO_RAIZ_KHOB, "img-e-visuais", "tutorial.md"))
if not os.path.exists(CAMINHO_MDTUTORIAL):
    CAMINHO_MDTUTORIAL = os.path.normpath(os.path.join(DIRETORIO_RAIZ_PROJETO, "tutorial.md"))

# ==============================================================================
# 3. PALETA DE CORES E CONSTANTES VISUAIS
# ==============================================================================
COR_FUNDO_CARTAO = ("#FFFFFF", "#242426")
COR_BORDA_CARTAO = ("#E0E0E0", "#38383A")
COR_TEXTO_PRINCIPAL = ("#1A1A1E", "#F5F5F7")
COR_TEXTO_SECUNDARIO = ("#4A4A50", "#A8A8B0")
COR_DESTAQUE = ("#E82953", "#E82953")
COR_FUNDO_TABELA_CABECALHO = ("#EAEAEF", "#2E2E32")
COR_FUNDO_TABELA_CELULA = ("#FAFAFC", "#1E1E22")


# ==============================================================================
# 4. RENDERIZADOR DE MARKDOWN E HTML
# ==============================================================================
def carregar_markdown() -> str:
    """Lê o arquivo tutorial.md garantindo a decodificação em UTF-8."""
    if os.path.exists(CAMINHO_MDTUTORIAL):
        try:
            with open(CAMINHO_MDTUTORIAL, "r", encoding="utf-8") as arquivo:
                return arquivo.read()
        except Exception as erro:
            return f"Erro ao ler o tutorial: {erro}"
    return "Arquivo tutorial.md não encontrado."


def desenhar_tabela(container: ctk.CTkFrame, linhas_tabela: list) -> None:
    """Renderiza tabelas do Markdown (| A | S |) como grades visuais estilizadas."""
    linhas_processadas = []
    for linha in linhas_tabela:
        celulas = [c.strip() for c in linha[1:-1].split("|")]
        # Ignora linhas de alinhamento (|:---:|:---:|)
        if all(all(ch in "-: " for ch in c) for c in celulas if c):
            continue
        linhas_processadas.append(celulas)

    if not linhas_processadas:
        return

    frame_tabela = ctk.CTkFrame(
        container,
        fg_color=COR_BORDA_CARTAO,
        border_width=1,
        border_color=COR_BORDA_CARTAO,
        corner_radius=8
    )
    frame_tabela.pack(pady=12, padx=15, anchor="w")

    for num_linha, linha in enumerate(linhas_processadas):
        is_cabecalho = (num_linha == 0)
        cor_fundo = COR_FUNDO_TABELA_CABECALHO if is_cabecalho else COR_FUNDO_TABELA_CELULA
        peso = "bold" if is_cabecalho else "normal"

        for num_col, texto_celula in enumerate(linha):
            celula = ctk.CTkLabel(
                frame_tabela,
                text=texto_celula if texto_celula else " ",
                font=ctk.CTkFont(size=13, weight=peso),
                fg_color=cor_fundo,
                text_color=COR_TEXTO_PRINCIPAL,
                width=75,
                height=30,
                corner_radius=4
            )
            celula.grid(row=num_linha, column=num_col, padx=1, pady=1, sticky="nsew")


def renderizar_markdown(container: ctk.CTkScrollableFrame, texto: str) -> None:
    """
    Interpreta o texto em Markdown e HTML básico e cria widgets visuais
    nativos do CustomTkinter respeitando o tema (Claro/Escuro).
    """
    linhas = texto.splitlines()
    i = 0
    tamanho = len(linhas)

    while i < tamanho:
        linha = linhas[i].strip()

        if not linha:
            i += 1
            continue

        # 1. Títulos H1 (<h1> ou #)
        m_h1 = re.match(r"<h1[^>]*>(.*?)</h1>", linha, re.IGNORECASE)
        if m_h1 or linha.startswith("# "):
            texto_h1 = m_h1.group(1).strip() if m_h1 else linha[2:].strip()
            rotulo = ctk.CTkLabel(
                container,
                text=texto_h1,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=COR_DESTAQUE
            )
            rotulo.pack(pady=(20, 6), anchor="w", padx=10)
            i += 1
            continue

        # 2. Subtítulos H2 (<h2> ou ##)
        m_h2 = re.match(r"<h2[^>]*>(.*?)</h2>", linha, re.IGNORECASE)
        if m_h2 or linha.startswith("## "):
            texto_h2 = m_h2.group(1).strip() if m_h2 else linha[3:].strip()
            rotulo = ctk.CTkLabel(
                container,
                text=texto_h2,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=COR_TEXTO_PRINCIPAL
            )
            rotulo.pack(pady=(16, 4), anchor="w", padx=10)
            i += 1
            continue

        # 3. Seções H3 (###)
        if linha.startswith("### "):
            rotulo = ctk.CTkLabel(
                container,
                text=linha[4:].strip(),
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=COR_DESTAQUE
            )
            rotulo.pack(pady=(12, 2), anchor="w", padx=10)
            i += 1
            continue

        # 4. Itens de Lista (<li> ou - ou *)
        m_li = re.match(r"<li>(.*?)</li>?", linha, re.IGNORECASE)
        if m_li or linha.startswith(("- ", "* ")):
            texto_li = re.sub(r"<[^>]+>", "", m_li.group(1)).strip() if m_li else linha[2:].strip()
            espacos = len(linhas[i]) - len(linhas[i].lstrip())
            recuo_x = 25 if espacos < 4 else 45

            rotulo = ctk.CTkLabel(
                container,
                text=f"•  {texto_li}",
                font=ctk.CTkFont(size=13),
                text_color=COR_TEXTO_PRINCIPAL,
                justify="left"
            )
            rotulo.pack(anchor="w", padx=recuo_x, pady=2)
            i += 1
            continue

        if linha.lower() in ("<ul>", "</ul>", "</li>"):
            i += 1
            continue

        # 5. Tabelas Markdown (| col1 | col2 |)
        if linha.startswith("|") and linha.endswith("|"):
            linhas_tabela = []
            while i < tamanho and linhas[i].strip().startswith("|") and linhas[i].strip().endswith("|"):
                linhas_tabela.append(linhas[i].strip())
                i += 1
            desenhar_tabela(container, linhas_tabela)
            continue

        # 6. Linha horizontal (--- ou ***)
        if linha in ("---", "***", "___"):
            separador = ctk.CTkFrame(container, height=1, fg_color=COR_BORDA_CARTAO)
            separador.pack(fill="x", padx=10, pady=10)
            i += 1
            continue

        # 7. Parágrafos comuns (acumula linhas e trata <br>)
        paragrafo = [linha]
        i += 1
        while i < tamanho:
            prox = linhas[i].strip()
            if not prox or prox.startswith(("#", "|", "<h", "<ul", "<li", "-", "*", "---")):
                break
            paragrafo.append(prox)
            i += 1

        texto_limpo = re.sub(r"<[^>]+>", "", " ".join(paragrafo).replace("<br>", "\n"))
        rotulo = ctk.CTkLabel(
            container,
            text=texto_limpo,
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SECUNDARIO,
            justify="left",
            wraplength=730,
            anchor="w"
        )
        rotulo.pack(anchor="w", padx=10, pady=5)


# ==============================================================================
# 5. CONSTRUÇÃO DA INTERFACE GRÁFICA
# ==============================================================================
def criar(janela_raiz: ctk.CTk) -> None:
    """Constrói e exibe a Tela de Tutorial dentro da janela raiz."""
    janela_raiz.title("Khob - Tutorial")

    largura_monitor = janela_raiz.winfo_screenwidth()
    altura_monitor = janela_raiz.winfo_screenheight()
    largura_janela = min(largura_monitor - 200, 850)
    altura_janela = min(altura_monitor - 150, 650)
    posicao_horizontal = (largura_monitor - largura_janela) // 2
    posicao_vertical = (altura_monitor - altura_janela) // 2

    janela_raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_horizontal}+{posicao_vertical}")
    janela_raiz.minsize(650, 500)

    # 5.1 Container Rolável Principal
    container_rolavel = ctk.CTkScrollableFrame(
        janela_raiz,
        corner_radius=12,
        fg_color=COR_FUNDO_CARTAO,
        border_width=1,
        border_color=COR_BORDA_CARTAO
    )
    container_rolavel.pack(fill="both", expand=True, padx=20, pady=20)

    # 5.2 Barra Superior (Botão Voltar)
    barra_topo = ctk.CTkFrame(container_rolavel, fg_color="transparent")
    barra_topo.pack(fill="x", padx=10, pady=(10, 0))

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

    # 5.3 Logotipo
    if os.path.exists(CAMINHO_LOGO):
        try:
            imagem_redimensionada = Image.open(CAMINHO_LOGO).convert("RGBA").resize((80, 80))
            imagem_custom = ctk.CTkImage(
                light_image=imagem_redimensionada,
                dark_image=imagem_redimensionada,
                size=(80, 80)
            )
            rotulo_logo = ctk.CTkLabel(container_rolavel, image=imagem_custom, text="")
            rotulo_logo.pack(pady=(10, 5))
        except Exception as erro_carregamento:
            print(f"[Aviso] Não foi possível renderizar a logo: {erro_carregamento}")

    # 5.4 Renderiza todo o conteúdo do tutorial.md
    conteudo_md = carregar_markdown()
    renderizar_markdown(container_rolavel, conteudo_md)

    janela_raiz.deiconify()


# ==============================================================================
# 6. EXECUÇÃO ISOLADA / TESTE DIRETO
# ==============================================================================
if __name__ == "__main__":
    aplicativo_teste = ctk.CTk()
    criar(aplicativo_teste)
    aplicativo_teste.mainloop()