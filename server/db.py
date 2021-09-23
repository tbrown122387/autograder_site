import os
from sqlmodel import create_engine

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_ADDRESS = os.environ['POSTGRES_ADDRESS']

# Scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URI, echo=True)
