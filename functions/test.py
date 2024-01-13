
# Dados de exemplo
dados = {
    '3MM': 41.18,
    '4MM': 773.9499999999996,
    '5MM': 8.65,
    '6MM': 40.65999999999999,
    '8MM': 51.15999999999999,
    '10MM': 11.390000000000002,
    '3+3': 20.159999999999997,
    '4+4': 43.980000000000004,
    '5+5': 2.9899999999999998
}

# Calculando o total
total = sum(dados.values())

# Calculando a porcentagem de cada chave
porcentagens = {chave: (valor / total) * 100 for chave, valor in dados.items()}

print(porcentagens)
