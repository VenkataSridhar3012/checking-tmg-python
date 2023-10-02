from app import app, db ,config_data # Import the Flask app instance and SQLAlchemy instance
import os


os.environ['APP_ENV'] = 'dev'
baseUrl = config_data['base_url'].replace('http://', '').replace('https://', '')
print(baseUrl)
# Create the tables in your database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
   app.run(host=baseUrl, port=8081, debug=True)