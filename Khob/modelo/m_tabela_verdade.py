# ==============================================================================
# MODELO: TABELA VERDADE (BACK-END)
# ==============================================================================
"""
Módulo responsável pela geração e estruturação lógica da Tabela Verdade.
Calcula combinações binárias das variáveis de entrada e associa às saídas correspondentes.
"""

from typing import List, Dict, Any, Optional

# Letras padrão para nomeação sequencial das variáveis booleanas
NOMES_VARIAVEIS = ["A", "B", "C", "D", "E", "F", "G", "H"]


def calcular_quantidade_variaveis(tamanho_saida: int) -> int:
    """
    Determina o número mínimo de variáveis necessárias para cobrir o tamanho da saída.
    
    Parâmetros:
        tamanho_saida (int): Comprimento da sequência binária de saída.
        
    Retorno:
        int: Quantidade de variáveis booleanas (mínimo 1, máximo 7).
    """
    if tamanho_saida <= 2:
        return 1
    elif tamanho_saida <= 4:
        return 2
    elif tamanho_saida <= 8:
        return 3
    elif tamanho_saida <= 16:
        return 4
    elif tamanho_saida <= 32:
        return 5
    elif tamanho_saida <= 64:
        return 6
    else:
        return 7


def gerar_tabela_verdade(
    sequencia_saida: str,
    quantidade_variaveis: Optional[int] = None
) -> Dict[str, Any]:
    """
    Gera a estrutura de dados completa para a renderização da Tabela Verdade.
    
    Parâmetros:
        sequencia_saida (str): Sequência de bits/caracteres ('0', '1', 'X').
        quantidade_variaveis (int, opcional): Número explícito de variáveis. Se omitido,
                                              será calculado automaticamente.
                                              
    Retorno:
        dict: Estrutura contendo:
            - 'variaveis': List[str] -> Lista com nomes das variáveis (ex: ['A', 'B'])
            - 'cabecalho': List[str] -> Cabeçalhos das colunas (ex: ['#', 'A', 'B', 'S'])
            - 'linhas': List[dict] -> Lista de linhas com mintermo, bits e valor de saída
            - 'total_linhas': int -> Quantidade total de linhas (2^n)
    """
    sequencia_limpa = sequencia_saida.upper().replace(" ", "")

    if quantidade_variaveis is None:
        qtd_vars = calcular_quantidade_variaveis(len(sequencia_limpa))
    else:
        qtd_vars = max(1, min(quantidade_variaveis, 7))

    total_linhas = 1 << qtd_vars  # 2^qtd_vars
    nomes_vars = NOMES_VARIAVEIS[:qtd_vars]
    cabecalho = ["#"] + nomes_vars + ["S"]

    linhas: List[Dict[str, Any]] = []
    for indice in range(total_linhas):
        binario_formatado = f"{indice:0{qtd_vars}b}"
        bits = list(binario_formatado)
        valor_saida = sequencia_limpa[indice] if indice < len(sequencia_limpa) else "X"

        linhas.append({
            "indice": indice,
            "bits": bits,
            "saida": valor_saida
        })

    return {
        "variaveis": nomes_vars,
        "cabecalho": cabecalho,
        "linhas": linhas,
        "total_linhas": total_linhas
    }
