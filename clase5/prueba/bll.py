from dal import * 
class Turbina:
    def __init__(self, id, nombre, potencia_maxima):
        self.__id = id
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
        except Exception as e:
            print(f"error al calcular la eficiencia {e}")
