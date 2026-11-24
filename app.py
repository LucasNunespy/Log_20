from flask import Flask, render_template, redirect, url_for, request
from config import Config
from database.db import db
from routes.auth_routes import auth
from routes.motoristas_routes import motoristas

from models.motoristas import Motorista
from models.mapas import Mapa
from models.entregas import Entrega
from routes.importacao_routes import importacao
from routes.operacao_routes import operacao
from models.jornadas_2art import Jornada2ART, Jornada2ARTMapa
from routes.jornadas_2art_routes import jornadas_2art

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(motoristas)
app.register_blueprint(importacao)
app.register_blueprint(operacao)
app.register_blueprint(jornadas_2art)


@app.route("/")
def home():
    return redirect(url_for("auth.login"))


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)