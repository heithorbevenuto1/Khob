import re
import os
import tkinter as tk

try:
    import pywinstyles
except ImportError:
    pywinstyles = None

CAMINHO_CSS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tema.css")

MAPA_PROPRIEDADES = {
    "background": "bg",
    "background-color": "bg",
    "color": "fg",
    "foreground": "fg",
    "border-width": "bd",
    "border": "bd",
    "padding-x": "padx",
    "padding-y": "pady",
    "width": "width",
    "height": "height",
    "cursor": "cursor",
    "relief": "relief",
    "justify": "justify",
    "text-align": "justify",
}
PROPRIEDADES_FONTE = {"font-family", "font-size", "font-weight", "font-style"}


def _limpar_valor(valor):
    return valor.strip().strip('"').strip("'").strip()


def ler_css(caminho=CAMINHO_CSS):
    """Devolve {seletor: {propriedade: valor}}. Nunca levanta erro."""
    regras = {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
    except OSError as e:
        print(f"[CSS] Não consegui abrir '{caminho}': {e}")
        return regras

    texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)

    for seletores, corpo in re.findall(r"([^{}]+)\{([^{}]*)\}", texto):
        props = {}
        for decl in corpo.split(";"):
            if ":" not in decl:
                if decl.strip():
                    print(f"[CSS] Linha ignorada (sem ':'): {decl.strip()!r}")
                continue
            chave, valor = decl.split(":", 1)
            props[chave.strip().lower()] = _limpar_valor(valor)

        for seletor in seletores.split(","):
            seletor = seletor.strip()
            if seletor:
                regras.setdefault(seletor, {}).update(props)
    return regras


def _montar_fonte(props):
    familia = props.get("font-family", "Segoe UI")
    try:
        tamanho = int(float(props.get("font-size", 10)))
    except ValueError:
        print(f"[CSS] font-size inválido: {props.get('font-size')!r}")
        tamanho = 10
    estilos = []
    if props.get("font-weight", "").lower() == "bold":
        estilos.append("bold")
    if props.get("font-style", "").lower() == "italic":
        estilos.append("italic")
    return (familia, tamanho, " ".join(estilos)) if estilos else (familia, tamanho)


def _aplicar_no_widget(widget, props):
    opcoes = {MAPA_PROPRIEDADES[k]: v for k, v in props.items() if k in MAPA_PROPRIEDADES}
    if PROPRIEDADES_FONTE & props.keys():
        opcoes["font"] = _montar_fonte(props)

    for opcao, valor in opcoes.items():
        try:
            widget.configure(**{opcao: valor})
        except tk.TclError:
            pass  # esse widget não tem essa opção


def _barra_windows(janela, props):
    if pywinstyles is None:
        return
    try:
        if "header-color" in props:
            pywinstyles.change_header_color(janela, color=props["header-color"])
        if "border-color" in props:
            pywinstyles.change_border_color(janela, color=props["border-color"])
    except Exception as e:
        print(f"[CSS] Não consegui pintar a barra do Windows: {e}")


def _todos_os_widgets(raiz):
    yield raiz
    for filho in raiz.winfo_children():
        yield from _todos_os_widgets(filho)


def classe(widget, nome):
    """Marca um widget com uma classe CSS e devolve o próprio widget.
    Uso: classe(tk.Label(...), "titulo")  ->  Label.titulo { ... }"""
    widget.css_class = nome
    return widget


def aplicar_css(janela, caminho=CAMINHO_CSS):
    """Aplica o CSS na janela e em tudo que está dentro dela."""
    regras = ler_css(caminho)

    for widget in _todos_os_widgets(janela):
        tipo = widget.winfo_class()               # "Tk", "Label", "Button"...
        seletores = ["*", tipo]
        nome = getattr(widget, "css_class", None)
        if nome:
            seletores += [f".{nome}", f"{tipo}.{nome}"]

        for seletor in seletores:                 # o mais específico vem por último
            if seletor in regras:
                _aplicar_no_widget(widget, regras[seletor])

    janela.update()
    _barra_windows(janela, regras.get(janela.winfo_class(), {}))