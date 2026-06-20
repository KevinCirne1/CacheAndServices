import os
#rom datetime import timedelta # 
from dotenv import load_dotenv

load_dotenv() 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- Configurações do JWT --
    #JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    #JWT_TOKEN_LOCATION = ['headers']
    #JWT_HEADER_NAME = 'Authorization'
    #JWT_HEADER_TYPE = 'Bearer'
    
    # AUMENTA O TEMPO DE VIDA DO TOKEN DE ACESSO PARA 1 HORA
    #JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
