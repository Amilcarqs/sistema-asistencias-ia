# reconocer_asistencia.py
from deepface import DeepFace
import cv2
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "src", "web"))

from models import Estudiante, Clase, Asistencia, db
from app import app

print("=" * 50)
print("SISTEMA DE RECONOCIMIENTO Y ASISTENCIA CON BD")
print("=" * 50)

with app.app_context():
    # 1. Seleccionar clase
    clases = Clase.query.order_by(Clase.fecha.desc()).all()

    if not clases:
        print("No hay clases registradas. Crea una clase primero.")
        exit()

    print("\nClases disponibles:")
    for i, clase in enumerate(clases, 1):
        print(f"{i}. {clase.descripcion}")

    try:
        opcion = int(input("\nSelecciona una clase (numero): "))
        clase_seleccionada = clases[opcion - 1]
    except:
        print("Opcion invalida")
        exit()

    # 2. Cargar estudiantes desde BD
    estudiantes = Estudiante.query.all()

    if not estudiantes:
        print("No hay estudiantes registrados.")
        exit()

    print(f"\n{len(estudiantes)} estudiante(s) cargados desde BD")
    print(f"Clase: {clase_seleccionada.descripcion}")

    # 3. Cargar estudiantes en memoria para reconocimiento
    estudiantes_dict = {}
    for est in estudiantes:
        ruta_foto = os.path.join(BASE_DIR, "datos", "estudiantes", est.nombre_completo, "foto.jpg")
        if os.path.exists(ruta_foto):
            estudiantes_dict[est.nombre_completo] = ruta_foto
            print(f"Cargado: {est.nombre_completo}")

    if not estudiantes_dict:
        print("No hay fotos de estudiantes en la carpeta datos/estudiantes")
        exit()

    print("Presiona ESPACIO para reconocer, ESC para salir")

    cap = cv2.VideoCapture(0)
    registrados_hoy = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Reconocimiento de Asistencia", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # ESPACIO
            temp_path = "datos/temporal/asis_temp.jpg"
            cv2.imwrite(temp_path, frame)

            print("\nReconociendo...")

            nombre_encontrado = None
            confianza_max = 0

            for nombre, ruta_foto in estudiantes_dict.items():
                try:
                    resultado = DeepFace.verify(
                        img1_path=temp_path,
                        img2_path=ruta_foto,
                        enforce_detection=True,
                        model_name='Facenet'
                    )

                    if resultado['verified']:
                        distancia = resultado['distance']
                        confianza = 1 - distancia

                        if confianza > confianza_max:
                            confianza_max = confianza
                            nombre_encontrado = nombre
                            print(f"   Coincidencia: {nombre} (confianza: {confianza:.2f})")

                except Exception as e:
                    continue

            if nombre_encontrado:
                # Buscar estudiante en BD (busqueda flexible)
                estudiante = None
                
                # 1. Buscar por nombre_completo
                estudiante = Estudiante.query.filter_by(nombre_completo=nombre_encontrado).first()
                
                # 2. Si no funciona, buscar por nombre y apellido por separado
                if not estudiante:
                    partes = nombre_encontrado.split(' ')
                    if len(partes) >= 2:
                        nombre_buscar = partes[0]
                        apellido_buscar = ' '.join(partes[1:])
                        estudiante = Estudiante.query.filter_by(nombre=nombre_buscar, apellido=apellido_buscar).first()
                
                # 3. Si aun no funciona, buscar solo por nombre
                if not estudiante and len(partes) >= 1:
                    estudiante = Estudiante.query.filter_by(nombre=partes[0]).first()

                if estudiante:
                    print(f"Encontrado en BD: {estudiante.nombre} {estudiante.apellido}")
                    
                    # Verificar si ya tiene asistencia en esta clase
                    existe = Asistencia.query.filter_by(
                        estudiante_id=estudiante.id,
                        clase_id=clase_seleccionada.id
                    ).first()

                    if existe:
                        print(f"{estudiante.nombre_completo} ya esta registrado en esta clase")
                    else:
                        # Registrar asistencia
                        asistencia = Asistencia(
                            estudiante_id=estudiante.id,
                            clase_id=clase_seleccionada.id,
                            estado="Presente"
                        )
                        db.session.add(asistencia)
                        db.session.commit()
                        registrados_hoy.append(estudiante.nombre_completo)

                        print(f"{estudiante.nombre_completo} registrado! (confianza: {confianza_max:.2f})")
                        print("Asistencia registrada en BD")

                        cv2.putText(frame, f"{estudiante.nombre_completo}", (10, 50),
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                        cv2.imshow("Reconocimiento de Asistencia", frame)
                        cv2.waitKey(1000)
                else:
                    print(f"{nombre_encontrado} no encontrado en BD")
                    # Mostrar estudiantes disponibles para debug
                    print("   Estudiantes en BD:")
                    for e in Estudiante.query.all():
                        print(f"   - {e.nombre_completo}")
            else:
                print("No se reconocio a ningun estudiante")
                cv2.putText(frame, "No reconocido", (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.imshow("Reconocimiento de Asistencia", frame)
                cv2.waitKey(1000)

            if os.path.exists(temp_path):
                os.remove(temp_path)

        elif key == 27:  # Esc para salr
            break

    cap.release()
    cv2.destroyAllWindows()

    # Mostrar resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE ASISTENCIA")
    print("=" * 50)
    print(f"Clase: {clase_seleccionada.descripcion}")
    print(f"Total estudiantes: {len(estudiantes)}")
    print(f"Registrados: {len(registrados_hoy)}")
    print(f"Faltantes: {len(estudiantes) - len(registrados_hoy)}")
    print("=" * 50)