import sqlite3


class DatabaseConnection:
    def __init__(self, db_name="clientes.db"):
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

    def eliminar_empleado(self, empleado_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM empleados WHERE id = ?", (empleado_id,))
            if cursor.rowcount == 0:
                raise Exception("Empleado no encontrado.")

