import uuid
from app import db
from sqlalchemy import Column, String, PrimaryKeyConstraint,DateTime,text,Boolean
from sqlalchemy.dialects.postgresql import UUID,JSONB
from datetime import datetime
        
        
class ActionPoint(db.Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    actionPointName = db.Column(db.String(80))
    actionPointDescription = db.Column(db.String(80))
    demandType = db.Column(db.String(80))
    customerName = db.Column(db.String(80))
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    value = db.Column(db.String(80))
    currency = db.Column(db.String(80))
    product_segment = db.Column(JSONB, default=[])
    product_group = db.Column(JSONB, default=[])
    product = db.Column(JSONB, default=[])
    enable =  db.Column(Boolean,default=True)
    scenarioId = db.Column(UUID(as_uuid=True), db.ForeignKey('scenario.id'))
    scenario = db.relationship('Scenario', backref='actionPoint')
    createdAt = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = Column(DateTime, onupdate=datetime.now, server_default=text('CURRENT_TIMESTAMP'))
    
    
    
def action_point_to_json(action_point):
    data = {
        "id": str(action_point.id),
        "actionPointName": action_point.actionPointName,
        "actionPointDescription": action_point.actionPointDescription,
        "demandType": action_point.demandType,
        "customerName": action_point.customerName,
        "startDate": action_point.startDate.isoformat() if action_point.startDate else None,
        "endDate": action_point.endDate.isoformat() if action_point.endDate else None,
        "value": action_point.value,
        "currency": action_point.currency,
        "productSegment": action_point.productSegment,
        "productGroup": action_point.productGroup,
        "product": action_point.product,
        "enable": action_point.enable,
        "scenarioId": str(action_point.scenarioId),
        "createdAt": action_point.createdAt.isoformat(),
        "updatedAt": action_point.updatedAt.isoformat(),
        # Add other attributes as needed
    }
    return data

    