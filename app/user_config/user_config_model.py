import uuid
from app import db
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
        
        
class Config(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    planningDuration = db.Column(db.String(80), unique=True, nullable=False)
    moduleNameAccess = db.Column(db.String(120), nullable=False)
    userId = db.Column(db.String(255))
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
    