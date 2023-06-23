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
    direccion_emp TEXT NOT NULL,
    user_redSocial TEXT NOT NULL,
    celular_emp INTEGER NOT NULL,
    estado Boolean NOT NULL DEFAULT TRUE
        )"""
    )

    producto = text("""CREATE TABLE IF NOT EXISTS producto (
        id_emp INTEGER REFERENCES emprendimiento (id_emp),
        id_producto SERIAL PRIMARY KEY,
        id_categoria INTEGER REFERENCES categoria (id_categoria),
        nombreProducto VARCHAR(50),
        cant_producto INTEGER,
        precioProducto NUMERIC,
        descripcion TEXT,
        estado Boolean NOT NULL DEFAULT TRUE
        )"""
    )

    imagen = text("""CREATE TABLE IF NOT EXISTS imagen (
        id_imagen SERIAL PRIMARY KEY,
        id_producto INTEGER REFERENCES producto (id_producto),
        img_url VARCHAR,
        estado Boolean NOT NULL DEFAULT TRUE
        )"""
    )

    categoria = text ("""CREATE TABLE IF NOT EXISTS categoria (
        id_categoria SERIAL PRIMARY KEY,
        nombre_categoria TEXT NOT NULL,
        padre_id INT NULL,
        FOREIGN KEY (padre_id) REFERENCES Categoria(id_categoria) ON DELETE CASCADE,
        estado Boolean NOT NULL DEFAULT TRUE
    )"""
    )

    pedido = text("""CREATE TABLE IF NOT EXISTS pedido (
        id_pedido SERIAL PRIMARY KEY,
        id_persona INTEGER REFERENCES persona (id_persona),
        id_prod INTEGER REFERENCES producto (id_producto),
        cant_prod INTEGER,
        precio_total NUMERIC,
        verified BOOLEAN NOT NULL,
        estado Boolean NOT NULL DEFAULT TRUE
    )"""
    )

    repartidor = text ("""CREATE TABLE IF NOT EXISTS repartidor (
        id_repartidor SERIAL PRIMARY KEY,
        nombre_rep TEXT NOT NULL,
        id_pedido INTEGER REFERENCES pedido (id_pedido),
        estado Boolean NOT NULL DEFAULT TRUE
    )"""
    )

    persona = text ("""CREATE TABLE IF NOT EXISTS persona (
        id_persona SERIAL PRIMARY KEY,
        nombre_persona TEXT NOT NULL,
        apellido_persona TEXT NOT NULL,
        usuario TEXT NOT NULL,
        celular INTEGER NOT NULL,
        contraseña VARCHAR,
        direccion TEXT,
        roles BOOLEAN NOT NULL,
        departamento VARCHAR,
        estado Boolean NOT NULL DEFAULT TRUE
    )"""
    )

    entrega = text("""CREATE TABLE IF NOT EXISTS entrega (
        id_entrega SERIAL PRIMARY KEY,
        id_pedido INTEGER REFERENCES pedido (id_pedido),
        fecha TIMESTAMP,
        id_repartidor INTEGER REFERENCES repartidor (id_repartidor),
        estado Boolean NOT NULL DEFAULT TRUE
    )"""
    )


    roles = text("""
        CREATE TABLE roles (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50) NOT NULL,
            estado Boolean NOT NULL DEFAULT TRUE
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