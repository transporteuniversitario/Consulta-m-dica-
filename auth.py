import sqlite3

def verificar_login(usuario, senha):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0]  # tipo do usuário (admin, secretaria, medico)
    return None

def criar_usuario(usuario, senha, tipo="secretaria"):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)", (usuario, senha, tipo))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def buscar_usuarios():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, tipo FROM usuarios ORDER BY usuario")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def excluir_usuario(user_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
