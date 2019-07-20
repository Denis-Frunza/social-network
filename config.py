import os


class BaseConfig:
    """Base configuration"""
    DEBUG = True
    PORT = 8000
    HOST = '0.0.0.0'
    SECRET_KEY = 'generated_string'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    pass

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True