import os
import tkinter as tk
from PIL import Image, ImageTk
from view.estilo import aplicar_css, classe

imagem_original = Image.open("Khob-main/imagens/1000138096.png").convert("RGBA")


def criar(raiz, ao_terminar):
    """Mostra o splash. Quando acabar, fecha e chama ao_terminar()."""
    tela = tk.Toplevel(raiz)
    tela.title("Carregando...")

    ltela = tela.winfo_screenwidth()
    atela = tela.winfo_screenheight()
    largura = ltela - int((ltela // 2) * 1.4)
    altura = atela - int((atela // 2) * 1.4)
    px = (ltela - largura) // 2
    py = (atela - altura) // 2
    tela.geometry(f"{largura}x{altura}+{px}+{py}")
    tela.overrideredirect(True)   # sem barra de título (splash)

    imagem_redimensionada = imagem_original.resize((200, 200))
    imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)

    label_imagem = tk.Label(tela, image=imagem_tk)
    label_imagem.image = imagem_tk   # evita o Python apagar a imagem da memória
    label_imagem.pack(pady=20)

    classe(tk.Label(tela, text="Carregando o sistema..."), "titulo").pack(pady=5)

    aplicar_css(tela)

    def fechar():
        tela.destroy()
        ao_terminar()

    tela.after(3000, fechar)
