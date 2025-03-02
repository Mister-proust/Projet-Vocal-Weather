from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from Database.db_connection import build_engine
import os

# DB schema 
schema='public'

# Metadata
metadata_obj = MetaData(schema=schema)

Base = declarative_base(metadata=metadata_obj)

#######################################################################
####                   Table Declarative Models                     ### 
#######################################################################

class Monitoring(Base):
    __tablename__ = 'Monitoring'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    texte_origine = Column(String, nullable=False)
    code_stt = Column(String, nullable=False, default="OK")
    time_stt = Column(Integer, nullable=False)  # Temps en ms
    msg_stt = Column(String, nullable=True)
    loc = Column(String, nullable=True)  # Localisation
    date_info = Column(String, nullable=True)  # Date extraite
    gemini_response = Column(String, nullable=True)  # Réponse de Gemini


