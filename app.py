import os
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/principal", methods=["GET", "POST"])
def principal():
    return render_template("principal.html")


@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    return render_template("categorias.html")


@app.route("/emprendimiento", methods=["GET", "POST"])
def trending():
    return render_template("emprendimiento.html")

@app.route("/carrito", methods=["GET", "POST"])
@login_required
def carrito():
    """Carrito"""
    if request.method == "POST":
        session["carrito"] = []
        id = request.form.get("id_persona")
        session["carrito"].append(id)
        return redirect("/carrito")
    

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    """Registro del usuario"""
    if request.method == "GET":
        return render_template("registrarse.html")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    usuario = request.form.get("usuario")
    contraseña = request.form.get("contraseña")
    confirmacion = request.form.get("confirmacion")
    celular = request.form.get("celular")
    direccion = request.form.get("direccion")
    departamento = request.form.get("departamento")
    usuario = request.form.get("usuario")
    if not nombre:
        print("Paso por Aca 1")
        return redirect("/registrarse")
    if not apellido:
        print("Paso por Aca 2")
        return redirect("/registrarse")
    if not contraseña:
        print("Paso por Aca 3")
        return redirect("/registrarse")
    if not confirmacion:
        print("Paso por Aca 4")
        return redirect("/registrarse")
    if not direccion:
        print("Paso por Aca 5")
        return redirect("/registrarse")
    if not departamento:
        print("Paso por Aca 6")
        return redirect("/registrarse")
    if celular:
        print("Paso por Aca 7")
        return redirect("/registrarse")
    if contraseña != confirmacion:
        print("Paso por Aca 8")
        return redirect("/registrarse")
    try:
        query = text("INSERT INTO persona(nombre_persona, apellido_persona, usuario, direccion, celular, contraseña, roles) VALUES (:nombre, :apellido, :usuario :direccion, :celular, :contraseña, :roles)")
        db.execute(query, {"nombre_persona":nombre, "apellido_persona": apellido, "usuario": usuario, "contraseña": contraseña, "direccion": direccion, "celular": celular, "roles": 0})
        db.commit()
        print("Paso por Aca commit")
    except:
        return redirect("/registrarse")
    return redirect("/registrarse")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
        # User reached route via POST (as by submitting a form via POST)

    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    contraseña = request.form.get("contraseña")
            
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("nombre"):
            return redirect("/login")
         # Ensure last name was submitted
        elif not request.form.get("apellido"):
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("contraseña"):
            return redirect("/login")

            # Query database for username
        rows = text("SELECT * FROM persona WHERE nombre_persona = :nombre)")
        db.execute(rows, {"nombre":nombre, "apellido": apellido,"contra": contraseña})
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["contra"], request.form.get("contraseña")):
            return redirect("/login")

        # Remember which user has logged in
        session["id_persona"] = rows[0]["id_persona"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")