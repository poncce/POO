import sqlite3



class DatabaseConnection:
    def __init__(self, db_name="hidroelectrica.db"):
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


def crear_tablas():
    try:
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Turbina (
                    id_turbina INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    potencia_maxima FLOAT NOT NULL,
                    tipo_turbina TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Registro (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_turbina INTEGER NOT NULL,
                    energia_generada REAL NOT NULL,
                    energia_consumida REAL NOT NULL,
                    fecha_registro TEXT NOT NULL,
                )
            """)
        
    except Exception as e:
        print(f"error al crear tablas: {e}")


class TurbinaDAL:
    def __init__(self, db_name="hidroelectrica.db"):
        self.db_name = db_name
    
    def obtener_todas_turbinas(self):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT id_turbina, nombre, potencia_maxima, tipo_turbina FROM Turbina")
                turbinas = cursor.fetchall()
                return turbinas
        except Exception as e:
            print(f"error al seleccionar: {e}")
            return []
    
    def obtener_turbina_por_id(self, id_turbina):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT id_turbina, nombre, potencia_maxima, tipo_turbina FROM Turbina WHERE id_turbina = ?", (id_turbina,))
                turbina = cursor.fetchone()
                return turbina
        except Exception as e:
            print(f"error al seleccionar la turbina: {e}")
            return []



class RegistroDAL:
    def __init__(self, db_name="hidroelectrica.db"):
        self.db_name = db_name
    
    def obtener_todos_registros(self):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute("SELECT id_registro, id_turbina, energia_generada, energia_consumida, fecha_registro FROM Registro")
                registros = cursor.fetchall()
                return registros
        except Exception as e:
            print(f"error al seleccionar los registros: {e}")
            return []
    
    def obtener_registros_por_turbina(self, id_turbina):
        try:
            with DatabaseConnection(self.db_name) as cursor:
                cursor.execute("SELECT energia_generada FROM Registro WHERE id_turbina = ?", (id_turbina,))
                registros = cursor.fetchall()
                return registros
        except Exception as e:
            print(f"error al obtenerr los registros de la turbina: {e}")
            return []

