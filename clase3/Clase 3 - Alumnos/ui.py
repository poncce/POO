from bll import ClienteService, EmpleadoService, PlanService, Cliente, Empleado, PlanEntrenamiento


def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DEL GIMNASIO ===")
    print("1. Registrar cliente")
    print("2. Listar clientes")
    print("3. Eliminar cliente")
    print("4. Registrar empleado")
    print("5. Listar empleados")
    print("6. Registrar plan de entrenamiento")
    print("7. Listar planes de entrenamiento")
    print("8. Asignar plan a cliente")
    print("9. Salir")


def main():
    cliente_service = ClienteService()
    empleado_service = EmpleadoService()
    plan_service = PlanService()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                nombre = input("Nombre del cliente: ")
                correo = input("Correo: ")
                cliente = Cliente(nombre, correo)
                cliente_service.agregar_cliente(cliente)
                print("Cliente registrado correctamente.")

            elif opcion == "2":
                clientes = cliente_service.obtener_clientes()
                if not clientes:
                    print("No hay clientes registrados.")
                else:
                    for c in clientes:
                        print(c.mostrar_info())

            elif opcion == "3":
                cliente_id = int(input("ID del cliente a eliminar: "))
                cliente_service.eliminar_cliente(cliente_id)
                print("Cliente eliminado correctamente.")

            elif opcion == "4":
                nombre = input("Nombre del empleado: ")
                correo = input("Correo: ")
                puesto = input("Puesto: ")
                salario = float(input("Salario: "))
                empleado = Empleado(nombre, correo, puesto, salario)
                empleado_service.agregar_empleado(empleado)
                print("Empleado registrado correctamente.")

            elif opcion == "5":
                empleados = empleado_service.obtener_empleados()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for e in empleados:
                        print(e.mostrar_info())

            elif opcion == "6":
                nombre = input("Nombre del plan: ")
                descripcion = input("Descripción: ")
                duracion = int(input("Duración (semanas): "))
                plan = PlanEntrenamiento(nombre, descripcion, duracion)
                plan_service.agregar_plan(plan)
                print("Plan de entrenamiento agregado correctamente.")

            elif opcion == "7":
                planes = plan_service.obtener_planes()
                if not planes:
                    print("No hay planes registrados.")
                else:
                    for p in planes:
                        print(p.mostrar_info())

            elif opcion == "8":
                cliente_id = int(input("ID del cliente: "))
                plan_id = int(input("ID del plan: "))
                plan_service.asignar_plan_a_cliente(cliente_id, plan_id)
                print("Plan asignado correctamente.")

            elif opcion == "9":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
