from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Função que conecta no banco e retorna os dados
def buscar_clientes():
    conexao = psycopg2.connect(
        host="postgres",
        port="5432",
        database="Luca",
        user="lucauser",
        password="lucasenha"
    )
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email FROM clientes")
    rows = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Converter os resultados em dicionários
    clientes = []
    for row in rows:
        clientes.append({
            "id": row[0],
            "nome": row[1],
            "email": row[2]
        })
    return clientes

# Rota /clientes
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    clientes = buscar_clientes()
    return jsonify(clientes)

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)