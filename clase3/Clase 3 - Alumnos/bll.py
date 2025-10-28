from dal import ClienteDAL, EmpleadoDAL, PlanDAL

class Persona:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Correo: {self.correo}, Planes de entrenamiento"


class Cliente(Persona):
    def __init__(self, nombre, correo, id_cliente=None):
        super().__init__(nombre, correo)
        self.id_cliente = id_cliente
        self.planes = []

    def mostrar_info(self):
        planes_texto = ', '.join([p.nombre for p in self.planes]) if self.planes else "Sin planes"
        return f"[Cliente {self.id_cliente or '-'}] {super().mostrar_info()} | Planes: {planes_texto}"


class ClienteService:
    def __init__(self):
        self.dal = ClienteDAL()
        self.plan_dal = PlanDAL()

    def agregar_cliente(self, cliente: Cliente):
        if not cliente.nombre or not cliente.correo:
            raise ValueError("El nombre y correo son obligatorios.")
        self.dal.insertar_cliente(cliente.nombre, cliente.correo)

    def obtener_clientes(self):
        registros = self.dal.listar_clientes()
        clientes = [Cliente(id_cliente=r[0], nombre=r[1], correo=r[2]) for r in registros]
        # cargar planes asociados
        for c in clientes:
            planes = self.plan_dal.obtener_planes_de_cliente(c.id_cliente)
            c.planes = [PlanEntrenamiento(id_plan=p[0], nombre=p[1], descripcion=p[2], duracion_semanas=p[3]) for p in planes]
        return clientes

    def eliminar_cliente(self, cliente_id):
        self.dal.eliminar_cliente(cliente_id)



class Empleado(Persona):
    def __init__(self, nombre, correo, puesto, salario, id_empleado=None):
        super().__init__(nombre, correo)
        self.puesto = puesto
        self.salario = salario
        self.id_empleado = id_empleado

    def calcular_bono(self):
        puesto_lower = self.puesto.lower()
        if "gerente" in puesto_lower:
            return self.salario * 0.20
        elif "supervisor" in puesto_lower:
            return self.salario * 0.15
        return self.salario * 0.10

    def mostrar_info(self):
        bono = self.calcular_bono()
        return f"[Empleado {self.id_empleado}] {super().mostrar_info()} | Puesto: {self.puesto} | Salario: {self.salario:.2f} | Bono: {bono:.2f}"


class EmpleadoService:
    def __init__(self):
        self.dal = EmpleadoDAL()

    def agregar_empleado(self, empleado: Empleado):
        if not empleado.nombre or not empleado.correo or not empleado.puesto:
            raise ValueError("El nombre, correo y puesto son obligatorios.")
        self.dal.insertar_empleado(empleado.nombre, empleado.correo, empleado.puesto, empleado.salario)

    def obtener_empleados(self):
        registros = self.dal.listar_empleados()
        return [Empleado(id_empleado=r[0], nombre=r[1], correo=r[2], puesto=r[3], salario=r[4]) for r in registros]

    def eliminar_empleado(self, empleado_id):
        self.dal.eliminar_empleado(empleado_id)

    def calcular_bono_empleado(self, empleado_id):
        empleados = self.obtener_empleados()
        empleado = next((e for e in empleados if e.id_empleado == empleado_id), None)
        if not empleado:
            raise ValueError("Empleado no encontrado.")
        return empleado.calcular_bono()


class PlanEntrenamiento:
    def __init__(self, nombre, descripcion, duracion_semanas, id_plan=None):
        self.id_plan = id_plan
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion_semanas = duracion_semanas

    def mostrar_info(self):
        return f"[Plan {self.id_plan or '-'}] {self.nombre} ({self.duracion_semanas} semanas): {self.descripcion}"


class PlanService:
    def __init__(self):
        self.dal = PlanDAL()

    def agregar_plan(self, plan: PlanEntrenamiento):
        self.dal.insertar_plan(plan.nombre, plan.descripcion, plan.duracion_semanas)

    def obtener_planes(self):
        registros = self.dal.listar_planes()
        return [PlanEntrenamiento(id_plan=r[0], nombre=r[1], descripcion=r[2], duracion_semanas=r[3]) for r in registros]

    def asignar_plan_a_cliente(self, cliente_id, plan_id):
        self.dal.asignar_plan_a_cliente(cliente_id, plan_id)


# En el caso de los
# empleados, se deberá incluir información relacionada con su puesto y salario, y el
# sistema deberá permitir calcular y mostrar un bono adicional según criterios
# definidos

