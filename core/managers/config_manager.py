import os
import secrets


class ConfigManager:
    def __init__(self, app):
        self.app = app

    def load_config(self, config_name="development"):
<<<<<<< HEAD
        # If config_name is not provided, use the environment variable FLASK_ENV
        if config_name is None:
            config_name = os.getenv("FLASK_ENV", "development")

        # Load configuration
=======
        if config_name is None:
            config_name = os.getenv("FLASK_ENV", "development")

>>>>>>> origin/trunk
        if config_name == "testing":
            self.app.config.from_object(TestingConfig)
        elif config_name == "production":
            self.app.config.from_object(ProductionConfig)
        else:
            self.app.config.from_object(DevelopmentConfig)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_bytes())
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER', 'default_user')}:"
        f"{os.getenv('MARIADB_PASSWORD', 'default_password')}@"
        f"{os.getenv('MARIADB_HOSTNAME', 'localhost')}:"
        f"{os.getenv('MARIADB_PORT', '3306')}/"
        f"{os.getenv('MARIADB_DATABASE', 'default_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = "Europe/Madrid"
    TEMPLATES_AUTO_RELOAD = True
    UPLOAD_FOLDER = "uploads"
<<<<<<< HEAD
=======
    
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ["true", "t", "1"]
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@midominio.com")
    
    # AÑADIDO PARA DEBUGGING
    MAIL_DEBUG = os.getenv("MAIL_DEBUG", "False").lower() in ["true", "t", "1"]
>>>>>>> origin/trunk


class DevelopmentConfig(Config):
    DEBUG = True
<<<<<<< HEAD
=======
    MAIL_DEBUG = True
>>>>>>> origin/trunk


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER', 'default_user')}:"
        f"{os.getenv('MARIADB_PASSWORD', 'default_password')}@"
        f"{os.getenv('MARIADB_HOSTNAME', 'localhost')}:"
        f"{os.getenv('MARIADB_PORT', '3306')}/"
        f"{os.getenv('MARIADB_TEST_DATABASE', 'default_db')}"
    )
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
<<<<<<< HEAD
=======
    MAIL_DEBUG = False
>>>>>>> origin/trunk
