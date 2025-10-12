class Persona:
    def __init__(self, nombre, edad, dni, licencia_conducir: bool, tipo_preferido=None, caracteristica_preferida=None):
        self.nombre = nombre
        self.edad = edad
        self.licencia_conducir = licencia_conducir
        self.__dni = dni
        self.tipo_preferido = tipo_preferido  
        self.caracteristica_preferida = caracteristica_preferida  

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Edad: {self.edad}, DNI: {self.__dni}, Licencia: {self.licencia_conducir}")

    def puede_conducir(self):
        if self.licencia_conducir:
            print("Puede conducir")
        else:
            print("No puede conducir")


class Vehiculo:
    def __init__(self, marca, modelo, anio):
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.conductor = None

    def asignar_conductor(self, persona: Persona):
        if not persona.licencia_conducir:
            print(f"{persona.nombre} no tiene licencia para conducir.")
            return False

        if self.__class__.__name__ != persona.tipo_preferido:
            print(f"{persona.nombre} no quiere conducir un {self.__class__.__name__}.")
            return False

        if hasattr(self, 'cantidad_puertas'):
            if persona.caracteristica_preferida != self.cantidad_puertas:
                print(f"{persona.nombre} no quiere un auto con {self.cantidad_puertas} puertas.")
                return False
        elif hasattr(self, 'cilindrada'):
            if persona.caracteristica_preferida != self.cilindrada:
                print(f"{persona.nombre} no quiere una moto de {self.cilindrada} cc.")
                return False

        self.conductor = persona
        print(f"{persona.nombre} ahora conduce el {self.__class__.__name__}.")
        return True

    def mostrar_info(self):
        cond = self.conductor.nombre if self.conductor else "Sin conductor"
        print(f"Marca: {self.marca}, Modelo: {self.modelo}, Año: {self.anio}, Conductor: {cond}")


class Auto(Vehiculo):
    def __init__(self, marca, modelo, anio, cantidad_puertas):
        super().__init__(marca, modelo, anio)
        self.cantidad_puertas = cantidad_puertas

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Cantidad de puertas: {self.cantidad_puertas}")


class Moto(Vehiculo):
    def __init__(self, marca, modelo, anio, cilindrada):
        super().__init__(marca, modelo, anio)
        self.cilindrada = cilindrada

    def mostrar_info(self):
        super().mostrar_info()
        print(f"Cilindrada: {self.cilindrada} cc")


persona1 = Persona("Pepe", 38, 11111111, True, tipo_preferido="Auto", caracteristica_preferida=4)
persona2 = Persona("Ana", 25, 22222222, True, tipo_preferido="Moto", caracteristica_preferida=500)
persona3 = Persona("Luis", 30, 33333333, False, tipo_preferido="Auto", caracteristica_preferida=2)

auto1 = Auto("Toyota", "Corolla", 2023, 4)
auto2 = Auto("Ford", "Mustang", 2022, 2)
moto1 = Moto("Honda", "CB500", 2022, 500)
moto2 = Moto("Yamaha", "R1", 2023, 1000)

auto1.asignar_conductor(persona1)  # Pepe quiere auto con 4 puertas -> OK
auto2.asignar_conductor(persona3)  # Luis no tiene licencia -> NO
moto1.asignar_conductor(persona2)  # Ana quiere moto 500cc -> OK
moto2.asignar_conductor(persona2)  # Ana no quiere moto 1000cc -> NO

auto1.mostrar_info()
auto2.mostrar_info()
moto1.mostrar_info()
moto2.mostrar_info()
