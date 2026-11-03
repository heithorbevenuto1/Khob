


#saida é o nome que se da aos valores consi
def karnaugh(saida):
    n = [c for c in saida]  # lista de caracteres
    tamanho = len(saida)
    if tamanho <= 3:

        def k2x2():
            mapa = [
                [n[0], n[1]],
                [n[2], n[3]],
            ]
            print(mapa)

        return k2x2
    elif (3 < tamanho) and (tamanho <= 7):

        def k2x4():
            mapa = [
                [n[0], n[1], n[3], n[2]],
                [n[4], n[5], n[7], n[6]],
            ]
            print(mapa)
        print(k2x4, sep="  ")
    elif 7 < tamanho : # and saida <=15: #adicione essa parte caso aumente o programa e adicione mapas maiores 

        def k4x4():
            mapa = [
                [n[0],  n[1],  n[3],  n[2]],
                [n[4],  n[5],  n[7],  n[6]],
                [n[12], n[13], n[15], n[14]],
                [n[8],  n[9],  n[11], n[10]],
            ]
            print(mapa)

while True:  # Loop infinito: só sai quando o usuário digitar algo válido (break)
    saida = input("Digite (apenas 0, 1 e X): ").upper()
    # .upper() converte tudo para maiúsculo, então 'x' vira 'X'
    # (útil para aceitar 'x' ou 'X' sem diferenciar)

    if all(c in "01X" for c in saida):
        karnaugh(saida)
        # all(...) verifica se TODOS os elementos são True.
        # O generator `c in "01X" for c in saida` percorre cada caractere e retorna True se ele for '0', '1' ou 'X'.

        
    
'''
    else:
        invalidos = set(saida) - set("01X")
    # set(saida)       → conjunto de caracteres únicos digitados
    # set("01X")       → conjunto dos caracteres permitidos {'0','1','X'}
    # A diferença (-) retorna apenas os caracteres NÃO permitidos
    # Ex.: "10A2!" → {'A','2','!'} (mostra só os inválidos, sem repetição)

        print(f" Caracteres inválidos: {invalidos}")
    # Informa ao usuário o que está errado e o loop recomeça
'''
