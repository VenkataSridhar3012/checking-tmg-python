from flask import jsonify
from .scenario_model import db,Scenario
from ..action_points.ap_model import db,ActionPoint
from sqlalchemy.orm.exc import NoResultFound

def sv_createScenario(data):
    try:
        
        # Create a new Scenario object
        new_scenario = Scenario(
            scenarioName=data['scenarioName'],
            scenarionDescription=data['scenarionDescription'],
            isPublish=data.get('isPublish', True),  # Default to True if not provided
            user_id=data['user_id']
            # Add other attributes as needed
        )

        # Add the new scenario to the database
        db.session.add(new_scenario)
        db.session.commit()

        return jsonify({'message': 'Scenario created successfully', 'scenario_id': str(new_scenario.id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def sv_editScenario(scenario_id, data):
    try:
        # Find the scenario to be edited by its id
        print(scenario_id)
        scenario_to_edit = Scenario.query.get(scenario_id)

        if not scenario_to_edit:
            return jsonify({'error': 'Scenario not found'}), 404

        # Update the scenario attributes based on the data provided
        if 'scenarioName' in data:
            scenario_to_edit.scenarioName = data['scenarioName']
        if 'scenarionDescription' in data:
            scenario_to_edit.scenarionDescription = data['scenarionDescription']
        if 'isPublish' in data:
            scenario_to_edit.isPublish = data['isPublish']
        
        # Add other attributes to update as needed

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Scenario updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def sv_deleteScenario(id):
    try:
        Scenario = Scenario.query.get(id)
        if Scenario is None:
            return jsonify({'error': 'Scenario not found'}), 404
        # deleteing action points
        db.query(ActionPoint).filter(ActionPoint.scenarioId == id).delete()
        db.commit()
        
        db.session.delete(Scenario)
        db.session.commit()

        return jsonify({'message': 'Scenario deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
def get_scenario(id):
    try:
        scenario = Scenario.query.get(id)
        if scenario is None:
            return jsonify({'error': 'Scenario not found'}), 404

        response_data = {
                "id": str(scenario.id),
                "scenarioName": scenario.scenarioName,
                "scenarioDescription": scenario.scenarionDescription,
                "isPublish": scenario.isPublish,
                "user_id": str(scenario.user_id),
                "createdAt": scenario.createdAt.isoformat(),
                "updatedAt": scenario.updatedAt.isoformat(),
            }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
   
   
    
def get_scenarios(id):
    try:
        # Query scenarios based on the provided ID
        scenarios = Scenario.query.filter(Scenario.user_id == id).all()

        response_data = []

        for scenario in scenarios:
            scenario_data = {
                "id": str(scenario.id),
                "scenarioName": scenario.scenarioName,
                "scenarioDescription": scenario.scenarionDescription,
                "isPublish": scenario.isPublish,
                "user_id": str(scenario.user_id),
                "createdAt": scenario.createdAt.isoformat(),
                "updatedAt": scenario.updatedAt.isoformat(),
            }
            response_data.append(scenario_data)

        return jsonify(response_data), 200

    except NoResultFound:
        return jsonify({'error': 'Scenario not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500