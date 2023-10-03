from app import app, db ,config_data # Import the Flask app instance and SQLAlchemy instance
import os


os.environ['APP_ENV'] = 'dev'
BASE_URL = config_data['BASE_URL'].replace('http://', '').replace('https://', '')
print(BASE_URL)
# Create the tables in your database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8081, debug=True)