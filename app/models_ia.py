from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from database_ia import BaseIA

class ConsultaIA(BaseIA):
    """
    Tabla para almacenar consultas generadas por IA, con su respectivo SQL.
    """
    __tablename__ = "consultas_ia"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(Text, nullable=False)  # Pregunta en lenguaje natural
    consulta_sql = Column(Text, nullable=False)  # SQL generado
    fecha_creacion = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

