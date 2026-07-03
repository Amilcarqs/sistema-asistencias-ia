# verificar.py
print("=" * 50)
print("🔍 VERIFICACIÓN DE DEPENDENCIAS")
print("=" * 50)

# Verificar DeepFace
try:
    from deepface import DeepFace
    print("✅ DeepFace instalado")
except Exception as e:
    print("❌ DeepFace:", e)

# Verificar Flask
try:
    import flask
    print("✅ Flask instalado")
except Exception as e:
    print("❌ Flask:", e)

# Verificar OpenCV
try:
    import cv2
    print("✅ OpenCV instalado")
except Exception as e:
    print("❌ OpenCV:", e)

# Verificar NumPy
try:
    import numpy as np
    print("✅ NumPy instalado")
except Exception as e:
    print("❌ NumPy:", e)

print("=" * 50)
print("✅ Todo listo para comenzar el proyecto")