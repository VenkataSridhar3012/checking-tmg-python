import uuid
from app import db
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text,Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
        
        
class UserConfig(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    planningDuration = db.Column(db.String(80))
    moduleNameAccess = moduleNameAccess = db.Column(Boolean,default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', backref='configurations')
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
    
    
    
def user_config_to_json(user_config):
    data = {
        "id": str(user_config.id),
        "planningDuration": user_config.planningDuration,
        "moduleNameAccess": user_config.moduleNameAccess,
        "user_id": str(user_config.user_id),
        "createdAt": user_config.createdAt.isoformat(),
        "updatedAt": user_config.updatedAt.isoformat(),
        # Add other attributes as needed
    }
    return data
    