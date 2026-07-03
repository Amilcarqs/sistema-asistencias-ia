# src/core/sistema_experto.py
from datetime import datetime, timedelta

class SistemaExperto:
    def __init__(self):
        self.reglas = []
        self.hechos = {}
        self._cargar_reglas()
    
    def _cargar_reglas(self):
        """Base de conocimiento: Reglas de producción para asistencia"""
        self.reglas = [
            {
                'id': 'R1',
                'condicion': lambda hechos: hechos.get('hora_llegada') <= hechos.get('hora_limite_presente'),
                'accion': 'estado_presente',
                'mensaje': 'PRESENTE',
                'estado': 'Presente'
            },
            {
                'id': 'R2',
                'condicion': lambda hechos: (
                    hechos.get('hora_llegada') > hechos.get('hora_limite_presente') and
                    hechos.get('hora_llegada') <= hechos.get('hora_limite_tarde')
                ),
                'accion': 'estado_tarde',
                'mensaje': 'TARDE',
                'estado': 'Tarde'
            },
            {
                'id': 'R3',
                'condicion': lambda hechos: (
                    hechos.get('hora_llegada') > hechos.get('hora_limite_tarde') and
                    hechos.get('hora_llegada') <= hechos.get('hora_limite_muy_tarde')
                ),
                'accion': 'estado_muy_tarde',
                'mensaje': 'MUY TARDE',
                'estado': 'Muy tarde'
            },
            {
                'id': 'R4',
                'condicion': lambda hechos: hechos.get('hora_llegada') > hechos.get('hora_limite_muy_tarde'),
                'accion': 'estado_ausente',
                'mensaje': 'AUSENTE (después de los 30 min)',
                'estado': 'Ausente'
            }
        ]
    
    def ejecutar(self, hechos_entrada):
        """
        Motor de inferencia: Evalúa las reglas con los hechos dados
        Retorna: dict con el estado y mensaje
        """
        self.hechos = hechos_entrada
        
        for regla in self.reglas:
            try:
                if regla['condicion'](self.hechos):
                    return {
                        'regla': regla['id'],
                        'estado': regla['estado'],
                        'mensaje': regla['mensaje'],
                        'accion': regla['accion']
                    }
            except Exception as e:
                print(f" Error evaluando regla {regla['id']}: {e}")
                continue
        
        # Si no se cumple ninguna regla (fallback)
        return {
            'regla': 'R0',
            'estado': 'Desconocido',
            'mensaje': 'No se pudo determinar el estado',
            'accion': 'estado_desconocido'
        }
    
    def determinar_estado(self, hora_actual, hora_inicio_clase):
        """
        metodo principal para determinar el estado de asistencia
        hora_actual: datetime.time
        hora_inicio_clase: datetime.time
        """
        # Crear objetos datetime para hacer cálculos
        hoy = datetime.now().date()
        dt_actual = datetime.combine(hoy, hora_actual)
        dt_inicio = datetime.combine(hoy, hora_inicio_clase)
        
        # Calcular diferencias en minutos
        minutos = (dt_actual - dt_inicio).total_seconds() / 60.0
        
        # Definir límites (en minutos desde el inicio)
        limite_presente = 5      # 5 minutos de tolerancia
        limite_tarde = 15        # 15 minutos
        limite_muy_tarde = 30    # 30 minutos
        
        # Preparar hechos para el motor
        hechos = {
            'hora_llegada': minutos,
            'hora_limite_presente': limite_presente,
            'hora_limite_tarde': limite_tarde,
            'hora_limite_muy_tarde': limite_muy_tarde,
            'hora_inicio_clase': hora_inicio_clase.strftime('%H:%M'),
            'hora_actual': hora_actual.strftime('%H:%M'),
            'minutos_desde_inicio': minutos
        }
        
        # Ejecutar motor de inferencia
        resultado = self.ejecutar(hechos)
        
        # Agregar información adicional al resultado
        resultado['minutos_desde_inicio'] = minutos
        resultado['hora_inicio'] = hora_inicio_clase.strftime('%H:%M')
        resultado['hora_llegada'] = hora_actual.strftime('%H:%M')
        
        return resultado
    
    def get_reglas_info(self):
        """Retorna información de las reglas para mostrar en la interfaz"""
        info = []
        for regla in self.reglas:
            info.append({
                'id': regla['id'],
                'estado': regla['estado'],
                'mensaje': regla['mensaje']
            })
        return info