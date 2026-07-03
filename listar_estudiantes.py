# listar_estudiantes.py
import os

carpeta = "datos/estudiantes"

if os.path.exists(carpeta):
    estudiantes = os.listdir(carpeta)
    print("=" * 50)
    print("📋 LISTA DE ESTUDIANTES REGISTRADOS")
    print("=" * 50)
    
    if estudiantes:
        for i, nombre in enumerate(estudiantes, 1):
            ruta_foto = os.path.join(carpeta, nombre, "foto.jpg")
            if os.path.exists(ruta_foto):
                print(f"{i}. {nombre}")
        print(f"\nTotal: {len(estudiantes)} estudiante(s)")
    else:
        print("No hay estudiantes registrados")
else:
    print("❌ La carpeta 'datos/estudiantes' no existe")