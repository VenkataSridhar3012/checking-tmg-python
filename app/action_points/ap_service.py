from flask import jsonify
from sqlalchemy import and_, text, or_,cast
from sqlalchemy.dialects.postgresql import JSONB
from .ap_model import db,ActionPoint,action_point_to_json
from sqlalchemy.sql.expression import bindparam

def sv_create_actionPoint(scenarioId, data):
    try:
        data['scenarioId'] = scenarioId
        new_action_point = ActionPoint(**data)
        db.session.add(new_action_point)
        db.session.commit()
        
        return jsonify({'message': 'ActionPoint created successfully', 'id': new_action_point.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def sv_editActionPoint(id, data):
    try:
        action_point = ActionPoint.query.get(id)
        if action_point is None:
            return jsonify({'error': 'ActionPoint not found'}), 404
        
        for key, value in data.items():
            setattr(action_point, key, value)
        
        db.session.commit()
        
        return jsonify({'message': 'ActionPoint updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def sv_deleteActionPoint(id):
    try:
        action_point = ActionPoint.query.get(id)
        if action_point is None:
            return jsonify({'error': 'ActionPoint not found'}), 404

        db.session.delete(action_point)
        db.session.commit()

        return jsonify({'message': 'ActionPoint deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
def sv_getActionPoints(scenario_id):
    try:
        
        # Query the ActionPoint table based on the specified criteria
        action_points = ActionPoint.query.filter(
            ActionPoint.scenarioId == scenario_id,
        ).all()
        if not action_points:
            return jsonify({'error': 'No matching ActionPoints found'}), 404
        
        
        # Convert the list of ActionPoints to a JSON response
        action_points_data = [
            {
               "id": str(action_point.id),
               "actionPointName": action_point.actionPointName,
               "actionPointDescription": action_point.actionPointDescription,
               "demandType": action_point.demandType,
               "startDate": action_point.startDate.isoformat() if action_point.startDate else None,
               "endDate": action_point.endDate.isoformat() if action_point.endDate else None,
               "value": action_point.value,
               "currency": action_point.currency,
               "product_segment": action_point.product_segment,
               "product_group": action_point.product_group,
               "product": action_point.product,
               "enable": action_point.enable,
               "scenarioId": str(action_point.scenarioId),
               "createdAt": action_point.createdAt.isoformat(),
               "updatedAt": action_point.updatedAt.isoformat(),
                 # Add other attributes as needed
            }
            for action_point in action_points
        ]
        print(f"Action points data: {action_points_data}")
        return jsonify({'actionPoints': action_points_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_actionPpoints_BasedOnCondition(product_segments, product_groups, products, scenario_id, customerName):
    try:
        # Create a list to hold the filtering conditions
        filters = []

        # # Add the scenario_id filter if it is provided
        # if scenario_id:
        #     filters.append(ActionPoint.scenarioId == scenario_id)

        # # Add the customer_name filter if it is provided
        # if customerName:
        #     filters.append(ActionPoint.customerName == customerName)

        # Add productSegment filter if it is provided
        if product_segments:
           segment_filters = [
                text("EXISTS (SELECT 1 FROM jsonb_array_elements_text(action_point.product_segment) AS p WHERE p = ANY (:segments))").params(segments=product_segments)
           ] 
           filters.append(and_(*segment_filters))

        if product_groups:
           group_filters = [
               text("EXISTS (SELECT 1 FROM jsonb_array_elements_text(action_point.product_group) AS p WHERE p = ANY (:groups))").params(groups=product_groups)
           ]
           filters.append(and_(*group_filters))

        if products:
           product_filters = [
               text("EXISTS (SELECT 1 FROM jsonb_array_elements_text(action_point.product) AS p WHERE p = ANY (:products))").params(products=products)
           ]
           filters.append(and_(*product_filters))
           

        # Combine all filter conditions with an 'and' clause
        final_filter = or_(*filters)  
        # Query the ActionPoint table based on the specified criteria
        action_points = ActionPoint.query.filter(final_filter).all()
        # Convert the action points to a list of dictionaries
        action_points_data = [
            {
               "id": str(action_point.id),
               "actionPointName": action_point.actionPointName,
               "actionPointDescription": action_point.actionPointDescription,
               "demandType": action_point.demandType,
               "startDate": action_point.startDate.isoformat() if action_point.startDate else None,
               "endDate": action_point.endDate.isoformat() if action_point.endDate else None,
               "value": action_point.value,
               "currency": action_point.currency,
               "product_segment": action_point.product_segment,
               "product_group": action_point.product_group,
               "product": action_point.product,
               "enable": action_point.enable,
               "scenarioId": str(action_point.scenarioId),
               "createdAt": action_point.createdAt.isoformat(),
               "updatedAt": action_point.updatedAt.isoformat(),
                 # Add other attributes as needed
            }
            for action_point in action_points
        ]
       
        return jsonify(action_points_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500