class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Gma12101956@localhost/library_db'
    DEBUG = True

class ProductionConfig:
    pass

class TestingConfig:
    pass
 