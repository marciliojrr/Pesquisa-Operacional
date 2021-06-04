# -*- coding: utf-8 -*-
"""Trabalho_2_PO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cJB0UtQrx6Tr3b4I9zuCxD6EBP65SAw3

##Pesquisa Operacional - Trabalho 2
###Professor: Teobaldo
---
Discentes:
- Marcílio de Oliveira Silva Júnior - Mat: 11413589
- Alan Hiores Freires de Sales Leite - Mat: 11228436
"""

# Importação de bibliotecas necessárias.
import numpy as np

# Abrindo arquivos de instância. Inserção manual do nome de cada arquivo.
arquivo = open('po1.txt', 'r', encoding='utf-8')

# readlines() retorna cada linha do arquivo lido anteriormente e salva em uma lista.
instancias = arquivo.readlines()

# Realizando limpeza e organização dos dados (removendo '\n' e afins e separando cada linha em uma lista).
instancias = [i.split() for i in instancias]

# Exibindo dados brutos da instancia lida.
print(instancias)

# Criando variáveis com a quantidade de variáveis e restrições da instancia lida.
num_vars = int(instancias[0][0])
num_rest = int(instancias[0][1])
print(f'''Número de variáveis: {num_vars}\nTipo da variável "num_vars": {type(num_vars)}\n
Quantidade de restrições: {num_rest}\nTipo da variável "num_vars": {type(num_rest)}
''')

# Criando array com os coeficientes da F.O.
coef_fo = [int(i) for i in instancias[1]]
coef_fo = np.array(coef_fo)
print(f'Coeficientes da FO: {coef_fo}\nTipo da variável "coef_fo": {type(coef_fo)}')

# Criando array com as restrições da instancia lida e o vetor b.
restricoes = instancias[2:]
b = []
for i in range(0, len(restricoes)):
  restricoes[i] = np.array(restricoes[i], int)
  b.append(restricoes[i][-1])
  restricoes[i] = np.delete(restricoes[i], -1)
b = np.array(b)

for i in range(0, len(restricoes)):
  print(f'Coeficientes da restrição {i + 1}: {restricoes[i]}\nTipo da variável: {type(restricoes[i])}\n')
print(f'Vetor b: {b}\nTipo da variável: {type(b)}')

# Construindo a matriz A já considerando a inserção das variáveis de folga.
A = np.array(restricoes)
coef_folga = np.eye(num_rest, dtype=int)
A = np.concatenate((A, coef_folga), axis=1)

print(f'''Matriz A:
{A}

Tipo de A: {type(A)}''')

# A partir das necessidades da função linalg, ajustes precisaram ser feitos 
# de modo que a mesma funcionasse corretamente. Esses ajustes são em relação as
# variáveis NÃO-BÁSICAS e, assim, não comprometendo o problema.
coef_folga_fo = np.zeros((num_rest - num_vars,), dtype=int)
coef_folga_fo

coef_fo_total = np.concatenate((coef_fo, coef_folga_fo), axis=0)
coef_fo_total

b_total = np.concatenate((b, coef_folga_fo), axis=0)
b_total

from math import factorial as factorial
from math import ceil as ceil
vars_total = num_vars + num_rest

qtd_comb = int(factorial(vars_total) / (factorial(num_rest) * factorial(vars_total - num_rest)))
print(f'- Quandidade de combinações para as colunas da matriz: {qtd_comb}\n')

counter = 0
bases_aux = []
#for i in range(num_vars - num_rest + 1):
for i in range(vars_total - num_rest + 1):
  for j in range(i + 1, vars_total):
    for k in range(j + 1, vars_total):

      print(f'- Matriz {counter} - (x{i + 1}, x{j + 1}, x{k + 1})')
      print(A[:, [i, j, k]],)

      det = np.linalg.det(A[:, [i, j, k]])
      if det != 0:
        bases_aux.append(A[:, [i, j, k]])
        print(f'Determinante: {ceil(det)} e, portanto, é L.I.\n')
      else:
        print(f'Determinante: {ceil(det)} e, portanto, é L.D.\n')
      counter += 1

# Esta biblioteca poderia dinamizar as matrizes, sem que fosse preciso alterar
# o código para matrizes de diferentes dimensões. Entretanto, não consegui
# utilizá-lo com meu código.

from itertools import combinations
matrizes = [i for i in range(qtd_comb)]

basis = []

for i in range(num_rest):
  comb = list(combinations(A[i], num_rest))
  print(comb)
  basis.append(comb)
  #for j in comb:
    #basis = np.array(j)
  #basis = np.array([comb])
  #basis[i] = np.array([comb])
  #for j, linha in enumerate(comb):
  #  matrizes.append(linha)

#print('Matrizes: ')
#for i, matriz in enumerate(matrizes):
#  print(f'Matriz #{i + 1}')
#  print(np.array(matriz))

# Uma vez que a função "linprog" só realiza operações de minimização,
# multiplicamos por (-1) os coeficientes da F.O.

coef_fo_total = -coef_fo_total
print(coef_fo_total)

"""Resolvendo para o arquivo de instância com as informações do exemplo passado em aula no dia 26/04 podemos comparar os resultados encontrados em aula e os exibidos pela função linprog. Vale lembrar que essa função, quando não passados os parâmetros sobre quais valores as variáveis podem assumir, ela define que serão sempre positivos (X >= 0).

---


- Exemplo da aula 26/04:

MAX 3X1 + 5X2

X1 <= 4

X2 <= 6

3X1 + 2X2 <= 18

X1, X2 >= 0

- Arquivo de instância:

2 3

3 5

1 0 4

0 1 6

3 2 18

---
- Em aula, utilizando a base:

1 0 1

0 1 0

3 2 0

Encontra-se os valores para X1, X2 e X3: 2, 6, 2 respectivamente.

Os mesmos valores podem ser vistos no retorno da função linalg.
"""

from scipy.optimize import linprog
res = linprog(coef_fo_total, A_ub = bases_aux[0], b_ub = b)
print(res)