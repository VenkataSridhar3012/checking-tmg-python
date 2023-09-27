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
    
    
    
def document_to_json(document):
    data = {
        "id": str(document.id),
        "startdate": document.startdate.isoformat() if document.startdate else None,
        "enddate": document.enddate.isoformat() if document.enddate else None,
        "demanddate": document.demanddate.isoformat() if document.demanddate else None,
        "productData": document.productData,
        "supplierCapacity": document.supplierCapacity,
        "productionCapacity": document.productionCapacity,
        "productionCapacityBacklog": document.productionCapacityBacklog,
        "workStation": document.workStation,
        "demandId": document.demandId,
        "demandFileKey": document.demandFileKey,
        "productId": document.productId,
        "productReference": document.productReference,
        "supplierCapacityFileKey": document.supplierCapacityFileKey,
        "backlogFileKey": document.backlogFileKey,
        "workStationFileKey": document.workStationFileKey,
        "createdAt": document.createdAt.isoformat(),
        "updatedAt": document.updatedAt.isoformat(),
        # Add other attributes as needed
    }
    return data
