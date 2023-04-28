# Importando os módulos necessários
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
