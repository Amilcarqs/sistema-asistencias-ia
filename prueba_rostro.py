# prueba_rostro.py
from deepface import DeepFace
import os

print("=" * 50)
print("🧠 PRUEBA DE RECONOCIMIENTO CON DEEPFACE")
print("=" * 50)

# Ruta de la imagen
ruta_imagen = r"C:\Users\AMILCAR\Downloads\estudiante.jpg"

# Verificar que la imagen existe
if not os.path.exists(ruta_imagen):
    print(f"❌ No se encontró la imagen en: {ruta_imagen}")
    print("Por favor, verifica la ruta.")
    exit()

print(f"📷 Imagen: {ruta_imagen}")

# Detectar rostro en la imagen
print("\n🔍 Detectando rostro...")

try:
    resultado = DeepFace.analyze(
        img_path=ruta_imagen,
        actions=['age', 'gender', 'emotion'],
        enforce_detection=True
    )
    
    if resultado:
        datos = resultado[0]
        
        print("\n✅ ROSTRO DETECTADO")
        print("=" * 40)
        print(f"📊 Edad estimada: {datos['age']} años")
        
        # El género viene como diccionario con 'Dominant' y 'Woman'/'Man'
        genero = datos['gender']
        print(f"⚤ Género: {genero}")
        # Extraer el género dominante
        if isinstance(genero, dict):
            genero_dominante = genero.get('Dominant', 'Desconocido')
            print(f"⚤ Género dominante: {genero_dominante}")
        
        # Emociones
        emociones = datos['emotion']
        emocion_dominante = max(emociones, key=emociones.get)
        print(f"😊 Emoción dominante: {emocion_dominante} ({emociones[emocion_dominante]:.2f}%)")
        print("=" * 40)
        
        print("\n📋 Detalle de emociones:")
        for emocion, porcentaje in emociones.items():
            print(f"   {emocion}: {porcentaje:.2f}%")
            
    else:
        print("❌ No se detectó ningún rostro.")
        
except Exception as e:
    print(f"❌ Error: {e}")