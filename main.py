import mysql.connector
import olp as olp
from mysql.connector import Error

try:
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='howvii',
                    )
    if conexao.is_connected():
        db_Info = conexao.get_server_info()
        print("Conectado com MySQL Server versão ", db_Info )
        consulta = """
                            SELECT
                                    p.VendaID,
                                    p.DataPagamento,
                                    p.ValorPagamento,
                                    i.CodigoImovel,
                                    i.DescricaoImovel,
                                    ti.Tipo
                            FROM Pagamento p
                            JOIN Imovel i ON p.CodigoImovel = i.CodigoImovel
                            JOIN TipoImovel ti ON i.TipoID = ti.TipoImovelID ;
                        """
        cursor = conexao.cursor()
        cursor.execute(consulta)
        result = cursor.fetchall()
        print("Estamos conectado com MySQL: \n")

        print('VendaID  DataPagamento  ValorPagamento CodigoImovel                        DescricaoImovel    '
              '                Tipo')
        print(
            '---------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        for row in result:
            linha = row
            VendaID,DataPagamento,ValorPagamento,CodigoImovel,DescricaoImovel,Tipo = linha
            print(f'{VendaID:^9} {DataPagamento} {ValorPagamento:>13,.2f} {CodigoImovel:^19} {DescricaoImovel[:50]:^15} {Tipo:^13}')
            print('---------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            #print(row)

    conexao.close()

except Error as e:
    print("Erro ao tentar se conectar com MySQL", e)


    ##para fazer inserts pelo codigo.

    #     # Create a new record
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    #
    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # conexao.commit()

