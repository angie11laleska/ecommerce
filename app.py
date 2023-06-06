import os
from flask import Flask, flash, redirect, render_template, request, session


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