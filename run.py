from app import app, db  # Import the Flask app instance and SQLAlchemy instance

#Create the tables in your database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True,port=8081)