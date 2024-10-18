import textwrap
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

def depositar(saldo, valor, extrato, /):  # recebe os argumentos por posição
    if valor > 0:
        saldo += valor
        extrato += f'Deposito: R${valor:.2f}\n'
        print('Deposito realizado com sucesso.')
    else:    
        print('Operação inválida, tente novamente.')
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo   
    excedeu_limite = valor > limite and not excedeu_saldo
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    if excedeu_saldo:
        print('Saldo insuficiente.')
    elif excedeu_limite:    
        print('O limite máximo de saques é de R$500,00.')
    elif excedeu_saques:    
        print('Número de saques excedido.')
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R${valor:.2f}\n'
        numero_saques += 1
        print('Saque realizado com sucesso.')
    else:    
        print('Operação inválida, tente novamente.')
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print('Extrato')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'Saldo: R${saldo:.2f}')
def criar_cliente(clientes):
    cpf = input('CPF (somente números): ')
    cliente = filtrar_clientes(cpf, clientes)
    if cliente:
        print('Já existe cliente com esse CPF.')
        return None

    nome = input('Nome completo: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    endereco = input('Endereço (logradouro, nro - bairro - cidade/sigle estado): ')  
    clientes.append({'nome': nome, 'cpf': cpf, 'data_nascimento': data_nascimento, 'endereco': endereco})

    print(f'Cliente {nome} criado com sucesso.')

def filtrar_clientes(cpf, clientes): 

    clientes_filtrados = [cliente for cliente in clientes if cliente['cpf'] == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None   

def criar_conta(agencia, numero_conta, clientes):
    cpf = input("Informe seu CPF (somente números): ")
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'cliente': cliente}
    print('Cliente nao encontrado, fluxo de criacao de conta encerrado.')

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}    
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['cliente']['nome']}
            CPF:\t\t{conta['cliente']['cpf']}
            """

        print("=" * 100)
        print(textwrap.dedent(linha))
        

def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == '1':
            valor = float(input('Quanto deseja depositar? '))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == '2':
            valor = float(input('Quanto deseja sacar? '))
            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, 
            limite=limite, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)

        elif opcao == '3':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == '4':
            
            conta = criar_conta(AGENCIA, len(contas) + 1, clientes)

            if conta:
                contas.append(conta)

        elif opcao == '5':
            quantas = len(contas)
            print(f'Existem {quantas} contas no sistema.')

        elif opcao == '6':
            criar_cliente(clientes)

        elif opcao == '7':
            print('ate a proxima!')
            break

        else:
            print('Operação inválida, tente novamente.')


if __name__ == '__main__':
    main()


# saldo = 0
# limite = 500
# extrato = ""
# numero_saques = 0
# LIMITE_SAQUES = 3

# while True:
#     opcao = menu()

#     if opcao == '1':
#         valor = float(input('Quanto deseja depositar? '))
#         if valor > 0:
#             saldo += valor
#             extrato += f'Deposito: R${valor:.2f}\n'
#         else:
#             print('Operação inválida, tente novamente.')

#     elif opcao == '2':
#         valor = float(input('Quanto deseja sacar? '))
#         excedeu_saldo = valor > saldo

#         excedeu_limite = valor > limite and not excedeu_saldo

#         excedeu_saques = numero_saques >= LIMITE_SAQUES

#         if excedeu_saldo:
#             print('Saldo insuficiente.')

#         elif excedeu_limite:
#             print('O limite máximo de saques é de R$500,00.')

#         elif excedeu_saques:    
#             print('Número de saques excedido.')

#         elif valor > 0:
#             saldo -= valor
#             extrato += f'Saque: R${valor:.2f}\n'
#             numero_saques += 1
#         else:
#             print('Operação inválida, tente novamente.')

#     elif opcao == '3':
#         print('Extrato')
#         print('Não foram realizadas movimentações.' if not extrato else extrato)
#         print(f'\nSaldo: R${saldo:.2f}')
#         print(f'Limite: R${limite:.2f}')
#         print(f'Número de saques: {numero_saques}')

#     elif opcao == '4':
#         break

#     else:
#         print('Operação inválida, tente novamente.')        

        