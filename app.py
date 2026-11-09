from flask import Flask, render_template, request
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# --- Funciones de Validación ---
def validar_usuario(usuario):
    return re.fullmatch(r"[A-Za-z0-9_]{4,20}", usuario) is not None

def validar_correo(correo):
    return re.fullmatch(r"^[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo) is not None

def validar_password(password):
    return len(password) >= 8

# --- Registro de Auditoría ---
def registrar_evento(tipo, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}, {tipo}, {usuario}\n")

# --- Rutas de la Aplicación ---
@app.route("/")
def inicio():
    return "Laboratorio de Ciberseguridad"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        # Validaciones de formato
        if not validar_usuario(usuario):
            return "Usuario inválido"
        if not validar_correo(correo):
            return "Correo electrónico inválido"
        if not validar_password(password):
            return "La contraseña debe contener al menos 8 caracteres"

        # Conexión a la base de datos
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Comprobar usuarios o correos duplicados
        cursor.execute("SELECT id FROM usuarios WHERE usuario = ? OR correo = ?", (usuario, correo))
        existente = cursor.fetchone()

        if existente:
            conexion.close()
            return "El usuario o correo ya está registrado"

        # Generar hash y guardar de forma parametrizada
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
            (usuario, correo, password_hash)
        )
        conexion.commit()
        conexion.close()
        return "Usuario registrado"

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Consulta parametrizada por usuario
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conexion.close()

        # Verificación del hash de la contraseña y registro en log
        if resultado and check_password_hash(resultado[3], password):
            registrar_evento("LOGIN_CORRECTO", usuario)
            return "Inicio de sesión correcto"
        else:
            registrar_evento("LOGIN_FALLIDO", usuario)
            return "Credenciales incorrectas"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)