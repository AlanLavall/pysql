# Importando as bibliotecas necessárias
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
