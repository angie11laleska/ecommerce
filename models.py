import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main ():
    tabla_categoria = text (
    """ CREATE TABLE categoria (
        id_categoria SERIAL PRIMARY KEY,
        nombre_categoria VARCHAR(50) NOT NULL
    )
    """
    )
    
    db.execute(tabla_categoria)