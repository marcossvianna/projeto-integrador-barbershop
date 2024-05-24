import sqlite3

conn = sqlite3.connect('barbershop.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                  id INTEGER PRIMARY KEY,
                  nome TEXT NOT NULL,
                  email TEXT NOT NULL,
                  telefone TEXT NOT NULL,
                  senha TEXT NOT NULL,
                  status TEXT NOT NULL
              )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                  id INTEGER PRIMARY KEY,
                  produto TEXT NOT NULL,
                  preco TEXT NOT NULL
              )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS agendamento (
                  id INTEGER PRIMARY KEY,
                  nome TEXT NOT NULL,
                  email TEXT NOT NULL,
                  telefone TEXT NOT NULL,
                  servico TEXT NOT NULL,
                  data TEXT NOT NULL                
              )''')

conn.commit()
conn.close()


def create_connection():
    conn = sqlite3.connect('barbershop.db')
    return conn
