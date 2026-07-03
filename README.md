# 📚 Sistema de Control de Asistencia con Reconocimiento Facial

Sistema automatizado de control de asistencia basado en reconocimiento facial para instituciones educativas.

## 🎯 Características

- ✅ Reconocimiento facial con DeepFace (FaceNet)
- ✅ Registro de estudiantes con cámara
- ✅ Registro automático de asistencia
- ✅ Sistema experto con reglas de producción (Presente, Tarde, Muy tarde, Ausente)
- ✅ Base de datos SQLite
- ✅ Scripts para gestión de estudiantes y clases

## 🛠️ Tecnologías

- Python 3.11
- DeepFace (FaceNet)
- OpenCV
- SQLite
- Flask (próximamente)

## 📋 Requisitos

``` bash
pip install -r requirements.txt
```

# 🚀 Uso
## 1. Inicializar base de datos

``` bash
cd src/web 
python app.py
```

## 2. Registrar estudiantes

``` bash
python registrar_estudiante.py
```
## 3. Crear una clase

``` bash
python crear_clase.py
```
## 4. Tomar asistencia
``` bash
python reconocer_asistencia.py
```

# 📁 Estructura del Proyecto
``` text
📁 proyecto/
├── 📁 datos/               # Base de datos y fotos
├── 📁 src/                 # Código fuente
│   ├── 📁 core/           # Lógica de IA y sistema experto
│   └── 📁 web/            # Aplicación web (próximamente)
├── 📁 scripts/             # Scripts de utilidad
├── requirements.txt        # Dependencias
└── README.md
```

## 📊 Reglas del Sistema Experto

|Regla |	Condición |	Estado |
|-------|--------|-------|
|R1	| Llegada ≤ 5 min |	Presente |
|R2 |	5 < llegada ≤ 15 min |	Tarde |
|R3 |	15 < llegada ≤ 30 min |	Muy tarde |
|R4 |	Llegada > 30 min |	Ausente |

# 👨‍💻 Autor
Amilcarqs

## 📝 Licencia
MIT


