import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main ():
    emprendimiento = text("""CREATE TABLE IF NOT EXISTS emprendimiento (
    id_emp SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES persona (id_persona),
    nombre_emp TEXT NOT NULL,
    user_redSocial TEXT NOT NULL,
    celular_emp INTEGER NOT NULL
        )"""
    )

    producto = text("""CREATE TABLE IF NOT EXISTS producto (
        id_producto SERIAL PRIMARY KEY,
        id_emp INTEGER REFERENCES emprendimiento (id_emp),
        id_categoria INTEGER REFERENCES categoria (id_categoria),
        nombreProducto VARCHAR(50),
        cant_producto INTEGER,
        precioProducto NUMERIC,
        descripción TEXT,
        correo VARCHAR(100)
        )"""
    )

    categoria = text ("""CREATE TABLE IF NOT EXISTS categoria (
        id_categoria SERIAL PRIMARY KEY,
        nombre_categoria TEXT NOT NULL
    )"""
    )

    pedido = text("""CREATE TABLE IF NOT EXISTS pedido (
        id_pedido SERIAL PRIMARY KEY,
        id_persona INTEGER REFERENCES persona (id_persona),
        id_prod INTEGER REFERENCES producto (id_producto),
        cant_prod INTEGER,
        precio_total NUMERIC,
        verified BOOLEAN NOT NULL
    )"""
    )

    repartidor = text ("""CREATE TABLE IF NOT EXISTS repartidor (
        id_repartidor SERIAL PRIMARY KEY,
        nombre_rep TEXT NOT NULL,
        id_pedido INTEGER REFERENCES pedido (id_pedido)
    )"""
    )

    persona = text ("""CREATE TABLE IF NOT EXISTS persona (
        id_persona SERIAL PRIMARY KEY,
        nombre_persona TEXT NOT NULL,
        direccion TEXT NOT NULL,
        celular INTEGER NOT NULL,
        pago NUMERIC NOT NULL,
        contra VARCHAR(8),
        roles BOOLEAN NOT NULL
    )"""
    )

    entrega = text("""CREATE TABLE IF NOT EXISTS entrega (
        id_entrega SERIAL PRIMARY KEY,
        id_pedido INTEGER REFERENCES pedido (id_pedido),
        fecha TIMESTAMP,
        id_repartidor INTEGER REFERENCES repartidor (id_repartidor)
    )"""
    )

    imagen = text("""CREATE TABLE IF NOT EXISTS imagen (
        id_imagen SERIAL PRIMARY KEY,
        id_producto INTEGER REFERENCES producto (id_producto),
        img_url TEXT
    )"""
    )

    roles = text("""
        CREATE TABLE roles (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL
        )
    """)
    
    db.execute(persona)
    db.execute(emprendimiento)
    db.execute(categoria)
    db.execute(producto)
    db.execute(pedido)
    db.execute(repartidor)
    db.execute(entrega)
    db.execute(imagen)
    db.execute(roles)
    db.commit()
    
if __name__ == "__main__":
    main()