from dal import ClienteDAL, EmpleadoDAL, PlanDAL
from datetime import datetime


class Persona:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Correo: {self.correo}"


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
        # Cargar planes asociados
        for c in clientes:
            planes = self.plan_dal.obtener_planes_de_cliente(c.id_cliente)
            c.planes = [PlanEntrenamiento(id_plan=p[0], nombre=p[1], descripcion=p[2], duracion_semanas=p[3]) for p in planes]
        return clientes

    def actualizar_cliente(self, cliente_id, nombre, correo):
        if not nombre or not correo:
            raise ValueError("El nombre y correo son obligatorios.")
        self.dal.actualizar_cliente(cliente_id, nombre, correo)

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
        return f"[Empleado {self.id_empleado or '-'}] {super().mostrar_info()} | Puesto: {self.puesto} | Salario: ${self.salario:.2f} | Bono: ${bono:.2f}"


class EmpleadoService:
    def __init__(self):
        self.dal = EmpleadoDAL()

    def agregar_empleado(self, empleado: Empleado):
        if not empleado.nombre or not empleado.correo or not empleado.puesto:
            raise ValueError("El nombre, correo y puesto son obligatorios.")
        if empleado.salario <= 0:
            raise ValueError("El salario debe ser mayor a cero.")
        self.dal.insertar_empleado(empleado.nombre, empleado.correo, empleado.puesto, empleado.salario)

    def obtener_empleados(self):
        registros = self.dal.listar_empleados()
        return [Empleado(id_empleado=r[0], nombre=r[1], correo=r[2], puesto=r[3], salario=r[4]) for r in registros]

    def actualizar_empleado(self, empleado_id, nombre, correo, puesto, salario):
        if not nombre or not correo or not puesto:
            raise ValueError("El nombre, correo y puesto son obligatorios.")
        if salario <= 0:
            raise ValueError("El salario debe ser mayor a cero.")
        self.dal.actualizar_empleado(empleado_id, nombre, correo, puesto, salario)

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
        if not plan.nombre or plan.duracion_semanas <= 0:
            raise ValueError("El nombre y duración válida son obligatorios.")
        self.dal.insertar_plan(plan.nombre, plan.descripcion, plan.duracion_semanas)

    def obtener_planes(self):
        registros = self.dal.listar_planes()
        return [PlanEntrenamiento(id_plan=r[0], nombre=r[1], descripcion=r[2], duracion_semanas=r[3]) for r in registros]

    def actualizar_plan(self, plan_id, nombre, descripcion, duracion_semanas):
        if not nombre or duracion_semanas <= 0:
            raise ValueError("El nombre y duración válida son obligatorios.")
        self.dal.actualizar_plan(plan_id, nombre, descripcion, duracion_semanas)

    def eliminar_plan(self, plan_id):
        self.dal.eliminar_plan(plan_id)

    def asignar_plan_a_cliente(self, cliente_id, plan_id):
        self.dal.asignar_plan_a_cliente(cliente_id, plan_id)

    def desasignar_plan_de_cliente(self, cliente_id, plan_id):
        self.dal.desasignar_plan_de_cliente(cliente_id, plan_id)


class ReporteService:
    def __init__(self):
        self.cliente_service = ClienteService()
        self.empleado_service = EmpleadoService()
        self.plan_service = PlanService()

    def generar_reporte_completo(self, nombre_archivo="reporte_gimnasio.txt"):
        """Genera un reporte completo del gimnasio y lo guarda en un archivo de texto."""
        clientes = self.cliente_service.obtener_clientes()
        empleados = self.empleado_service.obtener_empleados()
        planes = self.plan_service.obtener_planes()

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("REPORTE DEL GIMNASIO\n")
            f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")

            # Resumen general
            f.write("RESUMEN GENERAL\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total de clientes: {len(clientes)}\n")
            f.write(f"Total de empleados activos: {len(empleados)}\n")
            f.write(f"Total de planes de entrenamiento: {len(planes)}\n\n")

            # Detalle de clientes
            f.write("DETALLE DE CLIENTES\n")
            f.write("-" * 60 + "\n")
            if clientes:
                for c in clientes:
                    f.write(f"{c.mostrar_info()}\n")
            else:
                f.write("No hay clientes registrados.\n")
            f.write("\n")

            # Detalle de empleados
            f.write("DETALLE DE EMPLEADOS\n")
            f.write("-" * 60 + "\n")
            if empleados:
                total_salarios = sum(e.salario for e in empleados)
                total_bonos = sum(e.calcular_bono() for e in empleados)
                for e in empleados:
                    f.write(f"{e.mostrar_info()}\n")
                f.write(f"\nTotal en salarios: ${total_salarios:.2f}\n")
                f.write(f"Total en bonos: ${total_bonos:.2f}\n")
            else:
                f.write("No hay empleados registrados.\n")
            f.write("\n")

            # Detalle de planes
            f.write("DETALLE DE PLANES DE ENTRENAMIENTO\n")
            f.write("-" * 60 + "\n")
            if planes:
                for p in planes:
                    f.write(f"{p.mostrar_info()}\n")
            else:
                f.write("No hay planes registrados.\n")
            f.write("\n")

            f.write("=" * 60 + "\n")
            f.write("FIN DEL REPORTE\n")
            f.write("=" * 60 + "\n")

        return nombre_archivo