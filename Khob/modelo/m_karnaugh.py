# ==============================================================================
# MODELO: MAPA DE KARNAUGH (BACK-END)
# ==============================================================================
"""
Módulo responsável pela lógica de montagem, validação e estruturação
do Mapa de Karnaugh para diferentes dimensões (1 a 7 variáveis).
"""

from typing import List, Dict, Any, Optional, Tuple

TAMANHOS_VALIDOS = (2, 4, 8, 16, 32, 64, 128)


def validar_entrada_karnaugh(
    saida: str,
    tamanho_limite: Optional[int] = None
) -> Tuple[bool, str, str]:
    """
    Valida a sequência inserida pelo usuário para o Mapa de Karnaugh.
    
    Parâmetros:
        saida (str): Sequência digitada.
        tamanho_limite (int, opcional): Quantidade de células exigida pelo tamanho selecionado.
        
    Retorno:
        Tuple[bool, str, str]: (sucesso, mensagem_erro, sequencia_limpa)
    """
    sequencia_limpa = saida.upper().replace(" ", "")

    if not sequencia_limpa:
        return False, "Entrada vazia. Digite ao menos um valor (0, 1 ou X).", ""

    if not all(c in "01X" for c in sequencia_limpa):
        caracteres_invalidos = sorted(list(set(sequencia_limpa) - set("01X")))
        return False, f"Caracteres inválidos encontrados: {', '.join(caracteres_invalidos)}.", ""

    if len(sequencia_limpa) > 128:
        return False, "Entrada muito longa (limite máximo suportado de 128 bits).", ""

    if tamanho_limite is not None:
        if len(sequencia_limpa) > tamanho_limite:
            return False, (
                f"O tamanho selecionado suporta no máximo {tamanho_limite} casas, "
                f"mas foram digitados {len(sequencia_limpa)} bits."
            ), ""

    return True, "", sequencia_limpa


def calcular_alvo(tamanho_saida: int, tamanho_forçado: Optional[int] = None) -> int:
    """
    Determina a capacidade total de casas do mapa (2, 4, 8, 16, 32, 64 ou 128).
    """
    if tamanho_forçado is not None and tamanho_forçado in TAMANHOS_VALIDOS:
        return tamanho_forçado

    for tamanho in TAMANHOS_VALIDOS:
        if tamanho_saida <= tamanho:
            return tamanho

    return 128


def gerar_dados_karnaugh(
    saida: str,
    tamanho_forçado: Optional[int] = None
) -> Dict[str, Any]:
    """
    Processa a sequência lógica e devolve a matriz do mapa acompanhada
    dos rótulos das linhas, colunas e variáveis correspondentes.
    
    Parâmetros:
        saida (str): Sequência de saída lógica (0, 1, X).
        tamanho_forçado (int, opcional): Tamanho forçado pelo seletor de dimensão.
        
    Retorno:
        dict com:
            - 'alvo': int
            - 'num_variaveis': int
            - 'rotulo_canto': str (ex: 'AB \\ CD')
            - 'vars_linha': str
            - 'vars_coluna': str
            - 'rotulos_linhas': List[str]
            - 'rotulos_colunas': List[str]
            - 'matriz': List[List[str]]
            - 'saida_completa': str
            - 'dimensao': str (ex: '4x4')
    """
    sequencia = saida.upper().replace(" ", "")
    alvo = calcular_alvo(len(sequencia), tamanho_forçado)

    # Preenche com X caso a sequência seja menor que o alvo
    while len(sequencia) < alvo:
        sequencia += "X"

    n = list(sequencia)

    if alvo == 2:
        num_variaveis = 1
        vars_linha = ""
        vars_coluna = "A"
        rotulo_canto = "A"
        rotulos_linhas = ["S"]
        rotulos_colunas = ["0", "1"]
        matriz = [[n[0], n[1]]]
        dimensao = "1x2"

    elif alvo == 4:
        num_variaveis = 2
        vars_linha = "A"
        vars_coluna = "B"
        rotulo_canto = "A \\ B"
        rotulos_linhas = ["0", "1"]
        rotulos_colunas = ["0", "1"]
        matriz = [
            [n[0], n[1]],
            [n[2], n[3]],
        ]
        dimensao = "2x2"

    elif alvo == 8:
        num_variaveis = 3
        vars_linha = "A"
        vars_coluna = "BC"
        rotulo_canto = "A \\ BC"
        rotulos_linhas = ["0", "1"]
        rotulos_colunas = ["00", "01", "11", "10"]
        matriz = [
            [n[0], n[1], n[3], n[2]],
            [n[4], n[5], n[7], n[6]],
        ]
        dimensao = "2x4"

    elif alvo == 16:
        num_variaveis = 4
        vars_linha = "AB"
        vars_coluna = "CD"
        rotulo_canto = "AB \\ CD"
        rotulos_linhas = ["00", "01", "11", "10"]
        rotulos_colunas = ["00", "01", "11", "10"]
        matriz = [
            [n[0],  n[1],  n[3],  n[2]],
            [n[4],  n[5],  n[7],  n[6]],
            [n[12], n[13], n[15], n[14]],
            [n[8],  n[9],  n[11], n[10]],
        ]
        dimensao = "4x4"

    elif alvo == 32:
        num_variaveis = 5
        vars_linha = "AB"
        vars_coluna = "CDE"
        rotulo_canto = "AB \\ CDE"
        rotulos_linhas = ["00", "01", "11", "10"]
        rotulos_colunas = ["000", "001", "011", "010", "110", "111", "101", "100"]
        matriz = [
            [n[0],  n[1],  n[3],  n[2],  n[6],  n[7],  n[5],  n[4]],
            [n[8],  n[9],  n[11], n[10], n[14], n[15], n[13], n[12]],
            [n[24], n[25], n[27], n[26], n[30], n[31], n[29], n[28]],
            [n[16], n[17], n[19], n[18], n[22], n[23], n[21], n[20]],
        ]
        dimensao = "4x8"

    elif alvo == 64:
        num_variaveis = 6
        vars_linha = "ABC"
        vars_coluna = "DEF"
        rotulo_canto = "ABC \\ DEF"
        rotulos_linhas = ["000", "001", "011", "010", "110", "111", "101", "100"]
        rotulos_colunas = ["000", "001", "011", "010", "110", "111", "101", "100"]
        matriz = [
            [n[0],  n[1],  n[3],  n[2],  n[6],  n[7],  n[5],  n[4]],
            [n[8],  n[9],  n[11], n[10], n[14], n[15], n[13], n[12]],
            [n[24], n[25], n[27], n[26], n[30], n[31], n[29], n[28]],
            [n[16], n[17], n[19], n[18], n[22], n[23], n[21], n[20]],
            [n[48], n[49], n[51], n[50], n[54], n[55], n[53], n[52]],
            [n[56], n[57], n[59], n[58], n[62], n[63], n[61], n[60]],
            [n[40], n[41], n[43], n[42], n[46], n[47], n[45], n[44]],
            [n[32], n[33], n[35], n[34], n[38], n[39], n[37], n[36]],
        ]
        dimensao = "8x8"

    else:  # alvo == 128
        num_variaveis = 7
        vars_linha = "ABCD"
        vars_coluna = "EFG"
        rotulo_canto = "ABCD \\ EFG"
        rotulos_linhas = [
            "0000", "0001", "0011", "0010", "0110", "0111", "0101", "0100",
            "1100", "1101", "1111", "1110", "1010", "1011", "1001", "1000"
        ]
        rotulos_colunas = ["000", "001", "011", "010", "110", "111", "101", "100"]
        matriz = [
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
        dimensao = "8x16"

    return {
        "alvo": alvo,
        "num_variaveis": num_variaveis,
        "rotulo_canto": rotulo_canto,
        "vars_linha": vars_linha,
        "vars_coluna": vars_coluna,
        "rotulos_linhas": rotulos_linhas,
        "rotulos_colunas": rotulos_colunas,
        "matriz": matriz,
        "saida_completa": sequencia,
        "dimensao": dimensao
    }


def karnaugh(saida: str) -> None:
    """
    Função utilitária legada para exibição em terminal / console.
    """
    dados = gerar_dados_karnaugh(saida)
    print("\nMapa de Karnaugh:")
    for linha in dados["matriz"]:
        print(" | ".join(linha))
    print()


def karnaugh_loop() -> None:
    """
    Loop interativo para testes via terminal / console.
    """
    print("=" * 64)
    print("                            Khob")
    print("=" * 64)
    while True:
        print("O programa aceita: (0), (1), (x) e (X)")
        entrada = input(":> ")

        valido, mensagem, sequencia_limpa = validar_entrada_karnaugh(entrada)
        if not valido:
            print(f"[Aviso] {mensagem}")
            continue

        karnaugh(sequencia_limpa)


if __name__ == "__main__":
    karnaugh_loop()
