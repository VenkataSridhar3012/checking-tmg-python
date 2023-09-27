from datetime import timedelta

class Config:
    # Other app configurations here
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

# Configuration settings for Flask app
SECRET_KEY = 'secret_t_m_g'  # Replace with a strong secret key
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:spotdev@89.246.174.249:5432/postgres'  # Replace with your PostgreSQL database URL
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for SQLAlchemy

# Other configurations
DEBUG = True  # Set to False in production
