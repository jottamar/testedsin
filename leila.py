import datetime

def menu():
    opcao = input('''
===========================================
          PROJETO SALÃO DE BELEZA
          
 MENU:
[1] CADASTRAR CLIENTE
[2] REALIZAR AGENDAMENTO
[3] VISUALIZAR AGENDAMENTO
[4] EDITAR AGENDAMENTOS
===========================================  
ESCOLHA UMA OPÇÃO ACIMA  
''')
    if opcao == "1":
        cadastrarCliente()
    elif opcao == "2":
        menuAgendamentos()
    elif opcao == "3":
        visualizarAgendamentos()
    elif opcao == "4":
        cpf = input("Digite o CPF ou nome do cliente: ")
        nova_data = input("Digite a nova data do agendamento (formato: DD/MM/AAAA): ")
        nova_hora = input("Digite a nova hora do agendamento (formato: HH:MM): ")
        editarAgendamento(cpf, nova_data, nova_hora)
    else:
        print("OPÇÃO INVÁLIDA DIGITE UMA DE '1 A 4'")
        menu()
        return
    
    
        
def cadastrarCliente():
    while True:
        nome = input("Digite o nome do cliente: ")
        if not nome.isalpha():
            print("Nome inválido. Insira um nome com somente caracteres alfabéticos.")
        else:
            break

        with open("clientes.txt", "r") as arquivo_clientes:
            for linha in arquivo_clientes:
                if nome in linha:
                    print("Nome já cadastrado. Insira um nome diferente.")
                    menu()
                    return
                
    cpf = input("Digite o CPF do cliente: ")
    while True:
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Insira um CPF com 11 dígitos numéricos.")
            cpf = input("Digite o CPF do cliente novamente: ")
        else:
            break

    with open("clientes.txt", "r") as arquivo_clientes:
        for linha in arquivo_clientes:
            if cpf in linha:
                print("CPF já cadastrado. Insira um CPF diferente.")
                menu()
                return
            
    telefone = input("Digite o número de telefone do cliente: ")
    while True:
        if not telefone.isdigit() or len(telefone) != 11:
            print("Número de telefone inválido. Insira um número com 11 dígitos numéricos.")
            telefone = input("Digite o número de telefone do cliente novamente: ")
        else:
            break

    with open("clientes.txt", "r") as arquivo_clientes:
        for linha in arquivo_clientes:
            if telefone in linha:
                print("Telefone já cadastrado. Insira um número diferente.")
                menu()
                return
            
    with open("clientes.txt", "a") as arquivo_clientes:
        arquivo_clientes.write(f"Nome: {nome}, CPF: {cpf}, Telefone: {telefone}\n")
        print("Cliente cadastrado com sucesso!")
    menu()

def menuAgendamentos():
    opcao_agendamento = input('''
===========================================
          MENU DE AGENDAMENTOS
          
[1] Inserir novo agendamento
[2] Voltar ao menu principal
===========================================  
ESCOLHA UMA OPÇÃO ACIMA   
''')
    if opcao_agendamento == "1":
        inserirAgendamento()
    elif opcao_agendamento == "2":
        menu()
    else:
        print("OPÇÃO INVÁLIDA ESCOLHA '1 OU 2'")
        menuAgendamentos()
        return
    
def inserirAgendamento(cpf=None):
    if cpf is None:
        cpf = input("Digite o CPF do cliente: ")

    data = input("Digite a data do agendamento (formato: DD/MM/AAAA): ")
    hora = input("Digite a hora do agendamento (formato: HH:MM): ")
    servico = input("Digite o serviço a ser agendado: ")

    hoje = datetime.datetime.now()
    data_agendamento = datetime.datetime.strptime(data, "%d/%m/%Y")
    semana_atual = hoje.strftime("%U")
    semana_agendamento = data_agendamento.strftime("%U")

    with open("agendamentos.txt", "a") as arquivo_agendamentos:
        arquivo_agendamentos.write(f"CPF: {cpf}, Data: {data}, Hora: {hora}, Serviço: {servico}\n")
        print("Agendamento salvo com sucesso!")
    return
    
    with open("agendamentos.txt", "r") as arquivo_agendamentos:
                for linha in arquivo_agendamentos:
                    if f"Data: {data}, Hora: {hora}" in linha:
                        print("Atenção: Já existe um agendamento para o mesmo horário.")
                        menu()
                        return
                    elif f"CPF: {cpf}, Data: {data}, Hora: {hora}" in linha:
                        print("Atenção: Já existe um agendamento para o mesmo cliente nesta semana.")
                        print(f"Sugira que os serviços sejam agendados na mesma data ({data}).")
                        return

    with open("agendamentos.txt", "a") as arquivo_agendamentos:
        arquivo_agendamentos.write(f"CPF: {cpf}, Data: {data}, Hora: {hora}, Serviço: {servico}\n")
        print("Agendamento salvo com sucesso!")
        return

def visualizarAgendamentos():
    try:
        with open("agendamentos.txt", "r") as arquivo:
            agendamentos = arquivo.read()
            print("\nAgendamentos:")
            print(agendamentos)
            menu()
    except FileNotFoundError:
        print("Nenhum agendamento encontrado.")


def editarAgendamento(cpf, nova_data, nova_hora):
    agendamentos = []
    try:
        with open("agendamentos.txt", "r") as arquivo:
            for linha in arquivo:
                agendamento_info = linha.split(", ")
                agendamento = {"CPF": agendamento_info[0].split(": ")[1],
                               "Data": agendamento_info[1].split(": ")[1],
                               "Hora": agendamento_info[2].split(": ")[1]}
                agendamentos.append(agendamento)
    except FileNotFoundError:
        print("Nenhum agendamento encontrado.")

    for agendamento in agendamentos:
        if agendamento["CPF"] == cpf:
            data_agendamento = datetime.datetime.strptime(agendamento["Data"], "%d/%m/%Y")
            hoje = datetime.datetime.now()
            diferenca_dias = (data_agendamento - hoje).days
            if diferenca_dias >= 2:
                agendamento["Data"] = nova_data
                agendamento["Hora"] = nova_hora
                with open("agendamentos.txt", "w") as arquivo:
                    for ag in agendamentos:
                        arquivo.write(f"Nome do Cliente: {ag['CPF']}, Data: {ag['Data']}, Hora: {ag['Hora']}\n")
                print("Agendamento atualizado com sucesso!")
            else:
                print("Alterações só podem ser feitas com antecedência de pelo menos 2 dias, para realiza-la ligue ao estabelecimento.")
            menu()
            return
    print("Agendamento não encontrado.")
    menu()

def main():
    menu()

main()
