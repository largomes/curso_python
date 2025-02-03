import os
from abc import ABC, abstractmethod
from datetime import datetime

# Classe base Quarto
class Quarto(ABC):
    def __init__(self, numero: int, tipo: str, preco: float):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.reservado = False
        self.nome_cliente = None  # Nome do cliente
        self.contato_cliente = None  # Contato do cliente
        self.check_in = None
        self.check_out = None
        self.check_out_realizado = False
        self.nif_cliente = None  # NIF do cliente

    @abstractmethod
    def info(self):
        pass

    def reservar(self, cliente_nome, cliente_contato, check_in_str, check_out_str):
        if not self.reservado:
            self.reservado = True
            self.nome_cliente = cliente_nome  # Atribuir o nome do cliente
            self.contato_cliente = cliente_contato  # Atribuir o contato do cliente
            self.check_in = datetime.strptime(check_in_str, "%Y-%m-%d")  # Converter para data a partir da string
            self.check_out = datetime.strptime(check_out_str, "%Y-%m-%d")  # Converter para data a partir da string
            return f"Quarto {self.numero} reservado com sucesso para {cliente_nome}. Data de Check-in: {self.check_in.strftime('%Y-%m-%d')}, Data de Check-out: {self.check_out.strftime('%Y-%m-%d')}"
        return f"Quarto {self.numero} já está reservado."

    def liberar(self):
        if self.reservado:
            valor_total = self.calcular_total()  # Calcular o total da estadia
            gestao.total_fundo += valor_total  # Adicionar ao fundo de caixa
            self.nif_cliente = input("Por favor, insira o NIF do cliente: ")  # Solicitar o NIF do cliente
            self.gerar_recibo(valor_total)  # Gerar o recibo
            self.reservado = False
            self.nome_cliente = None
            self.contato_cliente = None
            self.check_out_realizado = True
            return f"Quarto {self.numero} foi liberado. Total a pagar: €{valor_total:.2f}"
        return f"Quarto {self.numero} não está reservado."

    def calcular_total(self):
        if self.check_in and self.check_out:
            estadia = self.check_out - self.check_in
            dias = estadia.days + 1  # Incluir o dia do check-in
            return self.preco * dias
        return 0.0

    def gerar_recibo(self, valor_total):
        dias_estadia = (self.check_out - self.check_in).days + 1
        print("\n--- Recibo de Check-out ---")
        print(f"Quarto: {self.numero}")
        print(f"Tipo: {self.tipo}")
        print(f"Preço por noite: €{self.preco}")
        print(f"Cliente: {self.nome_cliente}")
        print(f"Contato: {self.contato_cliente}")  # Exibindo o contato do cliente
        print(f"NIF: {self.nif_cliente}")  # Exibindo o NIF do cliente
        print(f"Data Check-in: {self.check_in.strftime('%Y-%m-%d')}")
        print(f"Data Check-out: {self.check_out.strftime('%Y-%m-%d')}")
        print(f"Nº de dias de estadia: {dias_estadia} dias")
        print(f"Total: €{valor_total:.2f}")
        print("-" * 30)

# Classe QuartoSimples
class QuartoSimples(Quarto):
    def info(self):
        return f"Quarto {self.numero}: Simples, Preço: €{self.preco}, {'Reservado' if self.reservado else 'Disponível'}"

# Classe QuartoDuplo
class QuartoDuplo(Quarto):
    def info(self):
        return f"Quarto {self.numero}: Duplo, Preço: €{self.preco}, {'Reservado' if self.reservado else 'Disponível'}"

# Classe de Gestão de Quartos
class GestaoQuartos:
    def __init__(self):
        self.quartos = []
        self.total_fundo = 0.0  # Variável para armazenar o total em caixa
        self.check_ins = 0
        self.check_outs = 0

    def adicionar_quarto(self, quarto: Quarto):
        self.quartos.append(quarto)
        print(f"\nQuarto {quarto.numero} criado com sucesso!")
        print("_" * 100)
        print("Listagem de quartos criados:")
        print("_" * 100)
        self.exibir_tabela_quartos()  # Exibe a tabela com os quartos após adicionar
        #self.registrar_movimento("Adição", quarto.numero)

    def exibir_tabela_quartos(self):
        print("\n{:<10} | {:<15} | {:<15} | {:<10}".format("Nº de Quarto", "Tipo", "Preço", "Status"))
        print("_" * 100)
        for quarto in self.quartos:
            print("{:<12} | {:<15} | €{:<14} | {:<10}".format(quarto.numero, quarto.tipo, quarto.preco,
                                                              'Reservado' if quarto.reservado else 'Disponível'))

    def listar_quartos(self):
        print("\n{:<10} | {:<15} | {:<15} | {:<10}".format("Nº de Quarto", "Tipo", "Preço", "Status"))
        print("-" * 70)
        for quarto in self.quartos:
            print("{:<10} | {:<15} | €{:<15} | {:<10}".format(quarto.numero, quarto.tipo, quarto.preco, 'Reservado' if quarto.reservado else 'Disponível'))

    def listar_reservas(self):
        print("\n{:<10} | {:<15} | {:<30} | {:<15} | {:<15}".format("Nº Quarto", "Tipo", "Cliente", "Check-in", "Check-out"))
        print("-" * 100)
        for quarto in self.quartos:
            if not quarto.reservado:
                print(" Sem reservas registadas...")
            else:                
                if quarto.reservado:
                    print("{:<10} | {:<15} | {:<30} | {:<15} | {:<15}".format(quarto.numero, quarto.tipo, quarto.nome_cliente, quarto.check_in.strftime("%Y-%m-%d"), quarto.check_out.strftime("%Y-%m-%d")))

    def reservar_quarto(self, numero_quarto, cliente_nome, cliente_contato, check_in_str, check_out_str):
        quarto = self.encontrar_quarto(numero_quarto)
        if quarto:
            resultado = quarto.reservar(cliente_nome, cliente_contato, check_in_str, check_out_str)
            self.check_ins += 1  # Incrementar o número de check-ins
            self.registrar_movimento("Reserva", quarto.numero)
            return resultado
        return "Erro: Quarto não encontrado."

    def liberar_quarto(self, numero_quarto):
        quarto = self.encontrar_quarto(numero_quarto)
        if quarto:
            resultado = quarto.liberar()
            self.check_outs += 1  # Incrementar o número de check-outs
            self.registrar_movimento("Check-out", quarto.numero)
            return resultado
        return "Erro: Quarto não encontrado."

    def encontrar_quarto(self, numero_quarto):
        for quarto in self.quartos:
            if quarto.numero == numero_quarto:
                return quarto
        return None

    def numero_reservas(self):
        return sum(1 for quarto in self.quartos if quarto.reservado)

    def numero_check_ins(self):
        return self.check_ins

    def numero_check_outs(self):
        return self.check_outs

    def ocupacao(self):
        return (self.numero_reservas() / len(self.quartos)) * 100 if self.quartos else 0.0

    def alterar_reserva(self, numero_quarto):
        quarto = self.encontrar_quarto(numero_quarto)
        if quarto and quarto.reservado:
            print(f"Reserva do Quarto {quarto.numero} para {quarto.nome_cliente}:")
            novo_check_in = input("Nova data de Check-in (AAAA-MM-DD): ")
            novo_check_out = input("Nova data de Check-out (AAAA-MM-DD): ")
            
            # Alterando as datas
            quarto.check_in = datetime.strptime(novo_check_in, "%Y-%m-%d")
            quarto.check_out = datetime.strptime(novo_check_out, "%Y-%m-%d")
            self.registrar_movimento("Alteração de Reserva", quarto.numero)
            return f"Reserva do Quarto {quarto.numero} foi alterada com sucesso.\nNovo Check-in: {quarto.check_in.strftime('%Y-%m-%d')}, Novo Check-out: {quarto.check_out.strftime('%Y-%m-%d')}"
        
        elif quarto and not quarto.reservado:
            return f"Erro: O Quarto {quarto.numero} não está reservado!"
        
        return f"Erro: Quarto {numero_quarto} não encontrado."

    def cancelar_reserva(self, numero_quarto):
        quarto = self.encontrar_quarto(numero_quarto)
        if quarto and quarto.reservado:
            quarto.reservado = False
            quarto.nome_cliente = None
            quarto.contato_cliente = None
            quarto.check_in = None
            quarto.check_out = None
            quarto.check_out_realizado = False
            self.registrar_movimento("Cancelamento de Reserva", quarto.numero)
            return f"Reserva do Quarto {quarto.numero} cancelada com sucesso!"
        return f"Erro: Quarto {numero_quarto} não encontrado ou não está reservado!"

    def registrar_movimento(self, acao, numero_quarto):
        # Registra a ação realizada em arquivo
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("movimentos_quartos.txt", "a") as arquivo:
            arquivo.write(f"{data_atual} - Ação: {acao} | Quarto: {numero_quarto}\n")

    def menu(self):
        while True:
            print("_" * 100)
            print(f"\n{' Bem vindo ao Sistema de Registo de Reservas '.center(90)}")
            print("_" * 100)
            print(f"\n{'Dados Recolhidos ate ao momento :'.center(100)}")
            print("_" * 100)
            print(f"\nNº Quartos Existentes: {len(self.quartos)} | Check-ins: {self.numero_check_ins()} | Check-outs: {self.numero_check_outs()} | Total de Ocupação: {self.ocupacao():.2f}%")
            print("_"*100)
            print(f"\nTotal em caixa: €{self.total_fundo:.2f}")
            print("_" * 100)
            print(f"\n{'  M E N U '.center(60)}")
            print("_" * 40)
            print("\n1. Adicionar Quarto")
            print("2. Listar Quartos")
            print("3. Listar Reservas")
            print("4. Fazer check-in ")
            print("5. Fazer check-out")
            print("6. Cancelar Reserva")
            print("7. Alterar Reserva")
            print("8. Sair")
            print("_" * 40)

            try:
                opcao = input("Escolha uma opção: ").strip()
                print("_" * 40)

                if opcao == '1':
                    while True:
                        numero = int(input("Número do quarto: "))

                        # Verificar duplicidade logo após o número ser inserido
                        for q in self.quartos:
                            if q.numero == numero:
                                print(f"Erro: Já existe um quarto com o número {numero}!")
                                break  # Se o quarto já existir, sai do loop de verificação e pede novamente o número
                        else:  # Se não encontrar um número duplicado, continua
                            break
                    tipo = input("Tipo de quarto (Simples/Duplo): ").capitalize()
                    preco = float(input("Preço do quarto: "))
                    if tipo == 'Simples':
                        quarto = QuartoSimples(numero, tipo, preco)
                    elif tipo == 'Duplo':
                        quarto = QuartoDuplo(numero, tipo, preco)
                    else:
                        print("Tipo inválido!")
                        continue
                    self.adicionar_quarto(quarto)
                    
                elif opcao == '2':
                    print("Listagem de quartos:")
                    self.listar_quartos()
                elif opcao == '3':
                    print("Listagem de reservas registadas:")
                    self.listar_reservas()
                elif opcao == '4':
                    numero = int(input("Número do quarto para check-in: "))
                    cliente_nome = input("Nome do cliente: ")
                    cliente_contato = input("Contato do cliente: ")
                    check_in_str = input("Data de Check-in (AAAA-MM-DD): ")
                    check_out_str = input("Data de Check-out (AAAA-MM-DD): ")
                    print(self.reservar_quarto(numero, cliente_nome, cliente_contato, check_in_str, check_out_str))
                elif opcao == '5':
                    numero = int(input("Número do quarto para check-out: "))
                    print(self.liberar_quarto(numero))
                elif opcao == '6':
                    numero = int(input("Número do quarto para cancelar reserva: "))
                    print(self.cancelar_reserva(numero))
                elif opcao == '7':
                    numero = int(input("Número do quarto para alterar reserva: "))
                    print(self.alterar_reserva(numero))
                elif opcao == '8':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Erro: Entrada inválida. Tente novamente.")
if __name__ == '__main__':
    gestao = GestaoQuartos()
    gestao.menu()                
