# models.py - MODELOS DE LA BASE DE DATOS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


# ========================================
# TABLA: Cliente
# ========================================
class Cliente(db.Model):
    __tablename__ = "Cliente"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombres = db.Column(db.String(30), nullable=False)
    Correo = db.Column(db.String(30), unique=True, nullable=False)
    Passwordd = db.Column(db.String(20), nullable=False)


# ========================================
# TABLA: CodigoVerificacion
# ========================================
class CodigoVerificacion(db.Model):
    __tablename__ = "CodigoVerificacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idCliente = db.Column(db.Integer, nullable=False)
    Codigo = db.Column(db.String(4), nullable=False)
    FechaCaducidad = db.Column(db.DateTime, nullable=False)