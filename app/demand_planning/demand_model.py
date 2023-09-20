from app import db  # Assuming you have a Flask app and SQLAlchemy instance named 'db'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


class DemandDataModel(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    customer_specific = db.Column(JSONB)
    customer_neutral = db.Column(JSONB)
    demandFileKey = db.Column(db.String(255))
    date = db.Column(db.Date)
    demandDataType=db.Column(JSONB)
    userId=db.Column(db.String(255))
    documentId=db.Column(db.String(255))
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
  
    

    
    