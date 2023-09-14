#Bibliotecas utilizadas
import mysql.connector #Para conexão com o mysql
from mysql.connector import Error #Para mostrar os erros obtidos relacionados com o mysql connector.
from flask import Flask, jsonify #Para criar o micro serviço e a aplicação com os endpoints e jsonify os results para a chamada get
from collections import defaultdict
app = Flask(__name__)

# Try Catch
try:
    # Conectando ao banco de dados por meio do mysql connector
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='howvii',
    )

    # Condição que verifica a conexão com o banco de dados, e se estiver executa o bloco de codigo.
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
        # For para dar um print no resultado pegando o valor de cada campo da query feita no BD e formatando com espaçamentos e limitando as strings
        for row in result:
            linha = row
            VendaID, DataPagamento, ValorPagamento, CodigoImovel, DescricaoImovel, Tipo = linha
            print(
                f'{VendaID:^9} {DataPagamento} {ValorPagamento:>13,.2f} {CodigoImovel:^19} {DescricaoImovel[:50]:^15} {Tipo:^13}')
            print(
                '---------------------------------------------------------------------------------------------------------------------------------------------------------------------')


        cursor = conexao.cursor(dictionary=True)  # Usar 'dictionary=True' para obter resultados como dicionários
        cursor.execute(consulta)
        vendas = cursor.fetchall()


        # Metodo para calcular e retornar a soma dos pagamentos de cada imovel, recebe como parametro a lista das vendas
        def somaPagamentosPorImovel(vendas):
            resultado = {}

            for venda in vendas:
                codigoImovel = venda['CodigoImovel']
                valorPagamento = venda['ValorPagamento']

                if codigoImovel in resultado:
                    resultado[codigoImovel] += valorPagamento
                else:
                    resultado[codigoImovel] = valorPagamento
            return resultado

        # Metodo para calcular e retornar o total de vendas por mês/ano, recebe como parametro a lista das vendas
        def totalVendasPorMesAno(vendas):
            resultado = defaultdict(float)

            for venda in vendas:
                dataPagamento = venda['DataPagamento']
                valorPagamento = venda['ValorPagamento']

                # Converte(cast) o valor de 'Decimal para 'float', pois na tablea foi declado como decimal'
                valorPagamentoFloat = float(valorPagamento)

                # Formata o DataPagamento para "mes/ano"
                dataString = dataPagamento.strftime("%m/%Y")

                resultado[dataString] += valorPagamentoFloat
            return resultado

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

        # Função para formatar e retornar um valor como moeda concatenando a string Total R$ com o valor formatado
        def formatarMoeda(valor):
            return "Total R$ {:,.2f}".format(valor)


        # ENDPOINT para calcular o total de vendas por mês/ano chamando o metodo totalVendasPorMesAno
        @app.route('/totalVendasPorMesAnoEndpoint', methods=['GET'])
        def totalVendasPorMesAnoEndpoint():

            resultado = totalVendasPorMesAno(vendas)

            #Resultado formatado chamando o metodo formatarMoeda
            resultadoFormatado = {chave: formatarMoeda(valor) for chave, valor in resultado.items()}

            return jsonify(resultadoFormatado)


        # ENDPOINT para calcular a soma de pagamentos por imóvel chamando o metodo somaPagamentosPorImovel.
        @app.route('/somaPagamentosPorImovelEndpoint', methods=['GET'])
        def somaPagamentosPorImovelEndpoint():
            resultado = somaPagamentosPorImovel(vendas)
            resultadoFormatado = {chave: formatarMoeda(valor) for chave, valor in resultado.items()}

            return jsonify(resultadoFormatado)

except Error as e:
    print("Erro ao tentar se conectar com MySQL", e)

if __name__ == '__main__':
    app.run(debug=True)