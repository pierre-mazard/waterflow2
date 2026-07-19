from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, Float, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id_client = Column(Integer, primary_key=True, index=True)
    code_client = Column(String(50), unique=True, nullable=False)
    nom_structure = Column(String(255), nullable=False)
    adresse_postale = Column(Text)
    api_key = Column(String(255), unique=True, nullable=False)
    date_creation = Column(TIMESTAMP)
    actif = Column(Boolean, default=True)


class Measurement(Base):
    __tablename__ = "measurements"

    id_measurement = Column(Integer, primary_key=True)
    id_client = Column(Integer, ForeignKey("clients.id_client"), nullable=False)
    date_prelevement = Column(TIMESTAMP, nullable=False)
    lieu_prelevement = Column(String(255))

    ph = Column(Float)
    hardness = Column(Float)
    solids = Column(Float)
    chloramines = Column(Float)
    sulfate = Column(Float)
    conductivity = Column(Float)
    organic_carbon = Column(Float)
    trihalomethanes = Column(Float)
    turbidity = Column(Float)

    provenance = Column(String(20))
    prediction = Column(Integer)
    prediction_model_version = Column(String(50))
    created_at = Column(TIMESTAMP)
