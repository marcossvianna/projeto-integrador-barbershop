from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import functions
from connection import create_connection

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'barbershop@123'

@app.route('/')
def index():
    session['email'] = None
    conn = create_connection()
    cursor = conn.cursor()
    preco = cursor.execute('SELECT preco FROM produtos').fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', item=preco)

@app.route('/menu_adm')
def menu_adm():
    login = functions.validaSessao()
    return login

@app.route('/menu')
def menu():
    login = functions.validaSessao()
    return login

@app.route('/agendamento', methods=['POST'])
def agendamento():
    return functions.agendamento()
'''
@app.route('/consulta_agendamento', methods=['GET'])
def consulta_agendamento():
    return functions.get_agendamento()
'''
@app.route('/consulta_agenda', methods=['GET'])
def consulta_agendamento():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone, servico, data, hora FROM agendamento')
    agendamentos = cursor.fetchall()
    conn.close()

    # Convertemos os dados para um formato serializável em JSON
    agendamento_list = []
    for agendamento in agendamentos:
        agendamento_list.append({
            'id': agendamento[0],
            'nome': agendamento[1],
            'email': agendamento[2],
            'telefone': agendamento[3],
            'servico': agendamento[4],
            'data': agendamento[5],
            'hora': agendamento[6]
        })
    return jsonify(agendamento_list)

# consulta agendamento administrador
@app.route('/consulta_agendamento')
def consulta_agenda():
    return render_template('consulta_agendamento.html')

@app.route('/delete_agendamento/<int:id>', methods=['POST'])
def delete_agendamento(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM agendamento WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/update_agendamento/<int:id>', methods=['POST'])
def update_agendamento(id):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    servico = data.get('servico')
    data_agendamento = data.get('data')
    hora = data.get('hora')

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE agendamento SET nome = ?, email = ?, telefone = ?, servico = ?, data = ?, hora = ? WHERE id = ?',
        (nome, email, telefone, servico, data_agendamento, hora, id))
    conn.commit()
    conn.close()
    return jsonify(success=True)
##########

@app.route('/consulta_usuario', methods=['GET'])
def consulta_usuario():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM usuarios where email = ?', (session['email'],))
    usuarios = cursor.fetchall()
    conn.close()

    # Convertemos os dados para um formato serializável em JSON
    usuario_list = []
    for usuario in usuarios:
        usuario_list.append({
            'id': usuario[0],
            'nome': usuario[1],
            'email': usuario[2],
            'telefone': usuario[3]
        })
    return jsonify(usuario_list)

# consulta agendamento administrador
@app.route('/editar_perfil')
def editar_perfil():
    return render_template('editar_perfil.html')

@app.route('/delete_usuario/<int:id>', methods=['POST'])
def delete_usuario(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/update_usuario/<int:id>', methods=['POST'])
def update_usuario(id):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE usuarios SET nome = ?, email = ?, telefone = ? WHERE id = ?',
        (nome, email, telefone, id))
    conn.commit()
    conn.close()
    return jsonify(success=True)

##########

@app.route('/cadastro_servicos_precos', methods=['POST'])
def cadastro_servicos_precos():
    return functions.cadastro_servicos_precos()

@app.route('/login', methods=['POST'])
def login():
    return functions.login_users()

@app.route('/reset_pwd', methods=['POST'])
def reset_pwd():
    return functions.recuperar_senha()

@app.route('/cadastro', methods=['POST'])
def cadastro():
    return functions.cadastro()

@app.route('/consulta_agenda')
def consulta():
    return render_template('consulta_agendamento.html')

if __name__ == '__main__':
    app.run(debug=True)