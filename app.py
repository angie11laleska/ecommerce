import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
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
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    flash('Este es el index', 'success')
    return render_template("index.html", navcat= query1)



@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    return render_template("categorias.html")



@app.route("/emprendimiento", methods=["GET", "POST"])
def emprendimiento():
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
            flash('Ingrese su nombre', 'error')
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
        catPadre = request.form.get("catPadre")
        if catPadre:
            catPadre = catPadre
            query = text("INSERT INTO categoria(nombre_categoria, padre_id) VALUES (:nombre,:catPadre)")
            db.execute(query, {"nombre":nombre, "catPadre":catPadre})
            db.commit()
            redirect("/admin/categoria")
        else:
            query = text("INSERT INTO categoria(nombre_categoria) VALUES (:nombre)")
            db.execute(query, {"nombre":nombre})
            db.commit()
            redirect("/admin/categoria")

    # query = db.execute(text("select * from categoria"))
    query = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    query2 = db.execute(text("select * from categoria")).fetchall()
    print(f"Esto es categoria2 {query2}")
    return render_template("admin/categoria.html", categorias = query, cat_padre= query2)

@app.route("/admin/categoria/editar/<int:id_categoria>" , methods=["GET","POST"])
def editarcate(id_categoria):
    if request.method == "POST":
        idhidden = request.form.get("id_categoria")
        nombre = request.form.get("nombre")
        catPadre = request.form.get("catPadre")
        if catPadre:

            query = (text("UPDATE categoria SET nombre_categoria = :nombre, padre_id = :padre_id WHERE id_categoria = (:idhidden);"))
            db.execute(query,{"idhidden":idhidden, "nombre":nombre,"padre_id":catPadre})
            print("categoria padre")
        else:
            query = (text("UPDATE categoria SET nombre_categoria = :nombre WHERE id_categoria = (:idhidden);"))
            db.execute(query,{"idhidden":idhidden, "nombre":nombre})
            print("categoria hijo")
            
        db.commit()
       
        return redirect("/admin/categoria")

    # query = db.execute(text("select * from categoria"))
    # db.commit()
    query = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    query2 = db.execute(text("select * from categoria")).fetchall()
    
    query3 = text("SELECT nombre_categoria, padre_id FROM categoria WHERE id_categoria = :id_categoria")
    formulario = db.execute(query3,{"id_categoria":id_categoria}).fetchone()
    
    print(f"Esto es categoria2 {query2}")
    return render_template("/admin/editcategoria.html", id_categoria = int(id_categoria), categorias = query, cat_padre= query2, formulario = formulario)

@app.route("/admin/categoria/eliminar/<int:id_categoria>" , methods=["GET"])
def eliminarcate(id_categoria):
    query = (text("delete from categoria where id_categoria= (:id)"))
    db.execute(query,{"id":id_categoria})
    db.commit()
    return redirect("/admin/categoria")

@app.route("/admin/emprender", methods=["GET", "POST"])
def emprendimientos():
    print('Paso por aca')
    if request.method == "POST":
        print('Paso por aca 2')
        nombreE = request.form.get("nombreE")
        redS = request.form.get("redS")
        phone = request.form.get("phone")
        idpersona = request.form.get("personaN")
        direccion = request.form.get("direccion")
    
        if not nombreE:
            print('Paso por aca 3')
            flash('Ingrese el nombre del emprendimiento', 'warning')
            return redirect("/admin/emprender")
        if not redS:
            flash('Ingrese el usuario de su red social', 'warning')
            return redirect("/admin/emprender")
        if not phone:
            flash('Ingrese el numero de su celular', 'warning')
            return redirect("/admin/emprender")
        if not direccion:
            flash("Ingrese su direccion", 'warning')
            return redirect("/admin/emprender")
        if not idpersona:
            flash('Seleccione una opcion', 'warning')
            return redirect("/admin/emprender")
        try:
             query = text("""INSERT INTO emprendimiento( id_persona, nombre_emp, direccion_emp, user_redsocial, celular_emp) 
                             VALUES (:idpersona,:nombreE, :direccion, :redS,:phone) 
                             """)
             params = {"idpersona":idpersona,"nombreE":nombreE, "direccion": direccion, "redS":redS,"phone":phone}
             db.execute(query,params)
             db.commit()
        except OperationalError:
             print("Error connecting to the database :/")
        return redirect("admin/emprender")
        
    query = db.execute( text("select id_persona, nombre_persona from persona"))
    
    return render_template("admin/emprender.html", personas=query)

@app.route("/admin/roles", methods=["GET", "POST"])
def roles():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        if nombre:
            query = text("INSERT INTO roles(nombre) VALUES (:nombre)")
            db.execute(query, {"nombre":nombre})
            db.commit()
            redirect("/admin/categoria")
        else:
            flash("Ingrese un rol", "warning")
    query2 = db.execute(text("select * from roles")).fetchall() 
    return render_template("admin/roles.html", roles = query2)

@app.route("/admin/roles/editar/<int:id>" , methods=["GET","POST"])
def editarRoles(id):
    if request.method == "POST":
        idhidden = request.form.get("id")
        nombre = request.form.get("nombre")
        if nombre:
            query = (text("UPDATE roles SET nombre = :nombre WHERE id = (:idhidden);"))
            db.execute(query,{"idhidden":idhidden, "nombre":nombre})
            print("nombre")        
        db.commit()  
        return redirect("/admin/roles")
    
    query2 = db.execute(text("select * from roles")).fetchall()
    
    query3 = text("SELECT nombre FROM roles WHERE id = :id")
    formulario = db.execute(query3,{"id":id}).fetchone()
    
    print(f"Esto es categoria2 {query2}")
    return render_template("/admin/editRoles.html", id = int(id), roles = query, formulario = formulario)

@app.route("/admin/roles/eliminar/<int:id>" , methods=["GET"])
def eliminarRoles(id):
    query = (text("delete from roles where id= (:id)"))
    db.execute(query,{"id":id})
    db.commit()
    return redirect("/admin/roles")
    
