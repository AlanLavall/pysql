# Importando bibliotecas necessárias
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
