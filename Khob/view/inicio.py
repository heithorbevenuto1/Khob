import tkinter as tk
from view.estilo import aplicar_css, classe


def criar(raiz):
    """Monta a tela inicial dentro da janela raiz."""
    raiz.title("Programa Principal")

    ltela = raiz.winfo_screenwidth()
    atela = raiz.winfo_screenheight()
    largura = ltela - 300
    altura = atela - 300
    px = (ltela - largura) // 2
    py = (atela - altura) // 2
    raiz.geometry(f"{largura}x{altura}+{px}+{py}")

    classe(tk.Label(raiz, text="Bem-vindo ao Programa Principal!"), "titulo").pack(pady=100)
    tk.Button(raiz, text="Clique aqui").pack()

    raiz.deiconify()   # mostra a raiz (ela começa escondida durante o loading)
    aplicar_css(raiz)

    # F5 recarrega o CSS sem fechar o programa
    raiz.bind("<F5>", lambda e: aplicar_css(raiz))
