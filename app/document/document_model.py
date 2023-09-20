from app import db  # Assuming you have a Flask app and SQLAlchemy instance named 'db'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Document(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    startdate = db.Column(db.Date, nullable=True)
    enddate = db.Column(db.Date, nullable=True)
    demanddate = db.Column(db.Date, nullable=True)
    productData = db.Column(db.String(255), nullable=True)
    supplierCapacity = db.Column(db.String(255), nullable=True)
    productionCapacity = db.Column(db.String(255), nullable=False)  # Non-nullable with a default value
    productionCapacityBacklog = db.Column(db.String(255), nullable=True)
    workStation = db.Column(db.String(255), nullable=True)
    demandId = db.Column(db.String(255), nullable=True)
    demandFileKey = db.Column(db.String(255), nullable=True)
    productId = db.Column(db.String(255), nullable=True) 
    productReference = db.Column(db.String(255), nullable=True)
    supplierCapacityFileKey = db.Column(db.String(255), nullable=True)
    backlogFileKey = db.Column(db.String(255), nullable=True)
    workStationFileKey = db.Column(db.String(255), nullable=True)
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))