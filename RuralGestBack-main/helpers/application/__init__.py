from flask import Flask
from flask_restful import Api
from config import Config
from helpers.database import db, ma, bcrypt
from flask_caching import Cache 
from flask_cors import CORS 
import os

app = Flask(__name__)
app.config.from_object(Config)


CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://10.112.136.42:3000"])

# Configuração do Redis (Pega do .env ou usa padrão local)
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)

# Configura o Cache
cache_config = {
    "DEBUG": True,
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300, 
    "CACHE_REDIS_HOST": redis_host,
    "CACHE_REDIS_PORT": redis_port
}

# Inicializa as restantes extensões
db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
cache = Cache(app, config=cache_config) 

api = Api(app)