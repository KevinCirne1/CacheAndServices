from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase

from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
bcrypt = Bcrypt()