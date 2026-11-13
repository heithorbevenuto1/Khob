def karnaugh(saida):
    saida = saida.upper().replace(" ", "") #transforma todos os caracteres em maiúsculo (upper()) e remove espaços (replace(" ", ""))
    
    # utiliza condições (compara por meio do len o tamanho de 'saida') iniciando do menor para o maior, se possuir mais casas que a primeira condição ele vai pra segunda e assim por diante, até chegar na condição que se encaixa
    if len(saida) <= 2: #o de 1 variavel não é utilizado de forma seria, sua aplicação neste programa para ser o mais completo possivel e atender todos objetivos que os usuarios possom necessitar
        alvo = 2
        def montar():
            mapa = [
                n[0],n[1],
            ]
            return mapa
    
    elif len(saida) <= 4:
        alvo = 4 #este é o temanho ideal, sendo 4,8, 16, essa variavel sera usada posteriormente pra adicionar X
        def montar(): 
            #função que monta o karnaugh, ela é igual pra todas pq só uma é ativada
            #karnaugh 2x2 ou 4 variaveis(4 bits)
            mapa = [
                [n[0], n[1]],
                [n[2], n[3]],
            ]
            return mapa #retorna o mapa montado

        #em seguida todos elifs sâo iguais ao primeiro if e seguem a mesma lógica
    elif len(saida) <= 8:
        alvo = 8
        def montar():
            #karnaugh 2x4 ou 3 variaveis(3 bits)
            mapa = [
                [n[0], n[1], n[3], n[2]],
                [n[4], n[5], n[7], n[6]],
            ]
            return mapa
    elif len(saida) <= 16:
        alvo = 16
        def montar():
            #karnaugh 4x4 ou 4 variaveis(4 bits)
            mapa = [
                [n[0],  n[1],  n[3],  n[2]],
                [n[4],  n[5],  n[7],  n[6]],
                [n[12], n[13], n[15], n[14]],
                [n[8],  n[9],  n[11], n[10]],
            ]
            return mapa
    elif len(saida) <= 32:
        alvo = 32
        def montar():
            #karnaugh 4x8 ou 5 variaveis(5 bits)
            mapa = [
                [n[0],  n[1],  n[3],  n[2],  n[6],  n[7],  n[5],  n[4]],
                [n[8],  n[9],  n[11], n[10], n[14], n[15], n[13], n[12]],
                [n[24], n[25], n[27], n[26], n[30], n[31], n[29], n[28]],
                [n[16], n[17], n[19], n[18], n[22], n[23], n[21], n[20]],   
            ]
            return mapa

    elif len(saida) <= 64:
        alvo = 64
        def montar():
            #karnaugh 4x8 ou 5 variaveis(5 bits)
            mapa = [
                [n[0],  n[1],  n[3],  n[2],  n[6],  n[7],  n[5],  n[4]],
                [n[8],  n[9],  n[11], n[10], n[14], n[15], n[13], n[12]],
                [n[24], n[25], n[27], n[26], n[30], n[31], n[29], n[28]],
                [n[16], n[17], n[19], n[18], n[22], n[23], n[21], n[20]],
                [n[48], n[49], n[51], n[50], n[54], n[55], n[53], n[52]],
                [n[56], n[57], n[59], n[58], n[62], n[63], n[61], n[60]],
                [n[40], n[41], n[43], n[42], n[46], n[47], n[45], n[44]],
                [n[32], n[33], n[35], n[34], n[38], n[39], n[37], n[36]],
            ]
            return mapa

    elif len(saida) <= 128:
        alvo = 128
        def montar():
            #karnaugh 8x8 ou 7 variaveis(7 bits)
            mapa = [
                [n[0],   n[1],   n[3],   n[2],   n[6],   n[7],   n[5],   n[4]],
                [n[8],   n[9],   n[11],  n[10],  n[14],  n[15],  n[13],  n[12]],
                [n[24],  n[25],  n[27],  n[26],  n[30],  n[31],  n[29],  n[28]],
                [n[16],  n[17],  n[19],  n[18],  n[22],  n[23],  n[21],  n[20]],
                [n[48],  n[49],  n[51],  n[50],  n[54],  n[55],  n[53],  n[52]],
                [n[56],  n[57],  n[59],  n[58],  n[62],  n[63],  n[61],  n[60]],
                [n[40],  n[41],  n[43],  n[42],  n[46],  n[47],  n[45],  n[44]],
                [n[32],  n[33],  n[35],  n[34],  n[38],  n[39],  n[37],  n[36]],
                [n[96],  n[97],  n[99],  n[98],  n[102], n[103], n[101], n[100]],
                [n[104], n[105], n[107], n[106], n[110], n[111], n[109], n[108]],
                [n[120], n[121], n[123], n[122], n[126], n[127], n[125], n[124]],
                [n[112], n[113], n[115], n[114], n[118], n[119], n[117], n[116]],
                [n[80],  n[81],  n[83],  n[82],  n[86],  n[87],  n[85],  n[84]],
                [n[88],  n[89],  n[91],  n[90],  n[94],  n[95],  n[93],  n[92]],
                [n[72],  n[73],  n[75],  n[74],  n[78],  n[79],  n[77],  n[76]],
                [n[64],  n[65],  n[67],  n[66],  n[70],  n[71],  n[69],  n[68]],
            ]
            return mapa
        #se o a entrada do usuario for maior que o maior karnaugh suportado pelo sistema, ele vai imprimir uma mensagem de erro
    else:
        print("Entrada grande demais (máx. 128).")
        return
    
    # aqui ele verificara se a entrada atinge um numero de base 2, como 4,8 ou 16, se estiver entre um e outro mas faltar bits, ele completara com X, que é o valor neutro do karnaugh
    while len(saida) < alvo:
        saida += "X" #enquanto a saida for menor que alvo ele vai ganhar um x
    
    # n lista cada caracter da saida, para que possa ser montado o mapa a partir de um texto unitario e não de um lista, que alem de ser mais simples de manusear, tambem requer menos processamento (no de 16bits pode ser 3 vezes mais leve)
    n = list(saida)
    
    # --- monta e imprime o mapa---
    mapa = montar()
    print("\nMapa de Karnaugh:")
    for linha in mapa: #a linha percorre o mapa
        print(" | ".join(linha)) #coloca uma bara em cada linha e junta os elementos
    print()#quebra de linha



def karnaugh_loop():
    # loop é infinito (por causa do while True), caso o break que esta comentado no if all continue comentado
    print("" \
    "================================================================" \
    "                            Khob" \
    "================================================================")
    while True:
        print("O programa aceita: (0),(1),(x) e (X)")
        entrada = input(":> ").upper() #é onde o usuario digita sua entrada, e o upper() transforma todos os caracteres em maiúsculo, para que o sistema não se confunda com letras minusculas
    
        if not entrada: #porta logica NOT, se o usuario não digitou nada e apertou enter, ele vai imprimir uma mensagem de erro e continuar o loop
            print("Entrada vazia.")
            continue
    
        if all(c in "01X" for c in entrada): #ele verifica se todos os caracteres da entrada do usuario são validos, sendo 0,1,X, caso for ele vai chamar a função
            karnaugh(entrada) #função karnough usando a entrada do usuario como parametro
        #break #esta comentado pq quero que seja um loop infinito, caso queira que pare apos a a resposta é só retira o # do break
        else: #caso possua algum valor equivocado ele vai imprimir a mensagem de erro
            invalidos = set(entrada) - set("01X") #invalo são todos valores da entrada exceto 0,1,X
            print(f"Caracteres inválidos: {invalidos}")

#karnaugh_loop()
