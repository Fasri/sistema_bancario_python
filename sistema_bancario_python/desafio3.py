from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self.agencia = '0001'
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    @property
    def cliente(self):
        return self._cliente
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo   
                
        if excedeu_saldo:
            print('Saldo insuficiente.')
        
        elif valor > 0:
            saldo -= valor
            print('Saque realizado com sucesso.')
        else:    
            print('Operação inválida, tente novamente.')
        return False

    def depositar(self, valor):
        
        if valor > 0:
            self.saldo += valor
            print('Deposito realizado com sucesso.')
        else:    
            print('Operação inválida, tente novamente.')
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite    
        self.limite_saques = limite_saques   

    def sacar(self, valor):
        numero_saques = self.historico.verificar_saques()
        if numero_saques >= self.limite_saques:
            print(f'Você excedeu o limite de saques. Tente novamente daqui a {self.limite_saques} vezes.')
        elif valor > self.limite:
            print(f'Você excedeu o limite de R${self.limite}. Tente novamente daqui a {self.limite_saques} vezes.')
        else:
            return super().sacar(valor)
        return False
    def __str__(self):
        return f"""
        Agência: {self.agencia}
        C/C: {self.numero}
        Titular: {self.cliente.nome}
        Saldo: {self.saldo}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []
    def adicionar_transacao(self, transacao):
        self._transacoes.append({"tipo": transacao.__class__.__name__,
        'valor': transacao.valor, 
        'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')})
    def verficar_saques(self):
        return len([transacao for transacao in self._transacoes if transacao['tipo'] == 'saque'])
    @property    
    def transacoes(self):
        return self._transacoes
    
class Transação(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor
    @property    
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transação):
    def __init__(self, valor):
        self._valor = valor
    @property    
    def valor(self):
        return self._valor
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
def menu():
    menu = """
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova conta
    [5] Listar contas
    [6] Novo cliente
    [7] Sair
    => """
    return input(textwrap.dedent(menu))

def exibir_extrato(clientes):
   cpf = input('CPF (somente números): ')
   cliente = filtrar_clientes(cpf, clientes)
   if not cliente:
       print('CPF não encontrado.')
       return
   conta = recuperar_conta_corrente(cliente)
   if not conta:
       print('Não há nenhuma conta para este cliente.')
       return
   print('Extrato:')
   
   transacoes = conta.historico.transacoes

   if not transacoes:
       print('Não foram realizadas movimentações.')
       return
   else:
        extrato = f"""\
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{cliente.nome}
            """
        for transacao in transacoes:
            extrato += f"""\
                Data:\t{transacao['data']}
                Tipo:\t{transacao['tipo']}
                Valor:\t{transacao['valor']}
                """
        print(textwrap.dedent(extrato))
        print(f"Saldo:\t{conta.saldo:.2f}")

def criar_cliente(clientes):
    cpf = input('CPF (somente números): ')
    cliente = filtrar_clientes(cpf, clientes)
    if cliente:
        print('Já existe cliente com esse CPF.')
        return

    nome = input('Nome completo: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    endereco = input('Endereço (logradouro, nro - bairro - cidade/sigle estado): ')  

    cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)

    print(f'Cliente {nome} criado com sucesso.')

def filtrar_clientes(cpf, clientes): 

    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None   

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe seu CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('CPF não encontrado, fluxo de criação de conta encerrado.')
        return
    
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    print(f'Conta criada com sucesso. Seu número é {conta}')

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def recuperar_conta_corrente(cliente):
    if not cliente.contas:
        print('Cliente não possui contas.')
        return None
    return cliente.contas[0]       

def depositar(clientes):

    cpf = input('CPF (somente números): ')
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('CPF não encontrado.')
    else:
        valor = float(input('Quanto deseja depositar? '))
        transacao = Deposito(valor)
        conta = recuperar_conta_corrente(cliente)
        if not conta:
            return
        cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('CPF (somente números): ')
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('CPF não encontrado.')
    else:
        valor = float(input('Quanto deseja sacar? '))
        transacao = Saque(valor)
        conta = recuperar_conta_corrente(cliente)
        if not conta:
            return
        cliente.realizar_transacao(conta, transacao)
def main():
   
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
           depositar(clientes)

        elif opcao == '2':
            sacar(clientes)

        elif opcao == '3':
            exibir_extrato(clientes)

        elif opcao == '4':
            
           numero_conta = len(contas) + 1
           criar_conta(numero_conta, clientes, contas)
          

        elif opcao == '5':
            listar_contas(contas)

        elif opcao == '6':
            criar_cliente(clientes)

        elif opcao == '7':
            print('ate a proxima!')
            break

        else:
            print('Operação inválida, tente novamente.')


if __name__ == '__main__':
    main()


