# crear_clase.py
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src", "web"))

from models import Clase, db
from app import app

print("=" * 50)
print("📅 CREAR NUEVA CLASE")
print("=" * 50)

with app.app_context():
    fecha_str = input("Fecha (YYYY-MM-DD): ")
    hora_inicio_str = input("Hora inicio (HH:MM): ")
    hora_fin_str = input("Hora fin (HH:MM): ")
    observaciones = input("Observaciones (opcional): ")
    
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
        
        clase = Clase(
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            observaciones=observaciones
        )
        db.session.add(clase)
        db.session.commit()
        
        print(f"\n✅ Clase creada: {clase.descripcion}")
        print(f"📋 ID: {clase.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")