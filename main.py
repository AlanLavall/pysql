# Importando os módulos necessários
from time import sleep
import os
import clientes
import plantas
import vendas
from funcoes import conn, cursor


# Exibindo o título do programa
print('----------------------BANCO FLORICULTURA--------------------')

# Iniciando o loop principal
try:
    while True:
        os.system('cls')  # Limpando a tela
        print('----------------------MENU PRINCIPAL--------------------')
        print('Menu: \n1 - Acessar Plantas\n2 - Acessar clientes cadastrados\n3 - Vendas\n0 - Sair')

        # Obtendo a escolha do usuário
        escolha = int(input('Escolha a opção: '))

        # Redirecionando para as funções correspondentes conforme a escolha do usuário
        if escolha == 1:
            plantas.plant()
        elif escolha == 2:
            clientes.client()
        elif escolha == 3:
            vendas.vendas()
        elif escolha == 0:
            break
        else:
            sleep(1)  # Esperando por um segundo
            print('\nOpção Inválida!\n')
            sleep(1)  # Esperando por mais um segundo

# Finalizando a conexão com o banco de dados
finally:
    cursor.close()
    conn.close()
