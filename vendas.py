# Importando os módulos necessários
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
