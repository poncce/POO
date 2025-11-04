import sqlite3


class DatabaseConnection:
    def __init__(self, db_name="gimnasio.db"):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("Ocurrió un error:", exc_value)
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


class ClienteDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL
                )
            """)

    def insertar_cliente(self, nombre, correo):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "INSERT INTO clientes (nombre, correo) VALUES (?, ?)",
                    (nombre, correo)
                )
        except sqlite3.IntegrityError as e:
            raise Exception("Error al insertar: correo duplicado.") from e

    def listar_clientes(self):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM clientes")
            return cursor.fetchall()

    def actualizar_cliente(self, cliente_id, nombre, correo):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "UPDATE clientes SET nombre = ?, correo = ? WHERE id = ?",
                    (nombre, correo, cliente_id)
                )
                if cursor.rowcount == 0:
                    raise Exception("Cliente no encontrado.")
        except sqlite3.IntegrityError as e:
            raise Exception("Error al actualizar: correo duplicado.") from e

    def eliminar_cliente(self, cliente_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            if cursor.rowcount == 0:
                raise Exception("Cliente no encontrado.")


class EmpleadoDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL,
                    puesto TEXT NOT NULL,
                    salario REAL NOT NULL
                )
            """)

    def insertar_empleado(self, nombre, correo, puesto, salario):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "INSERT INTO empleados (nombre, correo, puesto, salario) VALUES (?, ?, ?, ?)",
                    (nombre, correo, puesto, salario)
                )
        except sqlite3.IntegrityError as e:
            raise Exception("Error al insertar: correo duplicado.") from e

    def listar_empleados(self):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM empleados")
            return cursor.fetchall()

    def actualizar_empleado(self, empleado_id, nombre, correo, puesto, salario):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "UPDATE empleados SET nombre = ?, correo = ?, puesto = ?, salario = ? WHERE id = ?",
                    (nombre, correo, puesto, salario, empleado_id)
                )
                if cursor.rowcount == 0:
                    raise Exception("Empleado no encontrado.")
        except sqlite3.IntegrityError as e:
            raise Exception("Error al actualizar: correo duplicado.") from e

    def eliminar_empleado(self, empleado_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM empleados WHERE id = ?", (empleado_id,))
            if cursor.rowcount == 0:
                raise Exception("Empleado no encontrado.")


class PlanDAL:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        with DatabaseConnection() as cursor:
            # Tabla de planes de entrenamiento
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS planes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    duracion_semanas INTEGER NOT NULL
                )
            """)
            # Tabla de relación muchos a muchos entre clientes y planes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cliente_plan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    plan_id INTEGER NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
                    FOREIGN KEY (plan_id) REFERENCES planes(id) ON DELETE CASCADE,
                    UNIQUE(cliente_id, plan_id)
                )
            """)

    def insertar_plan(self, nombre, descripcion, duracion_semanas):
        with DatabaseConnection() as cursor:
            cursor.execute(
                "INSERT INTO planes (nombre, descripcion, duracion_semanas) VALUES (?, ?, ?)",
                (nombre, descripcion, duracion_semanas)
            )

    def listar_planes(self):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM planes")
            return cursor.fetchall()

    def actualizar_plan(self, plan_id, nombre, descripcion, duracion_semanas):
        with DatabaseConnection() as cursor:
            cursor.execute(
                "UPDATE planes SET nombre = ?, descripcion = ?, duracion_semanas = ? WHERE id = ?",
                (nombre, descripcion, duracion_semanas, plan_id)
            )
            if cursor.rowcount == 0:
                raise Exception("Plan no encontrado.")

    def eliminar_plan(self, plan_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM planes WHERE id = ?", (plan_id,))
            if cursor.rowcount == 0:
                raise Exception("Plan no encontrado.")

    def asignar_plan_a_cliente(self, cliente_id, plan_id):
        try:
            with DatabaseConnection() as cursor:
                # Verificar que el cliente y el plan existen
                cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
                if not cursor.fetchone():
                    raise Exception("Cliente no encontrado.")
                
                cursor.execute("SELECT id FROM planes WHERE id = ?", (plan_id,))
                if not cursor.fetchone():
                    raise Exception("Plan no encontrado.")
                
                # Asignar el plan
                cursor.execute(
                    "INSERT INTO cliente_plan (cliente_id, plan_id) VALUES (?, ?)",
                    (cliente_id, plan_id)
                )
        except sqlite3.IntegrityError:
            raise Exception("El plan ya está asignado a este cliente.")

    def obtener_planes_de_cliente(self, cliente_id):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT p.id, p.nombre, p.descripcion, p.duracion_semanas
                FROM planes p
                INNER JOIN cliente_plan cp ON p.id = cp.plan_id
                WHERE cp.cliente_id = ?
            """, (cliente_id,))
            return cursor.fetchall()

    def desasignar_plan_de_cliente(self, cliente_id, plan_id):
        with DatabaseConnection() as cursor:
            cursor.execute(
                "DELETE FROM cliente_plan WHERE cliente_id = ? AND plan_id = ?",
                (cliente_id, plan_id)
            )
            if cursor.rowcount == 0:
                raise Exception("Asignación no encontrada.")