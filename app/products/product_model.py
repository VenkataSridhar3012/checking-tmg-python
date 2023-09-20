from app import db  # Assuming you have a Flask app and SQLAlchemy instance named 'db'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
     
class ProductDataModel(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    productNumber = db.Column(db.String(255))
    productName = db.Column(db.String(255))
    productSegmaentNumber = db.Column(db.String(255))
    productSegmentName = db.Column(db.String(255))
    materialNumber=db.Column(db.String(255))
    materialName=db.Column(db.String(255))
    documentId=db.Column(db.String(255))
    productFileKey=db.Column(db.String(255))
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
    