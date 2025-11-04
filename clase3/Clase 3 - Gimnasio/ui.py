from bll import (ClienteService, EmpleadoService, PlanService, ReporteService,
                 Cliente, Empleado, PlanEntrenamiento)


def mostrar_menu():
    print("\n" + "=" * 50)
    print("    SISTEMA DE GESTIÓN DEL GIMNASIO")
    print("=" * 50)
    print("CLIENTES:")
    print("  1. Registrar cliente")
    print("  2. Listar clientes")
    print("  3. Modificar cliente")
    print("  4. Eliminar cliente")
    print("\nEMPLEADOS:")
    print("  5. Registrar empleado")
    print("  6. Listar empleados")
    print("  7. Modificar empleado")
    print("  8. Eliminar empleado")
    print("  9. Calcular bono de empleado")
    print("\nPLANES DE ENTRENAMIENTO:")
    print(" 10. Registrar plan de entrenamiento")
    print(" 11. Listar planes de entrenamiento")
    print(" 12. Modificar plan de entrenamiento")
    print(" 13. Eliminar plan de entrenamiento")
    print(" 14. Asignar plan a cliente")
    print(" 15. Desasignar plan de cliente")
    print("\nREPORTES:")
    print(" 16. Generar reporte completo")
    print("\n 0. Salir")
    print("=" * 50)


def main():
    cliente_service = ClienteService()
    empleado_service = EmpleadoService()
    plan_service = PlanService()
    reporte_service = ReporteService()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        try:
            # OPERACIONES DE CLIENTES
            if opcion == "1":
                print("\n--- REGISTRAR CLIENTE ---")
                nombre = input("Nombre del cliente: ").strip()
                correo = input("Correo: ").strip()
                cliente = Cliente(nombre, correo)
                cliente_service.agregar_cliente(cliente)
                print("✓ Cliente registrado correctamente.")

            elif opcion == "2":
                print("\n--- LISTA DE CLIENTES ---")
                clientes = cliente_service.obtener_clientes()
                if not clientes:
                    print("No hay clientes registrados.")
                else:
                    for c in clientes:
                        print(c.mostrar_info())

            elif opcion == "3":
                print("\n--- MODIFICAR CLIENTE ---")
                cliente_id = int(input("ID del cliente a modificar: "))
                nombre = input("Nuevo nombre: ").strip()
                correo = input("Nuevo correo: ").strip()
                cliente_service.actualizar_cliente(cliente_id, nombre, correo)
                print("✓ Cliente modificado correctamente.")

            elif opcion == "4":
                print("\n--- ELIMINAR CLIENTE ---")
                cliente_id = int(input("ID del cliente a eliminar: "))
                confirmacion = input(f"¿Está seguro de eliminar el cliente {cliente_id}? (s/n): ").lower()
                if confirmacion == 's':
                    cliente_service.eliminar_cliente(cliente_id)
                    print("✓ Cliente eliminado correctamente.")
                else:
                    print("Operación cancelada.")

            # OPERACIONES DE EMPLEADOS
            elif opcion == "5":
                print("\n--- REGISTRAR EMPLEADO ---")
                nombre = input("Nombre del empleado: ").strip()
                correo = input("Correo: ").strip()
                puesto = input("Puesto: ").strip()
                salario = float(input("Salario: "))
                empleado = Empleado(nombre, correo, puesto, salario)
                empleado_service.agregar_empleado(empleado)
                print("✓ Empleado registrado correctamente.")

            elif opcion == "6":
                print("\n--- LISTA DE EMPLEADOS ---")
                empleados = empleado_service.obtener_empleados()
                if not empleados:
                    print("No hay empleados registrados.")
                else:
                    for e in empleados:
                        print(e.mostrar_info())

            elif opcion == "7":
                print("\n--- MODIFICAR EMPLEADO ---")
                empleado_id = int(input("ID del empleado a modificar: "))
                nombre = input("Nuevo nombre: ").strip()
                correo = input("Nuevo correo: ").strip()
                puesto = input("Nuevo puesto: ").strip()
                salario = float(input("Nuevo salario: "))
                empleado_service.actualizar_empleado(empleado_id, nombre, correo, puesto, salario)
                print("✓ Empleado modificado correctamente.")

            elif opcion == "8":
                print("\n--- ELIMINAR EMPLEADO ---")
                empleado_id = int(input("ID del empleado a eliminar: "))
                confirmacion = input(f"¿Está seguro de eliminar el empleado {empleado_id}? (s/n): ").lower()
                if confirmacion == 's':
                    empleado_service.eliminar_empleado(empleado_id)
                    print("✓ Empleado eliminado correctamente.")
                else:
                    print("Operación cancelada.")

            elif opcion == "9":
                print("\n--- CALCULAR BONO DE EMPLEADO ---")
                empleado_id = int(input("ID del empleado: "))
                bono = empleado_service.calcular_bono_empleado(empleado_id)
                print(f"✓ El bono calculado es: ${bono:.2f}")

            # OPERACIONES DE PLANES
            elif opcion == "10":
                print("\n--- REGISTRAR PLAN DE ENTRENAMIENTO ---")
                nombre = input("Nombre del plan: ").strip()
                descripcion = input("Descripción: ").strip()
                duracion = int(input("Duración (semanas): "))
                plan = PlanEntrenamiento(nombre, descripcion, duracion)
                plan_service.agregar_plan(plan)
                print("✓ Plan de entrenamiento agregado correctamente.")

            elif opcion == "11":
                print("\n--- LISTA DE PLANES DE ENTRENAMIENTO ---")
                planes = plan_service.obtener_planes()
                if not planes:
                    print("No hay planes registrados.")
                else:
                    for p in planes:
                        print(p.mostrar_info())

            elif opcion == "12":
                print("\n--- MODIFICAR PLAN DE ENTRENAMIENTO ---")
                plan_id = int(input("ID del plan a modificar: "))
                nombre = input("Nuevo nombre: ").strip()
                descripcion = input("Nueva descripción: ").strip()
                duracion = int(input("Nueva duración (semanas): "))
                plan_service.actualizar_plan(plan_id, nombre, descripcion, duracion)
                print("✓ Plan modificado correctamente.")

            elif opcion == "13":
                print("\n--- ELIMINAR PLAN DE ENTRENAMIENTO ---")
                plan_id = int(input("ID del plan a eliminar: "))
                confirmacion = input(f"¿Está seguro de eliminar el plan {plan_id}? (s/n): ").lower()
                if confirmacion == 's':
                    plan_service.eliminar_plan(plan_id)
                    print("✓ Plan eliminado correctamente.")
                else:
                    print("Operación cancelada.")

            elif opcion == "14":
                print("\n--- ASIGNAR PLAN A CLIENTE ---")
                cliente_id = int(input("ID del cliente: "))
                plan_id = int(input("ID del plan: "))
                plan_service.asignar_plan_a_cliente(cliente_id, plan_id)
                print("✓ Plan asignado correctamente.")

            elif opcion == "15":
                print("\n--- DESASIGNAR PLAN DE CLIENTE ---")
                cliente_id = int(input("ID del cliente: "))
                plan_id = int(input("ID del plan: "))
                plan_service.desasignar_plan_de_cliente(cliente_id, plan_id)
                print("✓ Plan desasignado correctamente.")

            # REPORTES
            elif opcion == "16":
                print("\n--- GENERAR REPORTE COMPLETO ---")
                nombre_archivo = input("Nombre del archivo (Enter para usar 'reporte_gimnasio.txt'): ").strip()
                if not nombre_archivo:
                    nombre_archivo = "reporte_gimnasio.txt"
                archivo_generado = reporte_service.generar_reporte_completo(nombre_archivo)
                print(f"✓ Reporte generado exitosamente: {archivo_generado}")

            elif opcion == "0":
                print("\n¡Gracias por usar el Sistema de Gestión del Gimnasio!")
                print("Saliendo del sistema...")
                break

            else:
                print("✗ Opción inválida. Por favor, seleccione una opción del menú.")

        except ValueError as e:
            print(f"✗ Error de validación: {e}")
        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()