import sqlite3

def criar_tabelas():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL DEFAULT 'secretaria'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT,
            dias_atendimento TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            pago TEXT,
            forma_pagamento TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            medico_id INTEGER,
            especialidade TEXT,
            data TEXT,
            hora TEXT,
            valor REAL,
            pago TEXT,
            forma_pagamento TEXT,
            status TEXT,
            presenca TEXT DEFAULT 'Não',
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (medico_id) REFERENCES medicos(id)
        )
    """)

    conn.commit()
    conn.close()
