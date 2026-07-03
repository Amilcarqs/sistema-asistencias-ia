# src/web/app.py
from flask import Flask
from models import db
import os

# Obtener la ruta base del proyecto (sube 3 niveles desde src/web)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATOS_DIR = os.path.join(BASE_DIR, "datos")
DB_PATH = os.path.join(DATOS_DIR, "asistencias.db")

# Crear carpeta datos si no existe
if not os.path.exists(DATOS_DIR):
    os.makedirs(DATOS_DIR)
    print(f"📁 Carpeta creada: {DATOS_DIR}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-para-sistema-asistencias'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("=" * 50)
        print("✅ Base de datos creada/verificada")
        print(f"📁 Ruta: {DB_PATH}")
        print("📋 Tablas: estudiantes, clases, asistencias")
        print("=" * 50)