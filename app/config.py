# Configuration settings for Flask app
SECRET_KEY = 'secret_t_m_g'  # Replace with a strong secret key
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Sra%401901@localhost/test'  # Replace with your PostgreSQL database URL
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for SQLAlchemy

# Other configurations
DEBUG = True  # Set to False in production
