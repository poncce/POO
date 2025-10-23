class Persona:
    def __init__(self, nombre, licencia, tipo_preferido=None, preferencia=None):
        self.nombre = nombre
        self.licencia = licencia
        self.tipo_preferido = tipo_preferido      
        self.preferencia = preferencia            

class Auto:
    def __init__(self, marca, modelo, puertas):
        self.marca = marca
        self.modelo = modelo
        self.puertas = puertas
        self.conductor = None

    def asignar_conductor(self, persona):
        if not persona.licencia:
            print(f"{persona.nombre} no tiene licencia para conducir")
            return
        if persona.tipo_preferido != "Auto":
            print(f"{persona.nombre} no quiere conducir un auto")
            return
        if persona.preferencia != self.puertas:
            print(f"{persona.nombre} no quiere un auto con {self.puertas} puertas")
            return
        self.conductor = persona
        print(f"{persona.nombre} ahora conduce el auto {self.marca} {self.modelo}")

    def mostrar_info(self):
        cond = self.conductor.nombre if self.conductor else "Sin conductor"
        print(f"Auto {self.marca} {self.modelo}, Puertas: {self.puertas}, Conductor: {cond}")

class Moto:
    def __init__(self, marca, modelo, cilindrada):
        self.marca = marca
        self.modelo = modelo
        self.cilindrada = cilindrada
        self.conductor = None

    def asignar_conductor(self, persona):
        if not persona.licencia:
            print(f"{persona.nombre} no tiene licencia para conducir")
            return
        if persona.tipo_preferido != "Moto":
            print(f"{persona.nombre} no quiere conducir una moto")
            return
        if persona.preferencia != self.cilindrada:
            print(f"{persona.nombre} no quiere una moto de {self.cilindrada} cilindros")
            return
        self.conductor = persona
        print(f"{persona.nombre} ahora conduce la moto {self.marca} {self.modelo}")

    def mostrar_info(self):
        cond = self.conductor.nombre if self.conductor else "Sin conductor"
        print(f"Moto {self.marca} {self.modelo}, Cilindrada: {self.cilindrada}, Conductor: {cond}")

p1 = Persona("Pepe", True, "Auto", 4)
p2 = Persona("Ana", True, "Moto", 500)
p3 = Persona("Luis", False, "Auto", 2)

a1 = Auto("Toyota", "Corolla", 4)
a2 = Auto("Ford", "Mustang", 2)
m1 = Moto("Honda", "CB500", 500)

a1.asignar_conductor(p1)  
a2.asignar_conductor(p3) 
m1.asignar_conductor(p2) 

