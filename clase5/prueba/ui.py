from bll import HidroelectricaBLL

def mostrar_menu():
    print("\n--- Central Hidroeléctrica ---")
    print("1. Calcular porcentaje de energía consumida")
    print("2. Identificar turbina más eficiente")
    print("3. Salir")
    print("------------------------------")

def main():
    bll = HidroelectricaBLL()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            porcentaje = bll.calcular_porcentaje_consumido()
            print(f"\nPorcentaje de energía consumida: {porcentaje}%")
        
        elif opcion == "2":
            turbina = bll.turbina_mas_eficiente()
            if turbina:
                print(f"\nLa turbina más eficiente es: {turbina}")
            else:
                print("\nNo se pudo determinar la turbina más eficiente")
        
        elif opcion == "3":
            print("\nSaliendo del sistema...")
            break
        
        else:
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()