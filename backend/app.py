from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)
@app.route('/calcular', methods=['POST'])
def func():
    # Nota: Recorri ao Gemini para ajustar a forma de capturar o IP.
    # --- Código antigo ---
    # ip_usuario = request.remote_addr
    # ---------------------
    # Problema: Na nuvem (Railway), a API fica atrás de um "proxy".
    # O 'remote_addr' estava pegando o IP rotativo desse proxy, o que fazia o histórico falhar ou sumir ao recarregar a página.
    # Solução: Usar o cabeçalho 'X-Forwarded-For', que é onde o proxy repassa o IP real original do usuário.
    ip_usuario = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    dados = request.get_json()

    valorCompra = dados['valor_compra']
    descontoCupom = dados['desconto_cupom']
    eVip = dados['e_vip']
    tipo_cliente = "VIP" if eVip else "Padrão"
    cashbackBase = 0.05
    valorTotal= valorCompra - (valorCompra*(descontoCupom/100))
    cashback = valorTotal*cashbackBase
    # Usei o multiplicador fatorPromocao afim de evitar o uso de mais if's tornando o codigo mais otimizafdo
    fatorPromocao = 1
    if valorTotal > 500:
        fatorPromocao = 2
    if eVip == True:
        
        cashbackVip = (cashback+cashback*0.10)
        #print (cashbackVip * fatorPromocao)
        valorCashback = cashbackVip * fatorPromocao
    else:
        #print (cashback * fatorPromocao)
        valorCashback = cashback * fatorPromocao
    salvaBD(ip_usuario,valorCompra, valorCashback, tipo_cliente, )
    return jsonify({"cashback": valorCashback})
def salvaBD (ip, valorCompra, valorCashback, tipo_cliente):
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Usamos %s como marcadores de posição
    comando_insert = """
    INSERT INTO historico_consultas (ip_usuario, tipo_cliente, valor_compra, cashback_gerado)
    VALUES (%s, %s, %s, %s);
    """
    
    try:
        conexao = psycopg2.connect(DATABASE_URL)
        cursor = conexao.cursor()
        
        # Os valores entram aqui, em uma tupla, na mesma ordem dos %s
        cursor.execute(comando_insert, (ip, tipo_cliente, valorCompra, valorCashback))
        
        conexao.commit()
        print("Salvo no banco com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()

@app.route('/historico', methods=['GET'])
def obter_historico():
    ip_usuario = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    DATABASE_URL = os.environ.get('DATABASE_URL')
    try:
        conexao = psycopg2.connect(DATABASE_URL)
        cursor = conexao.cursor()
        
        comando_select = "SELECT tipo_cliente, valor_compra, cashback_gerado FROM historico_consultas WHERE ip_usuario = %s"
        cursor.execute(comando_select, (ip_usuario,))
        
        linhas = cursor.fetchall()
        
        historico_formatado = []
        for item in linhas:
            historico_formatado.append({
                "tipo_cliente": item[0],
                "valor_compra": float(item[1]), # convertemos para float para o JSON aceitar
                "cashback_gerado": float(item[2])
            })
            
        return jsonify(historico_formatado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
