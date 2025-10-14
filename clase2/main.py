from bll import CuentaNegocio

def main():
    negocio = CuentaNegocio()

    try:
        negocio.crear_cuenta("Jose", 1000)
        negocio.crear_cuenta("Alan", 3000)

        print("Depositar en cuenta Jose")
        nuevo_saldo = negocio.depositar("Jose", 200)
        print(f"Saldo en la cuneta de jose ${nuevo_saldo}")

        print("Retiro en la cuenta de Alan")
        nuevo_saldo= negocio.retirar("Alan", 100)
        print(f"Saldo de alan {nuevo_saldo}")

        print("Retirar mas de lo que hay")
        nuevo_saldo = negocio.retirar("Alan", 50000)
    except ValueError as e:
        print(f"Error de negocio: {e}")
    except Exception as e:
        print(f"Error inesperadovich: {e}")
    finally:
        print("\n---Listado de cuentas---")
        for cuenta in negocio.listar_cuentas():
            print(f"Titular: {cuenta.titular}, Saldo: {cuenta.get_saldo()}")
    

if __name__ == "__main__":
    main()