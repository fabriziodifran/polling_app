
class Config(object):
    DEV_MODE = True
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@database:5432/pollingdb"
    REGISTER_USER = {'USERNAME': 'user', 'PASSWORD': 'user1234'}
    ADMIN_USER = {'USERNAME': 'admin', 'PASSWORD': 'admin1234'}