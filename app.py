import os
from flask import Flask, flash, redirect, render_template, request, session
from .models import *

app = Flask(__name__)


@app.route("/")
def layout():
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


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    return render_template("registrarse.html")

app = Flask(__name__)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")
    contraseña = request.form.get("contraseña")
    confirmacion = request.form.get("confirmacion")
    direccion = request.form.get("direccion")
    departamento = request.form.get("departamento")
    numTelefono = request.form.get("celular")
    if not nombre:
        return redirect("/login")
    if not apellido:
        return redirect("/login")
    if not contraseña:
        return redirect("/login")
    if not confirmacion:
        return redirect("/login")
    if not direccion:
        return redirect("/login")
    if not departamento:
        return redirect("/login")
    if contraseña != confirmacion:
        return redirect("/login")
    try:
        query = text("INSERT INTO persona(nombre_persona, apellido, direccion, celular, pago, contra, roles) VALUES (:nombre, :direccion, :celular, :pago, :contra, :roles)")
        db.execute(query, {"nombre":nombre, "contra": contraseña, "direccion": direccion, "celular": numTelefono, "pago": 0, "roles": 0})
        db.commit
    except:
        return redirect("/login")
    return redirect("/login")

