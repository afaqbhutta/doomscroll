import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # format: postgresql://user:password@host/dbname
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOB_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    BLOB_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
