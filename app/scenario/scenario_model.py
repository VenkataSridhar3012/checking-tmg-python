import uuid
from app import db
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text,Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
        
        
class Scenario(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    scenarioName = db.Column(db.String(80))
    scenarionDescription = db.Column(db.String(80))
    isPublish  = db.Column(Boolean,default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user')
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
    
    
    
def scenario_to_json(scenario):
    data = {
        "id": str(scenario.id),
        "scenarioName": scenario.scenarioName,
        "scenarioDescription": scenario.scenarionDescription,
        "isPublish": scenario.isPublish,
        "user_id": str(scenario.user_id),
        "createdAt": scenario.createdAt.isoformat(),
        "updatedAt": scenario.updatedAt.isoformat(),
        # Add other attributes as needed
    }
    return data
    