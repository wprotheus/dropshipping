# Importações necessárias
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from local_settings import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Configuração Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dropshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate = Migrate(app, db)

# Importação dos Endpoints
from shopping.views import *
from shopping.models import *
