# verificar_bd.py
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src", "web"))

from app import app
from models import Estudiante, db

with app.app_context():
    estudiantes = Estudiante.query.all()
    print("=" * 40)
    print("📋 ESTUDIANTES EN BASE DE DATOS")
    print("=" * 40)
    
    if estudiantes:
        for e in estudiantes:
            print(f"ID: {e.id} | Nombre: {e.nombre} | Apellido: {e.apellido} | Completo: {e.nombre_completo}")
    else:
        print("❌ No hay estudiantes en la BD")
    
    print("=" * 40)
    print(f"Total: {len(estudiantes)} estudiantes")