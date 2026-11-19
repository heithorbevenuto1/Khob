# ==============================================================================
# MODELO: CONVERSOR DE BASES NUMÉRICAS (BACK-END)
# ==============================================================================
"""
Módulo responsável pela lógica de validação e conversão entre sistemas numéricos:
Decimal, Binário, Octal e Hexadecimal.
"""

from typing import Dict


MAPA_BASES = {
    "Decimal": 10,
    "Binário": 2,
    "Octal": 8,
    "Hexadecimal": 16
}


def converter_bases(valor_texto: str, base_origem: str) -> Dict[str, str]:
    """
    Converte um número na base de origem especificada para Decimal, Binário,
    Octal e Hexadecimal.
    
    Parâmetros:
        valor_texto (str): O texto digitado pelo usuário.
        base_origem (str): "Decimal", "Binário", "Octal" ou "Hexadecimal".
        
    Retorno:
        dict contendo os resultados formatados:
            - 'binario': representação binária sem prefixo '0b'
            - 'decimal': representação decimal
            - 'octal': representação octal sem prefixo '0o'
            - 'hexadecimal': representação hexadecimal maiúscula sem prefixo '0x'
            
    Levanta:
        ValueError: Caso o valor seja vazio ou contenha caracteres incompatíveis com a base.
    """
    texto_limpo = valor_texto.strip()

    if not texto_limpo:
        raise ValueError("Por favor, digite um valor para converter.")

    base_numerica = MAPA_BASES.get(base_origem)
    if base_numerica is None:
        raise ValueError(f"Base de origem desconhecida: '{base_origem}'.")

    try:
        numero_inteiro = int(texto_limpo, base_numerica)
    except ValueError:
        raise ValueError(f"O valor informado não é válido para a base {base_origem}.")

    if numero_inteiro < 0:
        # Se for negativo, formata mantendo o sinal
        bin_str = "-" + bin(numero_inteiro)[3:]
        oct_str = "-" + oct(numero_inteiro)[3:]
        hex_str = "-" + hex(numero_inteiro)[3:].upper()
    else:
        bin_str = bin(numero_inteiro)[2:]
        oct_str = oct(numero_inteiro)[2:]
        hex_str = hex(numero_inteiro)[2:].upper()

    return {
        "binario": bin_str,
        "decimal": str(numero_inteiro),
        "octal": oct_str,
        "hexadecimal": hex_str
    }
