import os
from flask import Flask, flash, redirect, render_template, request, session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import psycopg2
from psycopg2 import OperationalError

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
@login_required
def index():
    flash('Este es el index', 'alert-success')
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
    if request.method == "POST":
        
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        usuario = request.form.get("usuario")
        celular = request.form.get("celular")
        contraseña = request.form.get("contraseña")
        confirmacion = request.form.get("confirmacion")
        direccion = request.form.get("direccion")
        departamento = request.form.get("departamento")
        if not nombre:
            print("Paso por Aca 1")
            flash('Ingrese su nombre', 'alert-warning')
            return redirect("/registrarse")
        if not apellido:
            print("Paso por Aca 2")
            flash('Ingrese su apellido', 'alert-warning')
            return redirect("/registrarse")
        if not usuario:
            flash('Ingrese el nombre de usuario', 'alert-warning')
            return redirect("/registrarse")
        if not contraseña:
            print("Paso por Aca 3")
            flash('Ingrese la contrasena', 'alert-warning')
            return redirect("/registrarse")
        if not confirmacion:
            print("Paso por Aca 4")
            flash('Es necesaria la confirmacion de su contrasena', 'alert-warning')
            return redirect("/registrarse")
        if not direccion:
            print("Paso por Aca 5")
            flash('Ingrese su direccion', 'alert-warning')
            return redirect("/registrarse")
        if not departamento:
            print("Paso por Aca 6")
            flash('Elija su departamento', 'alert-warning')
            return redirect("/registrarse")
        if not celular:
            print("Paso por Aca 7")
            flash('Ingrese su numero de celular', 'alert-warning')
            return redirect("/registrarse")
        if contraseña != confirmacion:
            print("Paso por Aca 8")
            flash('Las contraseñas no son iguales', 'alert-warning')
            return redirect("/registrarse")
        try:
            print("try")
            # query = text("INSERT INTO persona(nombre_persona, apellido_persona, usuario, direccion, celular, contraseña, roles) VALUES (:nombre, :apellido, :usuario :direccion, :celular, :contraseña, :roles)")
            # db.execute(query, {"nombre_persona":nombre, "apellido_persona": apellido, "usuario": usuario, "contraseña": contraseña, "direccion": direccion, "celular": celular, "roles": 0})
            
            query = text("INSERT INTO persona(nombre_persona, apellido_persona, usuario, direccion, celular, contraseña, roles, departamento) VALUES (:nombre_persona, :apellido_persona, :usuario, :direccion, :celular, :contraseña, :roles, :departamento) RETURNING id_persona")
            params = {"nombre_persona": nombre, "apellido_persona": apellido, "usuario": usuario, "contraseña": generate_password_hash(contraseña), "direccion": direccion, "celular": celular, "roles": bool(0), "departamento": departamento}
            x=db.execute(query, params)
            
            row = x.fetchone()
            if row:
                session['user_id'] = row[0]
                db.commit()
            print("Paso por Aca commit")
            return redirect("/")
        except OperationalError:
            print("Error connecting to the database :/")
            return redirect("/registrarse")
    return render_template("registrarse.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
        # User reached route via POST (as by submitting a form via POST)

    usuario = request.form.get("usuario")
    contraseña = request.form.get("contraseña")
            
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("usuario"):
            flash('Ingrese el nombre de usuario', 'alert-warning')
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("contraseña"):
            flash('Ingrese su contraseña', 'alert-warning')
            return redirect("/login")

            # Query database for username
        rows = text("SELECT * FROM persona WHERE usuario = :usuario")
        result = db.execute(rows, {"usuario":usuario, "contraseña": contraseña}).fetchone()

      
        
        print(result)
        # print(request.form.get("contraseña"))
        
        print(check_password_hash(str(result[5]), request.form.get("contraseña")))
        
        # Ensure username exists and password is correct
        if result is None or not check_password_hash(str(result[5]), request.form.get("contraseña")):
            print("Paso por aca")
            flash('Ingrese bien los campos', 'alert-warning')
            print("Paso por aca 2")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = result[0]
        # Redirect user to home page
        print("Paso por aca 3")
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



# parte del admin
@app.route("/admin/categoria" , methods=["GET", "POST"])
def catadmin():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        query = text("INSERT INTO categoria(nombre_categoria) VALUES (:nombre)")
        db.execute(query, {"nombre_persona":nombre})
        db.commit()
        redirect("/admin/categoria")
    return render_template("admin/categoria.html", categorias = query)
