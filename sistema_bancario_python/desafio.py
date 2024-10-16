menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == '1':
        valor = float(input('Quanto deseja depositar? '))
        if valor > 0:
            saldo += valor
            extrato += f'Deposito: R${valor:.2f}\n'
        else:
            print('Operação inválida, tente novamente.')

    elif opcao == '2':
        valor = float(input('Quanto deseja sacar? '))
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
        else:
            print('Operação inválida, tente novamente.')

    elif opcao == '3':
        print('Extrato')
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'\nSaldo: R${saldo:.2f}')
        print(f'Limite: R${limite:.2f}')
        print(f'Número de saques: {numero_saques}')

    elif opcao == '4':
        break

    else:
        print('Operação inválida, tente novamente.')        

        