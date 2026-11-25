<h1 align=center>KARNAUGH</h1>
<h2 align=center>Indice</h2>

<ul>
  <li>O que é</li>
  <li>Tabela verdade e variáveis de entrada e saída</li>
  <li>Como usar Karnaugh
    <ul>
      <li>1 variavel  (1x2 - 2 bits)</li>
      <li>2 variáveis (2x2 - 4 bits)</li>
      <li>3 variáveis (2x4 - 8 bits)</li>
      <li>4 variáveis (4x4 - 16 bits)</li>
      <li>5 variaveis (4x8 - 32 bits)</li>
      <li>6 variaveis (8x8 - 64 bits)</li>
      <li>7 variaveis (8x16 - 128 bits)</li>
    </ul>
  </li>
  <li>Como usa a aplicação</li>
</ul>

# Sobre a aplicação

## Como utilizar
<li>Mapa de Karnaugh: Acesse a ferramenta pelo menu inicial, insira uma sequência de valores binários (0 e 1), podendo utilizar X para condições indiferentes. Escolha o tamanho do mapa ou utilize a opção automática e gere o resultado para visualizar o mapa e a tabela verdade.

<li>Conversor de Bases: Acesse o conversor, digite o número desejado, selecione sua base de origem (Binária, Decimal, Octal ou Hexadecimal) e clique em converter. O programa apresentará os valores equivalentes nas outras bases.

<li>Módulo de Treinamento: Utilize essa opção para estudar os conceitos de Mapas de Karnaugh, variáveis, tabelas verdade e formação de grupos.

<li>Configurações: Permite configurar e personalizar a aparência do programa, por exemplo, escolhendo entre os temas claro, escuro ou automático.


# Sobre o assunto
## O que é
O Mapa de Karnaugh é um método de simplificação lógica em eletrônica digital mais eficiente e fácil que o uso de expressões booleanas.<br>Enquanto a álgebra booleana exige aplicar dezenas de regras (De Morgan, absorção, distribuição...), o mapa resolve a mesma simplificação apenas visualmente, agrupando células vizinhas. <br>O mapa de Karnaugh pega os bits da saída e organiza em um mapa. Essa organização é feita para achar a fórmula do circuito lógico.

## Tabela verdade e variáveis de entrada e saída

O mapa de karnaugh é utilizado até 6 variáveis, o mais comum de se ver é de 2,3 e 4 variáveis.Mais do que 6 perde a vantagem visual. Entretanto, o programa suporta até 7 variaveis (128 bits) por futuras intenções de resolução por formula automatica
### S
Neste artigo usaremos o S como saída, enquanto as letras iniciando em A serão a entrada, por ir até 6 elas são: A,B,C,D,E e F. Entretanto, o uso de 5 ou 6 variáveis é pouco usado, logo a aplicação usara <br>A saída não segue um valor fixo, ela vai variar dependendo das necessidades do circuito, portanto neste arquivo ela será representada com espaços vazios.


### Tabela verdade 
A tabela é onde se organiza a saida lógica por meio da decisão de cada entrada, temos as variaveis (ABCDEF) no modelo padrão e o adotado pelo programa KHOB e sua equipe de desenvolvimento. Cada varivel é uma entrada, podendo ser ligado (1) ou desligado (0). Com isso pode-se analisar para achar a saida deseja, exemplo: quando o botão A estiver ligado (1) e B desligado (0) quero que a saida esteja ligada (1), logo:
|A|B|S|
|-|-|-|
|1|0|1|


a organização da das portas vai de A até F (depende do numero de variaveis), da esquerda para a direita, o pulo a organização varia de 0 e 1, onde o do lado é metade da anterior, exemplo:

|A|B|C|S|
|-|-|-|-|
|0|0|0| |
|0|0|1| |
|0|1|0| |
|0|1|1| |
|1|0|0| |
|1|0|1| |
|1|1|0| |
|1|1|1| |
### 1 variável
A tabela verdade com uma variável possui apenas 1 entrada e dois estados, desligado (0) e ligado (1), junto a isso possui poucas possibilidades de circuito.<br>Seu uso pode ser resumido a ligado e desligado.
|A|S|
|-|-|
|0| |
|1| |

### 2 variáveis
A tabela verdade de 2 variaveis possuicomeça a ser mais usual, a cada varivael adicionada a tabela dobra
|A|B|S|
|-|-|-|
|0|0| |
|0|1| | 
|1|0| |
|1|1| |
### 3 variaveis
|A|B|C|S|
|-|-|-|-|
|0|0|0| |
|0|0|1| |
|0|1|0| | 
|0|1|1| | 
|1|0|0| |
|1|0|1| |
|1|1|0| |  
|1|1|1| | 

### 4 variaveis

|A|B|C|D|S|
|-|-|-|-|-|
|0|0|0|0| |
|0|0|0|1| |
|0|0|1|0| |
|0|0|1|1| |
|0|1|0|0| | 
|0|1|0|1| |
|0|1|1|0| |
|0|1|1|1| |
|1|0|0|0| |
|1|0|0|1| |
|1|0|1|0| |
|1|0|1|1| |
|1|1|0|0| |
|1|1|0|1| |
|1|1|1|0| |
|1|1|1|1| | 

### 5 variaveis

|A|B|C|D|E|S|
|-|-|-|-|-|-|
|0|0|0|0|0| |
|0|0|0|0|1| | 
|0|0|0|1|0| | 
|0|0|0|1|1| |   
|0|0|1|0|0| |  
|0|0|1|0|1| |  
|0|0|1|1|0| |  
|0|0|1|1|1| |  
|0|1|0|0|0| |  
|0|1|0|0|1| |  
|0|1|0|1|0| |  
|0|1|0|1|1| | 
|0|1|1|0|0| |
|0|1|1|0|1| |
|0|1|1|1|0| |
|0|1|1|1|1| |
|1|0|0|0|0| |
|1|0|0|0|1| |
|1|0|0|1|0| |
|1|0|0|1|1| |
|1|0|1|0|0| |
|1|0|1|0|1| |
|1|0|1|1|0| |
|1|0|1|1|1| |
|1|1|0|0|0| |
|1|1|0|0|1| |
|1|1|0|1|0| |
|1|1|0|1|1| |
|1|1|1|0|0| |
|1|1|1|0|1| | 
|1|1|1|1|0| | 
|1|1|1|1|1| |

## Karnaugh

O mapa de karnaugh como anteriormente dito, é uma simplificação visual e simples de encontrar a equação lógica a partir da saìda. <br> A mapa de karnaugh pode ser expandido, a cada variavel ele dobra, primeiro para a direita e depois para baixo, uma cópiia do anterios só que invertido. exemplo:

|A/B|0|1|
|-|-|-|  
|**0**|||
|**1**|||    

|A/BC|0 +"0" = 00|"0" +"1" = 01|+|11|10|
|-|-|-|-|-|-|
|**0**| | | | | |
|**1**| | | | | |

|A/BC|00|01|11|10|
|-|-|-|-|-|
|**0**| | | | |
|**1**| | | | | 

como podemos observar, ao passar de de 2 variaveis para 3, o mapa duplicou para a direita e os numeros inverteram, onde era 0 virou 1 e onde era 1 virou 0 (00 → 11 e 01 → 10). Además disso, foi adicionado a variavel C, para se guiar é só analisar o a posição, como é BC, o primeiro digito é para o B e o segundo para o C. Esses numeros você utiliza para encontrar na tabela verdade e posicionar na casa exata do karnaugh, como se fossem coordenadas, exemplo:

|A|B|C|S|
|-|-|-|-|
|1|0|1|X|

Essa posição diz que o X esta na linha onde A é 1, B é 0 e C é 1, no caso essa:

|A/BC|00|01|11|10|
|-|-|-|-|-|
|**0**| | | | |
|**1**| |X| | |

O próximo caso é de 4x4, depois dele a lógica de expanção se mantem igual

|AB/CD|00|01|11|10|
|-|-|-|-|-|
|**00**||||||
|**01**||||||
|**11**||||||
|**10**||||||

Para o local das variaveis, se nota que o B passou de lado, a lógica disso é simples, as linhas podem ter somente 1 variavel a menos que as colunas, caso o numero de variaveis aumentar para impar, a nova variavel é acresentada ao lado que representa as colunas (em caso de estarem juntas na célula, ela esta a direita da barra), e quando o valor aumentar 1 variavel e virar par, a primenira variavel a direita passa a ser a ultima da esquerda. Exemplo

|(2x4): A/BC| &rarr; |(4x4): AB/CD |
|-|-|-|

como podemos analizar, a variavel D foi acrescentada no final da regigão das colunas (direita da barra) e a variavel B passou para ultima posição da região das linhas (esquerda da barra)

## Formação de grupos

Para formar grupos com karnaugh você deve indentificar um conjunto de linhas, colunas ou grupos quadrados, seus tamanhos permitidos são feitos com valores de 2<sup>X</sup>, como por exemplo 1 elemento (2<sup>0</sup>), 2 elementos (2<sup>1</sup>), 4 elemento (2<sup>2</sup>), 8 elementos (2<sup>3</sup>) e etc.
|1111|
|:-:|    

|1|
|:-:|
|**1**|
|**1**|
|**1**|

|1|1|
|-|-|
|**1**|**1**|

Nos exemplos acima ambos são grupos de quatro elementos.<br>

<br> Dentro dos grupos só podem conter 1 ou X. No caso do X ele pode ser 1 ou 0, você só deve consider como 1 caso ele auxilie na formação de um grupo maiores, exemplo:

|1|1|
|-|-|
|**1**|**X**|

Nesse caso o X auxiliaria em transformar o dois grupos de dois elementos cada em apenas um grupo com quatro elementos, reduzindo o numero de portas do circuito final
