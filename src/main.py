import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.programacao import *
from src.routes.user import user_bp
from src.routes.categorias import categorias_bp
from src.routes.estilos import estilos_bp
from src.routes.musicas import musicas_bp
from src.routes.locutores import locutores_bp
from src.routes.emissoras import emissoras_bp
from src.routes.locutor_emissora import locutor_emissora_bp
from src.routes.banco_locucoes import banco_locucoes_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(categorias_bp, url_prefix='/api')
app.register_blueprint(estilos_bp, url_prefix='/api')
app.register_blueprint(musicas_bp, url_prefix='/api')
app.register_blueprint(locutores_bp, url_prefix='/api')
app.register_blueprint(emissoras_bp, url_prefix='/api')
app.register_blueprint(locutor_emissora_bp, url_prefix='/api')
app.register_blueprint(banco_locucoes_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
