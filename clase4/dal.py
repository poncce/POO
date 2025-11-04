import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="veterinaria.db"):
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

class DuenoDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dueno (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL
                )
            """)

    def insertar_dueno(self, nombre, apellido, direccion, correo):
        try:
            with DatabaseConnection as cursor:
                cursor.execute("" \
                "INSERT INTO dueno (nombre, apellido, direccion, correo) VALUES (?. ?, ?, ?)", (nombre, apellido, direccion, correo))
        except sqlite3.IntegrityError as e:
            raise Exception("Error al insertar: correo duplicado.") from e

    def listar_duenos(self):
        with DatabaseConnection as cursor:
            cursor.execute("SELECT * FROM dueno")
            return cursor.fetchall()
        
    def actualizar_duenos(self, dueno_id, nombre, apellido, direccion, correo):
        try:
            with DatabaseConnection as cursor:
                cursor.execute("" 
                "UPDATE dueno SET nombre = ?, SET apellido = ?, direccion = ?, correo = ? WHERE dueno_id = ? ", (dueno_id, nombre, apellido, direccion, correo))
                if cursor.rowcount == 0:
                    raise Exception("Dueño no encontrado")
        except sqlite3.IntegrityError as e:
            raise Exception(f"El correo {correo} ya esta registrado")
        
    def eliminar_duenos(self, dueno_id):
        with DatabaseConnection as cursor:
            cursor.execute("DELETE FROM dueno where dueno_id = ?", (dueno_id))
            if cursor.rowcount == 0:
                raise Exception("Dueño no encontrado")
            

class MascotaDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mascotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especie TEXT NOT NULL,
                    raza TEXT,
                    edad INTEGER,
                    peso REAL,
                    dueno_id INTEGER NOT NULL,
                    FOREIGN KEY (dueno_id) REFERENCES duenos(id) ON DELETE CASCADE
                )
            """)

    def insertar_mascota(self, nombre, especie, raza, edad, peso, dueno_id):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT id FROM duenos WHERE id = ?", (dueno_id,))
            if not cursor.fetchone():
                raise Exception("El dueño especificado no existe.")
            
            cursor.execute(
                "INSERT INTO mascotas (nombre, especie, raza, edad, peso, dueno_id) VALUES (?, ?, ?, ?, ?, ?)",
                (nombre, especie, raza, edad, peso, dueno_id)
            )

    def listar_mascotas(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT m.*, d.nombre, d.apellido
                FROM mascotas m
                JOIN duenos d ON m.dueno_id = d.id
                ORDER BY m.nombre
            """)
            return cursor.fetchall()

    def buscar_mascota_por_id(self, mascota_id):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT m.*, d.nombre, d.apellido
                FROM mascotas m
                JOIN duenos d ON m.dueno_id = d.id
                WHERE m.id = ?
            """, (mascota_id,))
            return cursor.fetchone()

    def listar_mascotas_por_dueno(self, dueno_id):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM mascotas WHERE dueno_id = ?", (dueno_id,))
            return cursor.fetchall()

    def actualizar_mascota(self, mascota_id, nombre, especie, raza, edad, peso, dueno_id):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT id FROM duenos WHERE id = ?", (dueno_id,))
            if not cursor.fetchone():
                raise Exception("El dueño especificado no existe.")
            
            cursor.execute(
                "UPDATE mascotas SET nombre = ?, especie = ?, raza = ?, edad = ?, peso = ?, dueno_id = ? WHERE id = ?",
                (nombre, especie, raza, edad, peso, dueno_id, mascota_id)
            )
            if cursor.rowcount == 0:
                raise Exception("Mascota no encontrada.")

    def eliminar_mascota(self, mascota_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            if cursor.rowcount == 0:
                raise Exception("Mascota no encontrada.")


class VeterinarioDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS veterinarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    especialidad TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT UNIQUE
                )
            """)

    def insertar_veterinario(self, nombre, apellido, especialidad, telefono, email):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "INSERT INTO veterinarios (nombre, apellido, especialidad, telefono, email) VALUES (?, ?, ?, ?, ?)",
                    (nombre, apellido, especialidad, telefono, email)
                )
        except sqlite3.IntegrityError as e:
            raise Exception("Error: el email ya está registrado.") from e

    def listar_veterinarios(self):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM veterinarios ORDER BY apellido, nombre")
            return cursor.fetchall()

    def buscar_veterinario_por_id(self, veterinario_id):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT * FROM veterinarios WHERE id = ?", (veterinario_id,))
            return cursor.fetchone()

    def actualizar_veterinario(self, veterinario_id, nombre, apellido, especialidad, telefono, email):
        try:
            with DatabaseConnection() as cursor:
                cursor.execute(
                    "UPDATE veterinarios SET nombre = ?, apellido = ?, especialidad = ?, telefono = ?, email = ? WHERE id = ?",
                    (nombre, apellido, especialidad, telefono, email, veterinario_id)
                )
                if cursor.rowcount == 0:
                    raise Exception("Veterinario no encontrado.")
        except sqlite3.IntegrityError as e:
            raise Exception("Error: el email ya está registrado.") from e

    def eliminar_veterinario(self, veterinario_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM veterinarios WHERE id = ?", (veterinario_id,))
            if cursor.rowcount == 0:
                raise Exception("Veterinario no encontrado.")


class CitaDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS citas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mascota_id INTEGER NOT NULL,
                    veterinario_id INTEGER NOT NULL,
                    fecha_hora TEXT NOT NULL,
                    motivo TEXT NOT NULL,
                    estado TEXT DEFAULT 'Programada',
                    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
                    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id)
                )
            """)

    def insertar_cita(self, mascota_id, veterinario_id, fecha_hora, motivo):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT id FROM mascotas WHERE id = ?", (mascota_id,))
            if not cursor.fetchone():
                raise Exception("La mascota especificada no existe.")
            
            cursor.execute("SELECT id FROM veterinarios WHERE id = ?", (veterinario_id,))
            if not cursor.fetchone():
                raise Exception("El veterinario especificado no existe.")
            
            cursor.execute(
                "INSERT INTO citas (mascota_id, veterinario_id, fecha_hora, motivo) VALUES (?, ?, ?, ?)",
                (mascota_id, veterinario_id, fecha_hora, motivo)
            )

    def listar_citas(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT c.*, m.nombre as mascota_nombre, v.nombre as vet_nombre, v.apellido as vet_apellido
                FROM citas c
                JOIN mascotas m ON c.mascota_id = m.id
                JOIN veterinarios v ON c.veterinario_id = v.id
                ORDER BY c.fecha_hora DESC
            """)
            return cursor.fetchall()

    def listar_citas_por_estado(self, estado):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT c.*, m.nombre as mascota_nombre, v.nombre as vet_nombre, v.apellido as vet_apellido
                FROM citas c
                JOIN mascotas m ON c.mascota_id = m.id
                JOIN veterinarios v ON c.veterinario_id = v.id
                WHERE c.estado = ?
                ORDER BY c.fecha_hora
            """, (estado,))
            return cursor.fetchall()

    def actualizar_estado_cita(self, cita_id, estado):
        with DatabaseConnection() as cursor:
            cursor.execute("UPDATE citas SET estado = ? WHERE id = ?", (estado, cita_id))
            if cursor.rowcount == 0:
                raise Exception("Cita no encontrada.")

    def eliminar_cita(self, cita_id):
        with DatabaseConnection() as cursor:
            cursor.execute("DELETE FROM citas WHERE id = ?", (cita_id,))
            if cursor.rowcount == 0:
                raise Exception("Cita no encontrada.")

class HistorialMedicoDAL:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_medico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mascota_id INTEGER NOT NULL,
                    veterinario_id INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    diagnostico TEXT NOT NULL,
                    tratamiento TEXT,
                    observaciones TEXT,
                    FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
                    FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id)
                )
            """)

    def insertar_registro(self, mascota_id, veterinario_id, fecha, diagnostico, tratamiento, observaciones):
        with DatabaseConnection() as cursor:
            cursor.execute("SELECT id FROM mascotas WHERE id = ?", (mascota_id,))
            if not cursor.fetchone():
                raise Exception("La mascota especificada no existe.")
            
            cursor.execute("SELECT id FROM veterinarios WHERE id = ?", (veterinario_id,))
            if not cursor.fetchone():
                raise Exception("El veterinario especificado no existe.")
            
            cursor.execute(
                "INSERT INTO historial_medico (mascota_id, veterinario_id, fecha, diagnostico, tratamiento, observaciones) VALUES (?, ?, ?, ?, ?, ?)",
                (mascota_id, veterinario_id, fecha, diagnostico, tratamiento, observaciones)
            )

    def listar_historial_por_mascota(self, mascota_id):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT h.*, v.nombre, v.apellido
                FROM historial_medico h
                JOIN veterinarios v ON h.veterinario_id = v.id
                WHERE h.mascota_id = ?
                ORDER BY h.fecha DESC
            """, (mascota_id,))
            return cursor.fetchall()

    def listar_todo_historial(self):
        with DatabaseConnection() as cursor:
            cursor.execute("""
                SELECT h.*, m.nombre as mascota_nombre, v.nombre as vet_nombre, v.apellido as vet_apellido
                FROM historial_medico h
                JOIN mascotas m ON h.mascota_id = m.id
                JOIN veterinarios v ON h.veterinario_id = v.id
                ORDER BY h.fecha DESC
            """)
            return cursor.fetchall()