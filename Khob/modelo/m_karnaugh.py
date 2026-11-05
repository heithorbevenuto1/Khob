def karnaugh(saida):
    saida = saida.upper().replace(" ", "")
    
    # --- decide o tamanho do mapa ---
    if len(saida) <= 4:
        alvo = 4
        def montar():
            mapa = [
                [n[0], n[1]],
                [n[2], n[3]],
            ]
            return mapa
    elif len(saida) <= 8:
        alvo = 8
        def montar():
            mapa = [
                [n[0], n[1], n[3], n[2]],
                [n[4], n[5], n[7], n[6]],
            ]
            return mapa
    elif len(saida) <= 16:
        alvo = 16
        def montar():
            mapa = [
                [n[0],  n[1],  n[3],  n[2]],
                [n[4],  n[5],  n[7],  n[6]],
                [n[12], n[13], n[15], n[14]],
                [n[8],  n[9],  n[11], n[10]],
            ]
            return mapa
    else:
        print("Entrada grande demais (máx. 16).")
        return
    
    # --- completa com X até o tamanho do mapa ---
    while len(saida) < alvo:
        saida += "X"
    
    # --- agora sim, cria a lista n DEPOIS de completar ---
    n = list(saida)
    
    # --- monta e imprime ---
    mapa = montar()
    print("\nMapa de Karnaugh:")
    for linha in mapa:
        print("  ".join(linha))
    print()


# --- loop principal ---
while True:
    entrada = input("Digite (apenas 0, 1 e X): ").upper()
    
    if not entrada:
        print("Entrada vazia.")
        continue
    
    if all(c in "01X" for c in entrada):
        karnaugh(entrada)
        break
    else:
        invalidos = set(entrada) - set("01X")
        print(f"Caracteres inválidos: {invalidos}")
