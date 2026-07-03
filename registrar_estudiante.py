# registrar_estudiante.py
import cv2
import os
import sys

# Agregar ruta base para importar modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src", "web"))

from models import Estudiante, db
from app import app
from deepface import DeepFace

print("=" * 50)
print("📝 REGISTRO DE ESTUDIANTE CON BASE DE DATOS")
print("=" * 50)

nombre = input("👤 Nombre: ").strip()
apellido = input("👤 Apellido: ").strip()

if not nombre or not apellido:
    print("❌ Nombre y apellido son obligatorios")
    exit()

nombre_completo = f"{nombre} {apellido}"
print(f"\n📷 Colócate frente a la cámara para {nombre_completo}")
print("   Presiona ESPACIO para capturar, ESC para cancelar")

cap = cv2.VideoCapture(0)
captura_exitosa = False

with app.app_context():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.putText(frame, f"Registrando: {nombre_completo}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Presiona ESPACIO para capturar", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Registro de Estudiante", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # ESPACIO
            temp_path = "datos/temporal/temp.jpg"
            cv2.imwrite(temp_path, frame)
            
            try:
                # Verificar rostro con DeepFace
                resultado = DeepFace.analyze(img_path=temp_path, actions=['age'], enforce_detection=True)
                
                if resultado:
                    # Guardar foto
                    carpeta = os.path.join(BASE_DIR, "datos", "estudiantes", nombre_completo)
                    os.makedirs(carpeta, exist_ok=True)
                    ruta_foto = os.path.join(carpeta, "foto.jpg")
                    cv2.imwrite(ruta_foto, frame)
                    
                    # Guardar en base de datos
                    estudiante = Estudiante(
                        nombre=nombre,
                        apellido=apellido,
                        foto_ruta=f"static/estudiantes/{nombre_completo}/foto.jpg"
                    )
                    db.session.add(estudiante)
                    db.session.commit()
                    
                    print(f"\n✅ {nombre_completo} registrado correctamente!")
                    print(f"📁 ID en BD: {estudiante.id}")
                    captura_exitosa = True
                    break
                else:
                    print("❌ No se detectó rostro. Intenta de nuevo.")
                    
            except Exception as e:
                print(f"❌ Error en DeepFace: {e}")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        elif key == 27:  # ESC
            print("\n❌ Registro cancelado")
            break
    
    cap.release()
    cv2.destroyAllWindows()

if captura_exitosa:
    print("\n📋 Resumen:")
    print(f"   Estudiante: {nombre_completo}")
    print(f"   Carpeta: datos/estudiantes/{nombre_completo}/")