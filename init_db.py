
import sqlite3

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    senha TEXT
)
""")
cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', '123')")

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    especialidade TEXT,
    dias TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    nascimento TEXT,
    responsavel TEXT,
    telefone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER,
    medico_id INTEGER,
    data TEXT,
    hora TEXT,
    pagamento TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
print("Banco de dados inicializado.")
