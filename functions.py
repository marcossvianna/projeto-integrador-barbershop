from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import bcrypt
import smtplib
from connection import create_connection
import random

from app import index

app = Flask(__name__, template_folder='templates')


def validaSessao():
    if session['email'] is None:
        return render_template('index.html', message_login="Voce precisa está logado para acessar o sitema",
                               item=index(), focus="login")


def agendamento():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        servico = request.form['servico']
        data = request.form['data']
        hora = request.form['time']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO agendamento (nome, email, telefone, servico, data, hora) VALUES (?, ?, ?, ?, ?, ?)',
                       (nome, email, telefone, servico, data, hora))
        conn.commit()
        conn.close()
        return render_template("menu.html")
    return render_template("menu.html")

def cadastro():
    if request.method == 'POST':
        session = None
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM usuarios WHERE email=?', [email])
        message_login = ""
        if len(cursor.fetchall()) == 0:
            cursor.execute('INSERT INTO usuarios (nome, email, telefone, senha, status) VALUES (?, ?, ?, ?, ?)',
                           (nome, email, telefone, hashed_password.decode('utf-8'), 'user'))
        else:
            message_login = "Usuario já cadastrado"
        conn.commit()
        conn.close()
        return render_template('index.html', item=index(), message_login=message_login, focus='login')
    return render_template('index.html', item=index())


def login_users():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user:
            hashed_password = user[4]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                if user[5] == "adm":
                    conn.close()
                    session['email'] = email
                    return render_template('menu_adm.html')
                conn.close()
                session['email'] = email
                return render_template('menu.html')
            else:
                conn.close()
                return render_template('index.html', message_login="Senha incorreta", item=index(), focus="login")
        else:
            conn.close()
            return render_template('index.html', message_login="Usuário não cadastrado", item=index(), focus="login")
    return render_template('index.html', item=index())


def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT email FROM usuarios WHERE email=?', [email])
        if len(cursor.fetchall()) != 0:
            escolhas_possiveis = 'ABC123'
            senha = ''
            for i in range(8):
                senha += random.choice(escolhas_possiveis)
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('UPDATE usuarios SET senha=? WHERE email=?',
                           (hashed_password.decode('utf-8'), email))
            body = 'Subject: Recuperar senha - Barbershop \n\n\n' + 'Olá senhor(a), segue sua senha provisoria, para o acesso de login no Barbershop: ' + senha
            try:
                smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
            except Exception as e:
                print(e)
                smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login('email@outlook.com.br', "senha")
            smtpObj.sendmail('email@outlook.com.br', email, body.encode('utf-8'))
        conn.commit()
        conn.close()

        return render_template('index.html',
                               alert='Uma nova senha foi enviada para o seu email, verifique sua caixa de spam',
                               focus='login', item=index())
    return render_template('index.html', item=index())


def cadastro_servicos_precos():
    if request.method == 'POST':
        servico = request.form['servico']
        preco = request.form['preco']
        preco = "R$ %.2f" % float(preco)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT produto FROM produtos WHERE produto=?', [servico])
        if len(cursor.fetchall()) != 0:
            cursor.execute('UPDATE produtos SET produto=?, preco=? WHERE produto=?',
                           (servico, preco, servico))
        else:
            cursor.execute('INSERT INTO produtos (produto, preco) VALUES (?, ?)',
                           (servico, preco))
        conn.commit()
        conn.close()
        return redirect(url_for('cadastro_servicos_precos'))
    return render_template("cadastro_servicos_precos.html")


def get_agendamento():
    if request.method == 'GET':
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM agendamento')
        rows = cursor.fetchall()
        conn.close()

        # Transforma os resultados em uma lista de dicionários
        data = []
        for row in rows:
            agendamento = {
                'id': row[0],
                'nome': row[1],
                'email': row[2],
                'telefone': row[3],
                'servico': row[4],
                'data': row[5]
            }
            data.append(agendamento)

        # Retorna os dados como JSON
    return jsonify(data)
