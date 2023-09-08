import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify
from collections import defaultdict
app = Flask(__name__)

try:
    # Conectando ao banco de dados
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='howvii',
    )
    if conexao.is_connected():
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
        cursor2 = conexao.cursor()
        cursor2.execute(consulta)
        result = cursor2.fetchall()

        print("Estamos conectado com MySQL: \n")

        print('VendaID  DataPagamento  ValorPagamento CodigoImovel                        DescricaoImovel    '
              '                Tipo')
        print(
            '---------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        for row in result:
            linha = row
            VendaID, DataPagamento, ValorPagamento, CodigoImovel, DescricaoImovel, Tipo = linha
            print(
                f'{VendaID:^9} {DataPagamento} {ValorPagamento:>13,.2f} {CodigoImovel:^19} {DescricaoImovel[:50]:^15} {Tipo:^13}')
            print(
                '---------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            # print(row)

        cursor = conexao.cursor(dictionary=True)  # Usar 'dictionary=True' para obter resultados como dicionários
        cursor.execute(consulta)
        vendas = cursor.fetchall()

        # ENDPOINT para calcular a soma de pagamentos por imóvel
        @app.route('/somaPagamentosPorImovel', methods=['GET'])
        def somaPagamentosPorImovel():
            resultado = {}
            for venda in vendas:
                codigoImovel = venda['CodigoImovel']
                valorPagamento = venda['ValorPagamento']
                valorPagamentoFormatado = f"R$ {valorPagamento}"
                if codigoImovel in resultado:
                    resultado[codigoImovel] += valorPagamentoFormatado
                else:
                    resultado[codigoImovel] = valorPagamentoFormatado
            return jsonify(resultado)



        # ENDPOINT para calcular o total de vendas por mês/ano
        @app.route('/totalVendasPorMesAno', methods=['GET'])
        def totalVendasPorMesAno():

            resultado = defaultdict(float)
            for venda in vendas:
                dataPagamento = venda['DataPagamento']
                valorPagamento = venda['ValorPagamento']
                dataString = str(dataPagamento)

                if dataPagamento in resultado:
                    resultado[dataString] += f"R$ {valorPagamento}"
                else:
                    resultado[dataString] = f"R$ {valorPagamento}"

            return jsonify(resultado)

        # ENDPOINT para calcular o valor percentual por tipo de imóvel
        @app.route('/valorPercentualPorTipoImovel', methods=['GET'])
        def valorPercentualPorTipoImovel():
            totalVendas = sum(venda['ValorPagamento'] for venda in vendas)
            resultado = {}
            for venda in vendas:
                tipoImovel = venda['Tipo']
                valorPagamento = venda['ValorPagamento']

                if tipoImovel in resultado:
                    resultado[tipoImovel] += valorPagamento
                else:
                    resultado[tipoImovel] = valorPagamento
            for tipo, valor in resultado.items():
                resultado[tipo] = f"Venda: {(valor / totalVendas) * 100:.2f}%"
            return jsonify(resultado)


except Error as e:
    print("Erro ao tentar se conectar com MySQL", e)

if __name__ == '__main__':
    app.run(debug=True)