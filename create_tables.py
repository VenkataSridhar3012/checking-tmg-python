from app import app, db  # Import the Flask app instance and SQLAlchemy instance

# Create the "documents" table in your database
with app.app_context():
    db.create_all()

print("The 'documents' table has been created.")