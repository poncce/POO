class CuentaBancaria:
    def __init__ (self, titular, saldo):
        self.titular = titular
        self.__saldo = saldo

    def get_saldo(self):
        return self.__saldo

    def depositar(self, monto):
        if monto <= 0:
            raise  ValueError("El monto a depositar debe ser positivo")
        self.__saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto a retirar tiene q ser positivo")
        elif monto > self.__saldo:
            raise ValueError("Fondos insuficientes")
        self.__saldo -= monto

class CuentaNegocio:
    def __init__ (self):
        self.__cuentas = {}

    def crear_cuenta(self, titular, saldo_inicial = 0):
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        cuenta = CuentaBancaria(titular, saldo_inicial)
        self.__cuentas[titular] = cuenta   
        return cuenta 

    def depositar(self, titular, monto):
        cuenta = self.buscar_cuenta(titular)
        cuenta.depositar(monto)
        return cuenta.get_saldo()
    
    def retirar(self, titular, monto):
        cuenta = self.buscar_cuenta(titular)
        cuenta.retirar(monto)
        return cuenta.get_saldo()

    def ver_saldo(self, titular):
        cuenta = self.buscar_cuenta(titular)
        return cuenta.get_saldo()

    def buscar_cuenta(self, titular):
        if titular not in self.__cuentas:
            raise ValueError('Titular no encontrado')
        return self.__cuentas[titular]

        
    def listar_cuentas(self):
        return self.__cuentas.values()