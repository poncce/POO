from dal import TurbinaDAL, RegistroDAL

class Turbina:
    def __init__(self, id_turbina, nombre, potencia_maxima):
        self.id = id_turbina
        self.nombre = nombre
        self.potencia_maxima = potencia_maxima
    
    def eficiencia(self):
        return 1

class TurbinaPelton(Turbina):
    def __init__(self, id_turbina, nombre, potencia_maxima):
        super().__init__(id_turbina, nombre, potencia_maxima)
        self.potencia_actual = 0
    
    def calcular_potencia_actual(self):
        try:
            registro_dal = RegistroDAL()
            registros = registro_dal.obtener_registros_por_turbina(self.id)
            if registros:
                total = sum([r[0] for r in registros])
                self.potencia_actual = total / len(registros)
            else:
                self.potencia_actual = 0
        except Exception as e:
            print(f"Error calculando potencia actual: {e}")
            self.potencia_actual = 0
    
    def eficiencia(self):
        try:
            if self.potencia_maxima == 0:
                return 0
            return self.potencia_actual / self.potencia_maxima
        except:
            return 0

class HidroelectricaBLL:
    def __init__(self):
        self.turbina_dal = TurbinaDAL()
        self.registro_dal = RegistroDAL()
    
    def calcular_porcentaje_consumido(self):
        try:
            registros = self.registro_dal.obtener_todos_registros()
            
            if not registros:
                return 0.0
            
            energia_generada_total = 0
            energia_consumida_total = 0
            
            for registro in registros:
                energia_generada_total += registro[2]
                energia_consumida_total += registro[3]
            
            if energia_generada_total == 0:
                return 0.0
            
            porcentaje = (energia_consumida_total / energia_generada_total) * 100
            return round(porcentaje, 2)
        except Exception as e:
            print(f"Error al calcular porcentaje consumido: {e}")
            return 0.0
    
    def turbina_mas_eficiente(self):
        try:
            turbinas_data = self.turbina_dal.obtener_todas_turbinas()
            registros = self.registro_dal.obtener_todos_registros()
            
            if not turbinas_data or not registros:
                return None
            
            eficiencias = {}
            
            for turbina_data in turbinas_data:
                id_turbina = turbina_data[0]
                nombre = turbina_data[1]
                potencia_maxima = turbina_data[2]
                
                registros_turbina = [r for r in registros if r[1] == id_turbina]
                
                if registros_turbina:
                    energia_total = sum([r[2] for r in registros_turbina])
                    cantidad_registros = len(registros_turbina)
                    
                    if potencia_maxima > 0 and cantidad_registros > 0:
                        eficiencia = energia_total / (potencia_maxima * cantidad_registros)
                        eficiencias[nombre] = eficiencia
            
            if eficiencias:
                turbina_eficiente = max(eficiencias, key=eficiencias.get)
                return turbina_eficiente
            else:
                return None
        except Exception as e:
            print(f"Error al calcular turbina más eficiente: {e}")
            return None