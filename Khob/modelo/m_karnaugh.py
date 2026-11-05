def karnaugh(saida):
    saida = saida.upper().replace(" ", "") #transforma todos os caracteres em maiúsculo (upper()) e remove espaços (replace(" ", ""))
    
    # utiliza condições (compara por meio do len o tamanho de 'saida') iniciando do menor para o maior, se possuir mais casas que a primeira condição ele vai pra segunda e assim por diante, até chegar na condição que se encaixa
    if len(saida) <= 4:
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
        #se o a entrada do usuario for maior que o maior karnaugh suportado pelo sistema, ele vai imprimir uma mensagem de erro
    else:
        print("Entrada grande demais (máx. 16).")
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
    while True:
        entrada = input("Digite (apenas 0, 1 e X): ").upper() #é onde o usuario digita sua entrada, e o upper() transforma todos os caracteres em maiúsculo, para que o sistema não se confunda com letras minusculas
    
        if not entrada: #porta logica NOT, se o usuario não digitou nada e apertou enter, ele vai imprimir uma mensagem de erro e continuar o loop
            print("Entrada vazia.")
            continue
    
        if all(c in "01X" for c in entrada): #ele verifica se todos os caracteres da entrada do usuario são validos, sendo 0,1,X, caso for ele vai chamar a função
            karnaugh(entrada) #função karnough usando a entrada do usuario como parametro
        #break #esta comentado pq quero que seja um loop infinito, caso queira que pare apos a a resposta é só retira o # do break
        else: #caso possua algum valor equivocado ele vai imprimir a mensagem de erro
            invalidos = set(entrada) - set("01X") #invalo são todos valores da entrada exceto 0,1,X
            print(f"Caracteres inválidos: {invalidos}")

