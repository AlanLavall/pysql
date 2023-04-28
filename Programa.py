Módulo Principal:
""" # Importando os módulos necessários
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
 """
Módulo com as funções:
""" # Importando os módulos necessários
import sys
import psycopg2

conn = psycopg2.connect(    # Cria uma conexão com o banco de dados 'floricultura'
    host='localhost',
    database='floricultura',
    user='postgres',
    password='7868'
)

cursor = conn.cursor()     # Cria um cursor para executar as consultas SQL no banco de dados


# Função que verifica se a quantidade de plantas escolhida está disponível em estoque
def verifica_estoque(id_planta, quant_planta, id_venda):
    cursor.execute("SELECT quant FROM plantas WHERE id = %s", (id_planta,))
    resultado = cursor.fetchone()[0]
    if quant_planta > resultado:
        print('Quantidade em estoque insuficiente!')
        cursor.execute('DELETE FROM vendas_plantas WHERE id_venda = %s', (id_venda,))
        conn.commit()
        cursor.execute('DELETE FROM vendas WHERE id = %s', (id_venda,))
        conn.commit()
        input()
        sys.exit()        # Encerra o programa caso não haja quantidade suficiente em estoque


# Função que calcula o preço total da planta escolhida a partir da quantidade selecionada
def calcula_total_unitario(id_planta, quant_planta):
    cursor.execute("SELECT preco FROM plantas WHERE id = %s", (id_planta,))
    preco_planta = cursor.fetchone()[0]
    preco_total = quant_planta * preco_planta
    return preco_total


# Função que atualiza a quantidade de plantas em estoque após uma venda
def atualiza_estoque_venda(id_planta, quant_planta):
    cursor.execute("UPDATE plantas SET quant = quant - %s"
                   " WHERE id = %s", (quant_planta, id_planta))
    conn.commit()
 """
Módulo plantas:
""" # Importando as bibliotecas necessárias
from time import sleep
from os import system
from funcoes import cursor, conn
from prettytable import PrettyTable


# Define uma função para lidar com plantas
def plant():
    # Define as colunas que aparecerão na tabela
    colunas = ['ID', 'NOME', 'ESTOQUE', 'PREÇO']
    while True:
        # Limpa a tela
        system('cls')
        # Imprime o menu
        print('----------------------MENU PLANTAS--------------------')
        print('1 - Conferir plantas em estoque\n2 - Adicionar plantas\n3 - Editar tabela\n4 - Excluir planta'
              '\n0 - Voltar')

        # Lê a escolha do usuário
        escolha = int(input('Escolha a opção: '))
        # Limpa a tela
        system('cls')

        # Se o usuário escolheu 1, mostra as plantas em estoque
        if escolha == 1:
            # Executa a consulta SQL para obter todas as plantas ordenadas pelo ID
            cursor.execute("SELECT * FROM plantas order by id")
            # Obtém todos os resultados da consulta
            resultados = cursor.fetchall()
            # Cria uma tabela bonita usando PrettyTable e adiciona cada registro à tabela
            tabela = PrettyTable(colunas)
            for registro in resultados:
                tabela.add_row(registro)
            # Imprime a tabela
            print(tabela)
            # Aguarda até que o usuário pressione ENTER
            input('Pressione ENTER para continuar')

        # Se o usuário escolheu 2, adiciona uma nova planta ao estoque
        elif escolha == 2:
            # Lê o nome, quantidade e preço da nova planta
            _nome = input('Nome da Planta: ')
            _quant = int(input('Quantidade: '))
            _preco = float(input('Preço: '))

            # Insere a nova planta na tabela de plantas
            cursor.execute('INSERT INTO plantas (nome, quant, preco) VALUES (%s, %s, %s)', (_nome, _quant, _preco))
            # Confirma a transação
            conn.commit()
            # Limpa a tela
            system('cls')
            # Imprime uma mensagem de sucesso
            print('Adicionado!')
            # Aguarda até que o usuário pressione ENTER
            input('Pressione ENTER para continuar')
        # Se o usuário escolheu 3, permite a edição dos dados de uma planta específica
        elif escolha == 3:
            while True:
                _idEdit = int(input('Qual o ID da planta que você deseja alterar: '))
                atributo = int(input('Qual atributo você deseja alterar:\n1 - Nome\n2 - Quantidade em estoque\n'
                                     '3 - Preço\n0 - Voltar\nEscolha: '))

                # Se o usuário escolher o atributo 1, permite a edição do nome da planta
                if atributo == 1:
                    novo_nome = input('Insira o novo nome da planta: ')
                    cursor.execute('UPDATE plantas SET nome = %s WHERE id = %s', (novo_nome, _idEdit))
                    conn.commit()
                    print('Nome alterado')

                # Se o usuário escolher o atributo 2, permite a edição da quantidade em estoque da planta
                elif atributo == 2:
                    nova_quant = int(input('Insira o nova quantidade em estoque: '))
                    cursor.execute('UPDATE plantas SET quant = %s WHERE id = %s', (nova_quant, _idEdit))
                    conn.commit()
                    print('Quantidade alterada')

                # Se o usuário escolher o atributo 3, permite a edição do preço da planta
                elif atributo == 3:
                    novo_preco = float(input('Insira o novo nome da planta: '))
                    cursor.execute('UPDATE plantas SET preço = %s WHERE id = %s', (novo_preco, _idEdit))
                    conn.commit()
                    print('Preço alterado')

                # Se o usuário escolher 0, volta ao menu principal
                elif atributo == 0:
                    break

                # Se o usuário escolher um número que não corresponde a uma opção, exibe uma mensagem de erro
                else:
                    print('Opção Invalida')

        # Se o usuário escolheu 4, permite a exclusão de uma planta do estoque
        elif escolha == 4:
            id_delete = int(input('Qual o ID da planta que deseja excluir: '))
            cursor.execute("SELECT * FROM plantas WHERE id = %s", (id_delete,))
            resultados = cursor.fetchall()
            print('Tem certeza que deseja excluir os seguintes dados:')
            tabela = PrettyTable(colunas)
            for registro in resultados:
                tabela.add_row(registro)
            print('Tem certeza que deseja excluir os seguintes dados:')
            print(tabela)
            escolha = input('S ou N: ')

            # Se o usuário confirmar a exclusão, exclui a planta do estoque
            if escolha == 'S' or 's':
                cursor.execute('DELETE FROM plantas WHERE ID = %s', (id_delete,))
                conn.commit()
                system('cls')
                print('Deletado com Sucesso!')
                input('Pressione ENTER para continuar')

            # Se o usuário cancelar a exclusão, volta ao menu principal
            elif escolha == 'n' or 'N':
                break

            # Se o usuário digitar uma opção inválida, exibe uma mensagem de erro
            else:
                sleep(1)
                print('\nOpção Inválida!\n')
                sleep(2)

        # Se o usuário escolher 0 volta ao menu principal
        elif escolha == 0:
            break
        # Se o usuário digitar uma opção inválida, exibe uma mensagem de erro
        else:
            sleep(1)
            print('\nOpção Inválida!\n')
            sleep(2)
 """
Módulo clientes:
""" # Importando bibliotecas necessárias
from time import sleep
from os import system
from funcoes import cursor, conn
from prettytable import PrettyTable


# Definindo a função client
def client():
    # Definindo as colunas que serão exibidas na tabela
    colunas = ['ID', 'NOME', 'TELEFONE']

    while True:
        # Limpando a tela
        system('cls')
        sleep(0.5)

        # Imprimindo o menu
        print('----------------------MENU CLIENTES--------------------')
        print('1 - Conferir Cadastro de clientes\n2 - Cadastrar Clientes\n3 - Editar dados\n4 - Excluir cliente'
              '\n0 - Voltar')

        # Obtendo a escolha do usuário
        escolha = int(input('Escolha a opção: '))
        system('cls')

        # Verificando a escolha do usuário
        if escolha == 1:
            # Exibindo todos os clientes cadastrados ordenado pelo ID
            cursor.execute("SELECT * FROM clientes order by id")
            resultados = cursor.fetchall()
            tabela = PrettyTable(colunas)
            for registro in resultados:
                tabela.add_row(registro)
            print(tabela)
            input('Pressione ENTER para continuar')

        elif escolha == 2:
            # Cadastrando novo cliente
            _nome = input('Nome do cliente: ')
            _tel = input('Telefone: ')
            cursor.execute('INSERT INTO clientes (nome, telefone) VALUES (%s, %s)', (_nome, _tel))
            conn.commit()
            system('cls')
            print('Cadastro realizado!')
            input('Pressione ENTER para continuar')

        elif escolha == 3:
            # Editando dados do cliente
            while True:
                _idEdit = int(input('Qual o ID do cliente que você deseja alterar: '))
                atributo = int(input('Qual dado você deseja alterar:\n1 - Nome\n2 - Telefone\n0 - Voltar\nEscolha: '))
                if atributo == 1:
                    # Alterando o nome do cliente
                    novo_nome = input('Insira o novo nome: ')
                    cursor.execute('UPDATE clientes SET nome = %s WHERE id = %s', (novo_nome, _idEdit))
                    conn.commit()
                    system('cls')
                    print('Nome alterado!')
                    input('Pressione ENTER para continuar')
                    break
                elif atributo == 2:
                    # Alterando o telefone do cliente
                    novo_tel = int(input('Insira o nova número de telefone: '))
                    cursor.execute('UPDATE clientes SET telefone = %s WHERE id = %s', (novo_tel, _idEdit))
                    conn.commit()
                    system('cls')
                    print('Número de telefone alterado!')
                    input('Pressione ENTER para continuar')
                    break
                elif atributo == 0:
                    break
                else:
                    print('Opção Invalida')

        # Excluir os dados de um cliente
        elif escolha == 4:
            # Pede pro usuário inserir o ID do cliente
            id_delete = int(input('Qual o ID do cliente que você deseja excluir: '))
            cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_delete,))
            resultados = cursor.fetchall()
            tabela = PrettyTable(colunas)
            for registro in resultados:
                tabela.add_row(registro)
            # Mostra os dados do cliente e pede a confirmação da exclusão
            print('Tem certeza que deseja excluir os seguintes dados:')
            print(tabela)
            escolha = input('S ou N: ')
            # Se a escolha for 'Sim' deleta os dados do sistema
            if escolha.lower() == 's':
                cursor.execute('DELETE FROM clientes WHERE ID = %s', (id_delete,))
                conn.commit()
                system('cls')
                print('Deletado com Sucesso!')
                input('Pressione ENTER para continuar')
            elif escolha.lower() == 'n':
                break
            else:
                sleep(1)
                print('\nOpção Inválida!\n')
                sleep(2)

        elif escolha == 0:
            break
        else:
            sleep(1)
            print('\nOpção Inválida!\n')
            sleep(2)
 """
Módulo vendas:
""" # Importando os módulos necessários
from time import sleep
from os import system
from funcoes import cursor, conn, atualiza_estoque_venda, verifica_estoque, calcula_total_unitario
from prettytable import PrettyTable


def vendas():
    while True:
        # Exibe o menu de vendas
        system('cls')
        colunasvendas = ['ID', 'ID DO CLIENTE', 'DATA', 'TOTAL']
        colunasvendaplantas = ['ID DA VENDA', 'ID DA PLANTA', 'QUANTIDADE', 'TOTAL POR PLANTA']
        system('cls')
        sleep(0.5)
        print('----------------------MENU VENDAS--------------------')
        # Pede para o usuário inserir a opção desejada
        print('1 - Pesquisar vendas realizadas\n2 - Cadastrar vendas\n3 - Excluir venda\n0 - Voltar')
        escolha = int(input('Escolha a opção: '))
        system('cls')
        # Se a escolha for 1 irá exibir opções de pesquisa na tabela vendas
        if escolha == 1:
            while True:
                system('cls')
                print('1 - Pesquisar todas vendas\n2 - Pesquisar detalhes de uma venda\n0 - Voltar')
                escolha = int(input('Escolha a opção: '))
                system('cls')
                # Se a escolha for 1 irá exibir todas as vendas ordenadas pela data
                if escolha == 1:
                    cursor.execute("SELECT * FROM vendas order by data")
                    resultados = cursor.fetchall()
                    tabela = PrettyTable(colunasvendas)
                    for registro in resultados:
                        tabela.add_row(registro)
                    print(tabela)
                    input('Pressione ENTER para continuar')
                # Se a escolha for 2 exibe os detalhes de uma venda escolhida pelo ID
                elif escolha == 2:
                    id_venda = int(input('Insira o ID da venda: '))
                    cursor.execute('SELECT * FROM vendas_plantas WHERE id_venda = %s', (id_venda,))
                    resultados = cursor.fetchall()
                    tabela = PrettyTable(colunasvendaplantas)
                    for registro in resultados:
                        tabela.add_row(registro)
                    print(tabela)
                    input('Pressione ENTER para continuar')
                elif escolha == 0:
                    break
                else:
                    sleep(1)
                    print('\nOpção Inválida!\n')
                    sleep(1)
        # Opção para cadastrar uma venda
        elif escolha == 2:
            valor_total = 0  # Define o valor total como 0 para depois ir somando
            # pede os dados para cadastro da venda
            cliente_id = int(input('Insira o ID do cliente: '))
            quant_plantas = int(input('Quantidade de plantas: '))
            data = input('Data: ')
            # insere na tabela vendas os dados e retorna o id gerado
            cursor.execute('INSERT INTO vendas (id_cliente, data)'
                           'VALUES (%s, %s)'
                           'RETURNING id',
                           (cliente_id, data))
            conn.commit()
            id_venda = cursor.fetchone()[0]
            # laço para cadastro da(s) planta(s) vendida(s)
            for i in range(quant_plantas):
                id_planta = int(input('Id da planta: '))
                quant_planta = int(input('Quantidade da planta: '))
                verifica_estoque(id_planta, quant_planta, id_venda)  # verifica se a quantidade inserida esta
                # disponível em estoque, se não estiver irá cancelar toda a venda e apagar os dados já inseridos
                total_unitario = calcula_total_unitario(id_planta, quant_planta)  # calcula o valor unitário
                # insere os dados na tabela vendas_plantas
                cursor.execute('INSERT INTO vendas_plantas (id_venda, id_planta, quantidade, total_unitario)'
                               'VALUES (%s, %s, %s, %s); ', (id_venda, id_planta, quant_planta, total_unitario))
                conn.commit()
                atualiza_estoque_venda(id_planta, quant_planta)  # atualiza o estoque
                valor_total += total_unitario  # calcula o valor total
            # insere o valor total na tabela vendas
            cursor.execute('UPDATE vendas SET valor_total = %s WHERE id = %s', (valor_total, id_venda))
            conn.commit()
            print('Venda cadastrada!')
            input('Pressione ENTER para continuar!')
        # Opção para excluir uma venda
        elif escolha == 3:
            id_venda = int(input('Insira o ID da venda que deseja excluir: '))  # pede o id para exclusão
            cursor.execute('SELECT * FROM vendas WHERE id = %s', (id_venda,))
            resultados = cursor.fetchall()
            tabela = PrettyTable(colunasvendas)
            for registro in resultados:
                tabela.add_row(registro)
            print('Tem certeza que deseja excluir os seguintes dados:')
            print(tabela)
            escolha = input('S ou N: ')  # mostra os dados da venda e pede confirmação
            if escolha.lower() == 's':
                cursor.execute('DELETE FROM vendas_plantas WHERE id_venda = %s', (id_venda,))
                conn.commit()  # primeiro deleta da tabela vendas_plantas
                cursor.execute('DELETE FROM vendas WHERE id = %s', (id_venda,))
                conn.commit()  # Agora deleta da tabela vendas
                system('cls')
                print('Deletado com Sucesso!')
                input('Pressione ENTER para continuar')
            elif escolha.lower() == 'n':
                break
            else:
                sleep(1)
                print('\nOpção Inválida!\n')
                sleep(2)
        elif escolha == 0:
            break
        else:
            sleep(1)
            print('\nOpção Inválida!\n')
            sleep(1)
 """
