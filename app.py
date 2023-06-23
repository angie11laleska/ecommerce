
import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, current_app
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, stringAleatorio
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv


#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename 
#El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
import os 
from os import remove #Modulo  para remover archivo
from os import path #Modulo para obtener la ruta o directorio

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route("/")

def index():
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    query2 = db.execute(text("Select * from producto p JOIN categoria c ON p.id_categoria = c.id_categoria order by id_producto DESC  "))
    flash('Este es el index', 'success')
    return render_template("index.html", navcat= query1, productos= query2)

@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("categorias.html", navcat=query1)

@app.route("/emprendimiento", methods=["GET", "POST"])
def emprendimiento():
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("emprendimiento.html", navcat=query1)

@app.route("/carrito", methods=["GET", "POST"])
@login_required
def carrito():
    """Carrito"""
    if request.method == "POST":
        session["carrito"] = []
        id = request.form.get("id_persona")
        session["carrito"].append(id)
        query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
        return render_template("carrito.html", navcat=query1)
    
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
            
            query = text("INSERT INTO persona(nombre_persona, apellido_persona, usuario, direccion, celular, contraseña, departamento) VALUES (:nombre_persona, :apellido_persona, :usuario, :direccion, :celular, :contraseña, :departamento) RETURNING id_persona")
            params = {"nombre_persona": nombre, "apellido_persona": apellido, "usuario": usuario, "contraseña": generate_password_hash(contraseña), "direccion": direccion, "celular": celular, "departamento": departamento}
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
            flash('Ingrese el nombre de usuario', 'warning')
            return redirect("/login")
        # Ensure password was submitted
        elif not request.form.get("contraseña"):
            flash('Ingrese su contraseña', 'warning')
            return redirect("/login")

            # Query database for username
        rows = text("SELECT * FROM persona WHERE usuario = :usuario")
        result = db.execute(rows, {"usuario":usuario, "contraseña": contraseña}).fetchone()
        print(result)
        # print(request.form.get("contraseña"))
        
        # print(check_password_hash(str(result[6]), request.form.get("contraseña")))
        
        # Ensure username exists and password is correct
        if result is None or not check_password_hash(str(result[5]), request.form.get("contraseña")):
            print("Paso por aca")
            flash('Ingrese bien los campos', 'alert-warning')
            print("Paso por aca 2")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = result[0]
        session["rol"] = result[9]
        x = session["rol"]
        
        print(f"ESto es lo que devuelve usuario {result}")
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
#pensar en una implmentacion de admin 
# Categoria admin
@app.route("/admin/categoria" , methods=["GET", "POST"])
@login_required
def catadmin():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        catPadre = request.form.get("catPadre")
        if not request.form.get("nombre"):
            flash('Es necesario ingresar una categoria', 'warning')
            return redirect("/admin/categoria")
        # Ensure password was submitted
        # elif not request.form.get("catPadre"):
        #     flash('Elija una categoría padre', 'warning')
        #     return redirect("/admin/categoria")
        
        if request.form.get("catPadre"):
            catPadre = catPadre
            query = text("INSERT INTO categoria(nombre_categoria, padre_id) VALUES (:nombre,:catPadre)")
            db.execute(query, {"nombre":nombre, "catPadre":catPadre})
            db.commit()
            return redirect("/admin/categoria")
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
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("admin/categoria.html", categorias = query, cat_padre= query2, navcat=query1)

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
        query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
        return redirect("/admin/categoria", navcat=query1)

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

@app.route("/admin/categoria/eliminar/<int:id>" , methods=["GET"])
def eliminarCat(id):
    query = (text("delete from categoria where id_categoria= (:id)"))
    db.execute(query,{"id":id})
    db.commit()
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return redirect("/admin/categoria", navcat=query1)

#Endcategoria

# inicio de emprendimiento
@app.route("/admin/emp", methods=["GET", "POST"])
def emprendimientos():
    print('Paso por aca')
          
    query = db.execute( text("select id_persona, nombre_persona from persona"))
    query2 = db.execute( text("""
                                    select id_emp, nombre_persona, nombre_emp, direccion_emp, celular_emp, emprendimiento.estado from emprendimiento INNER JOIN
                                    persona ON persona.id_persona = emprendimiento.id_persona
    """))
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("admin/emprender.html", personas=query, info = query2, navcat=query1)
#da un error
@app.route("/admin/emp/agregar", methods=["GET", "POST"])
def emp_add():
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
            return redirect("/admin/emp")
        if not redS:
            flash('Ingrese el usuario de su red social', 'warning')
            return redirect("/admin/emp")
        if not phone:
            flash('Ingrese el numero de su celular', 'warning')
            return redirect("/admin/emp")
        if not direccion:
            flash("Ingrese su direccion", 'warning')
            return redirect("/admin/emp")
        if not idpersona:
            flash('Seleccione una opcion', 'warning')
            return redirect("/admin/emp")
        try:
             query = text("""INSERT INTO emprendimiento( id_persona, nombre_emp, direccion_emp, user_redsocial, celular_emp) 
                             VALUES (:idpersona,:nombreE, :direccion, :redS,:phone) 
                             """)
             params = {"idpersona":idpersona,"nombreE":nombreE, "direccion": direccion, "redS":redS,"phone":phone}
             db.execute(query,params)
             db.commit()
             return redirect("/admin/emp")
        except OperationalError:
             flash("Ocurrio un error, intentelo nuevamente", "danger")
             return redirect("/admin/emp")
    query = db.execute( text("select id_persona, nombre_persona from persona"))
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("/admin/add-emp.html", personas = query, navcat=query1)

@app.route("/admin/emp/editar/<int:id_emp>", methods=["GET", "POST"])
def emp_edit(id_emp):
    if request.method == "POST":
        idhidden = request.form.get("id_emp")
        nombre = request.form.get("nombreE")
        red = request.form.get("redS")
        phone = request.form.get("phone")
        direccion = request.form.get("direccion")
        persona = request.form.get("personaN")
        
        if nombre:
            query = (text("UPDATE emprendimiento SET nombre_emp = :nombre, user_redsocial = :red, celular_emp = :phone, direccion_emp = :direccion, id_persona = :persona WHERE id_emp = (:idhidden);"))
            db.execute(query,{"idhidden":idhidden, "nombre":nombre, "red":red, "phone":phone, "direccion": direccion, "persona": persona})
            print("nombre")        
        db.commit()  
        return redirect("/admin/emp")
    
    # query2 = db.execute(text("select * from emprendimiento")).fetchall()
    
    query3 = text("SELECT * FROM emprendimiento WHERE id_emp = :id_emp")
    formulario = db.execute(query3,{"id_emp":id_emp}).fetchone()
    personas = db.execute( text("select id_persona, nombre_persona from persona"))
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("/admin/edit-emp.html", id_emp = int(id_emp),formulario = formulario, personas=personas, navcat=query1)

#validar un boton de activo o inactivo
@app.route("/admin/emp/eliminar/<int:id_emp>" , methods=["GET"])
def eliminarEmp(id_emp):
    query = (text("UPDATE emprendimiento SET estado = :estado where id_emp= (:id)"))
    db.execute(query,{"id":id_emp, "estado":False})
    db.commit()
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return redirect("/admin/emp", navcat=query1)
#fin de Emprendimiento

#inicio roles
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
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("admin/roles.html", roles = query2, navcat=query1)

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
        query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
        return redirect("/admin/roles", navcat=query1)
    
    query2 = db.execute(text("select * from roles")).fetchall()
    
    query3 = text("SELECT nombre FROM roles WHERE id = :id")
    formulario = db.execute(query3,{"id":id}).fetchone()
    print(f"Esto es categoria2 {query2}")
    query = db.execute( text("select id_persona, nombre_persona from persona"))
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("/admin/editRoles.html", id = int(id),formulario = formulario, roles = query2, navcat=query1)

@app.route("/admin/roles/eliminar/<int:id>" , methods=["GET"])
def eliminarRoles(id):
    query = (text("delete from roles where id= (:id)"))
    db.execute(query,{"id":id})
    db.commit()
    return redirect("/admin/roles")
    
# endroles

#inicio repartidor
@app.route("/admin/repartidor", methods=["GET", "POST"])
def repartidor():
    if request.method == "POST":
        nombre_rep = request.form.get("nombre_rep")
        if nombre_rep:
            query = text("INSERT INTO repartidor(nombre_rep) VALUES (:nombre_rep)")
            db.execute(query, {"nombre_rep":nombre_rep})
            db.commit()
            redirect("/admin/repartidor")
        else:
            flash("Ingrese un repartidor", "warning")
    query2 = db.execute(text("select * from repartidor")).fetchall() 
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("admin/repartidor.html", repartidor = query2, navcat=query1)

@app.route("/admin/repartidor/editar/<int:id_repartidor>" , methods=["GET","POST"])
def editarRep(id_repartidor):
    if request.method == "POST":
        id_repartidor = request.form.get("id_repartidor")
        nombre_rep = request.form.get("nombre")
        if nombre_rep:
            query = (text("UPDATE repartidor SET nombre_rep = :nombre_rep WHERE id_repartidor = (:id_repartidor);"))
            db.execute(query,{"id_repartidor":id_repartidor, "nombre_rep":nombre_rep})
            print("nombre_rep")        
        db.commit()  
        return redirect("/admin/repartidor")
    print(id_repartidor)
    query2 = db.execute(text("select * from repartidor")).fetchall()
    
    query3 = text("SELECT nombre_rep FROM repartidor WHERE id_repartidor = :id_repartidor")
    formulario = db.execute(query3,{"id_repartidor":id_repartidor}).fetchone()
    print(f"Esto es repartidor {query2}")
    query = db.execute( text("select id_repartidor, nombre_rep from repartidor"))
    return render_template("/admin/editRepartidor.html", id_repartidor = int(id_repartidor),formulario = formulario, repartidor = query2)

@app.route("/admin/repartidor/eliminar/<int:id_repartidor>" , methods=["GET"])
def eliminarRep(id_repartidor):
    query = (text("delete from repartidor where id_repartidor= (:id)"))
    db.execute(query,{"id":id_repartidor, "estado":False})
    db.commit()
    return redirect("/admin/repartidor")


# Articulos
@app.route("/misproductos",methods=["GET","POST"])
def misproductos():

    query = text("""
                    select producto.id_producto,producto.nombreproducto,producto.cant_producto, producto.precioproducto, categoria.nombre_categoria, producto.estado, producto.url_image from producto inner join emprendimiento on producto.id_emp = emprendimiento.id_emp
                    INNER JOIN persona on emprendimiento.id_persona = persona.id_persona inner join categoria on producto.id_categoria = categoria.id_categoria where persona.id_persona = :iduser""")
    productos = db.execute(query, {"iduser":session["user_id"]})
    print(productos)
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("misproductos.html", productos = productos, navcat=query1)

@app.route("/addproducto",methods=["GET","POST"])
def addproductos():

    if request.method == "POST":
        nombreprod = request.form.get("nombre")
        cantidadprod = int(request.form.get("cantidad"))
        precioprod = int(request.form.get("precio"))
        descripcprod = request.form.get("descripcion")
        idemp = request.form.get("idemp")
        idcat = request.form.get("idcat")
        print(f"Este es el id de emp {idemp}")
        print(f"Este es el id de cat {idcat}")

        if(request.files['archivo']):
                file = request.files['archivo']
                basepath = os.path.dirname(__file__)  # La ruta donde se encuentra el archivo actual
                filename = secure_filename(file.filename)  # Nombre original del archivo

                # Capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
                extension = os.path.splitext(filename)[1]
                nuevoNombreFile = stringAleatorio() + extension

                upload_path = path.join(basepath, 'static/archivos', nuevoNombreFile)
                print(f"Este es el upload path: {upload_path}")
                file.save(upload_path)
                relative_path = upload_path.split('static', 1)[1].strip('/')
                print(f"Este es el nombre de la img {relative_path}")
                ruta = f"\static\{relative_path}"
                print(ruta)

        consulta = text("""Insert into producto(id_emp,id_categoria,nombreproducto, cant_producto, precioproducto, descripcion, url_image)
                            values(:idemp,:idcat,:nombreprod,:cantprod,:precioprod,:descripc,:url)""")
        db.execute(consulta,{"idemp":idemp,"idcat":idcat,"nombreprod":nombreprod,"cantprod":cantidadprod,"precioprod":precioprod,"descripc":descripcprod,"url":ruta})
        db.commit()
        return redirect("/misproductos")

    query = text("""select emprendimiento.id_emp, emprendimiento.nombre_emp from emprendimiento 
                    inner join persona on emprendimiento.id_persona = persona.id_persona 
                    where persona.id_persona = :idpersona""")
    resultadoemp = db.execute(query,{"idpersona":session["user_id"]}).fetchall()
    print(resultadoemp)

    if resultadoemp == []:
        flash("Debe de registrar un emprendimiento para poder publicar un producto", "danger")
        return redirect("/")
    
    query2 = text("select * from categoria")
    resultadocat = db.execute(query2).fetchall()
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("addproducto.html", selectemp = resultadoemp, selectcat = resultadocat, navcat=query1)

@app.route("/misproductos/eliminar/<int:id_producto>" , methods=["GET"])
def eliminarProd(id_producto):
    query = (text("delete from producto where id_producto= (:id)"))
    db.execute(query,{"id":id_producto, "estado":False})
    db.commit()
    return redirect("/misproductos")

@app.route("/misproductos/editar/<int:id_producto>", methods=["GET", "POST"])
def producto_edit(id_producto):
    if request.method == "POST":
        idhidden = request.form.get("id_producto")
        nombre = request.form.get("nombre")
        cantidad = request.form.get("cantidad")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion") 
        
        if nombre:
            query1 = (text("UPDATE producto SET nombreProducto = :nombre, cant_producto = :cantidad, precioProducto = :precio, descripción = :descripcion WHERE id_producto = (:idhidden);"))
            db.execute(query1,{"idhidden":idhidden, "nombre":nombre, "cantidad":cantidad, "precio":precio, "descripcion": descripcion})
            print("nombre")        
        db.commit()  
        return redirect("/misproductos")
    query = text("""select emprendimiento.id_emp, emprendimiento.nombre_emp from emprendimiento 
                    inner join persona on emprendimiento.id_persona = persona.id_persona 
                    where persona.id_persona = :idpersona""")
       
    resultadoemp = db.execute(query,{"idpersona":session["user_id"]}).fetchall()
    print(resultadoemp)
    
    query2 = text("select * from categoria")
    resultadocat = db.execute(query2).fetchall()
        

    query3 = text("SELECT * FROM producto WHERE id_producto = :id_producto")
    formulario = db.execute(query3,{"id_producto":id_producto}).fetchone()
    producto = db.execute( text("select id_producto, nombreProducto from producto"))
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("editarproducto.html", id_producto = int(id_producto),formulario = formulario, producto=producto, selectemp = resultadoemp, selectcat = resultadocat, navcat=query1)

@app.route("/categoria/<nombreCat>", methods=["GET", "POST"])
def infocat(nombreCat):
    query = (text("select id_producto, nombre_categoria, nombreproducto, cant_producto,precioproducto,descripcion, producto.url_image from producto inner join categoria on producto.id_categoria = categoria.id_categoria where categoria.nombre_categoria= :nombreCat"))
    resultad = db.execute(query,{"nombreCat":nombreCat}).fetchall()
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    print(resultad)
    return render_template("listaProductos.html", resul=resultad, navcat=query1)

@app.route("/producto/<int:id_producto>", methods=["GET", "POST"])
def productoid( id_producto):
    query = text("select * from producto inner join categoria on producto.id_categoria = categoria.id_categoria where id_producto = :idproductos")
    resultado = db.execute(query, {"idproductos":id_producto}).fetchall()
    print(resultado)
    query1 = db.execute(text("""
                            SELECT c1.id_categoria, c1.nombre_categoria, c2.nombre_categoria AS cat_padre 
                            FROM categoria AS c1 
                            LEFT JOIN categoria AS c2 ON c1.padre_id = c2.id_categoria
                            ORDER BY c1.padre_id IS NULL DESC
                            """))
    return render_template("producto.html", resul = resultado, navcat=query1)



@app.route("/admin", methods=["GET", "POST"])
def admin( ):
    return render_template("admin/admin.html")

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('page_not_found.html'), 404