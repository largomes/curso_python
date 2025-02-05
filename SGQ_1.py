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
        
    def calcular_total(self):
        if self.check_in and self.check_out:
            estadia = self.check_out - self.check_in
            dias = estadia.days + 1  # Incluir o dia do check-in
            return self.preco * dias
        return 0.0
    
    def gerar_recibo(self, valor_total):
        dias_estadia = (self.check_out - self.check_in).days + 1
        print("\n--- Recibo de Check-out ---")
    
    # Garantir que os dados do cliente estão preenchidos antes de gerar o recibo
        if not self.nome_cliente or not self.contato_cliente:
            print("Informações do cliente não encontradas! Solicitando dados...")
            print("_"*40)
            self.nome_cliente = input("Por favor, insira o nome do cliente: ")
            self.contato_cliente = input("Por favor, insira o contato do cliente: ")
            print("_"*40)
            print(f"Quarto: {self.numero}")
            print(f"Tipo: {self.tipo}")
            print(f"Preço por noite: €{self.preco}")
            print(f"Cliente: {self.nome_cliente}")
            print(f"Contato: {self.contato_cliente}")  # Exibindo o contato do cliente
            print(f"NIF: {self.nif_cliente}")  # Exibindo o NIF do cliente
            print(f"Data Check-in: {self.check_in.strftime('%Y-%m-%d')}")
            print(f"Data Check-out: {self.check_out.strftime('%Y-%m-%d')}")
            print(f"Nº de dias de estadia: {dias_estadia} dias")
            print("_"*40)
            print(f"Total: €{valor_total:.2f}")
            print("_" * 40)

    # Perguntar se o usuário deseja salvar o recibo em arquivo
            salvar = input("Deseja salvar o recibo em um arquivo? (S/N): ").strip().upper()
            if salvar == 'S':
                self.salvar_recibo_em_arquivo(valor_total)
        
    def salvar_recibo_em_arquivo(self, valor_total):
        dias_estadia = (self.check_out - self.check_in).days + 1
        with open("recibo.txt", "w") as mostra:
            mostra.write("_"*30)
            mostra.write("\n--- Recibo de Check-out ---\n")
            mostra.write("_"*30)
            mostra.write(f"\nQuarto: {self.numero}\n")
            mostra.write(f"Tipo: {self.tipo}\n")
            mostra.write(f"Preço por noite: €{self.preco}\n")
            mostra.write(f"Cliente: {self.nome_cliente}\n")
            mostra.write(f"Contato: {self.contato_cliente}\n")
            mostra.write(f"NIF: {self.nif_cliente}\n")
            mostra.write(f"Data Check-in: {self.check_in.strftime('%Y-%m-%d')}\n")
            mostra.write(f"Data Check-out: {self.check_out.strftime('%Y-%m-%d')}\n")
            mostra.write(f"Nº de dias de estadia: {dias_estadia} dias\n")
            mostra.write("_"*30)
            mostra.write(f"\nTotal: €{valor_total:.2f}\n")
            mostra.write("_" * 30)

    @abstractmethod
    def info(self):
        pass

    def reservar(self, cliente_nome, cliente_contato, check_in_str, check_out_str):
        if not self.reservado:
            # Validação das datas
            try:
                check_in = datetime.strptime(check_in_str, "%Y-%m-%d")
                check_out = datetime.strptime(check_out_str, "%Y-%m-%d")
                
                if check_in >= check_out:
                    return "Erro: A data de Check-out deve ser posterior à data de Check-in."

            except ValueError:
                return "Erro: O formato da data deve ser AAAA-MM-DD."

            self.reservado = True
            self.nome_cliente = cliente_nome
            self.contato_cliente = cliente_contato
            self.check_in = check_in
            self.check_out = check_out
            return f"Quarto {self.numero} reservado com sucesso para {cliente_nome}. Data de Check-in: {self.check_in.strftime('%Y-%m-%d')}, Data de Check-out: {self.check_out.strftime('%Y-%m-%d')}"
        
        return f"Quarto {self.numero} já está reservado."

    
    def libertar(self):
        if self.reservado:
            valor_total = self.calcular_total()  # Calcular o total da estadia
            gestao.total_fundo += valor_total  # Adicionar ao fundo de caixa
         
        if not self.nif_cliente:
            self.nif_cliente = input("Por favor, insira o NIF do cliente: ")  # Solicitar o NIF do cliente
        
        if not self.nome_cliente or not self.contato_cliente:
            # Solicitar informações faltantes (nome e contato)
            self.nome_cliente = input("Por favor, insira o nome do cliente: ")
            self.contato_cliente = input("Por favor, insira o contato do cliente: ")
        
            self.reservado = False
            self.check_out_realizado = True
            self.registrar_movimento("Check-out", self.numero)
        
            return f"Quarto {self.numero} foi liberado. Total a pagar: €{valor_total:.2f}"
    
        return f"Quarto {self.numero} não está reservado."
    def calcular_total(self):
        if self.check_in and self.check_out:
            estadia = self.check_out - self.check_in
            dias = estadia.days + 1  # Incluir o dia do check-in
            return self.preco * dias
        return 0.0   
 
# Classe QuartoSimples
class QuartoSimples(Quarto):
    def info(self):
        return f"Quarto {self.numero}: Simples, Preço: €{self.preco}, {'Reservado' if self.reservado else 'Disponível'}"

# Classe QuartoDuplo
class QuartoDuplo(Quarto):
    def info(self):
        return f"Quarto {self.numero}: Duplo, Preço: €{self.preco}, {'Reservado' if self.reservado else 'Disponível'}"
#classe gestora dos sistema
class GestaoQuartos:
    def __init__(self):
        self.quartos = []
        self.total_fundo = 0.0  # Variável para armazenar o total em caixa
        self.check_ins = 0
        self.check_outs = 0

    def registrar_movimento(self, acao, numero_quarto):
        # Registra a ação realizada em arquivo, formatado como tabela
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("movimentos_quartos.txt", "a") as arquivo:
            # Tentar adicionar cabeçalho se for o primeiro movimento
            if os.stat("movimentos_quartos.txt").st_size == 0:
                arquivo.write(f"{'Data':<20} | {'Ação':<20} | {'Número do Quarto':<20}\n")
                arquivo.write("-" * 60 + "\n")
            
            arquivo.write(f"{data_atual:<20} | {acao:<20} | {numero_quarto:<20}\n")
    
# função para adicionar os quartos
    def adicionar_quarto(self, quarto: Quarto):
        self.quartos.append(quarto)
        print(f"\nQuarto {quarto.numero} criado com sucesso!")
        print("_" * 100)
        print("Listagem de quartos criados:")
        print("_" * 100)
        self.exibir_tabela_quartos()  # Exibe a tabela com os quartos após adicionar
#exebição da tabela de quartos criados
    def exibir_tabela_quartos(self):
        print("\n{:<10} | {:<15} | {:<15} | {:<10}".format("Nº de Quarto", "Tipo", "Preço", "Status"))
        print("_" * 100)
        for quarto in self.quartos:
            print("{:<12} | {:<15} | €{:<14} | {:<10}".format(quarto.numero, quarto.tipo, quarto.preco,
                                                              'Reservado' if quarto.reservado else 'Disponível'))
# função para a opção 2 - listar quartos
    def listar_quartos(self):
        print("\n{:<10} | {:<15} | {:<15} | {:<10}".format("Nº de Quarto", "Tipo", "Preço", "Status"))
        print("_" * 100)
        for quarto in self.quartos:
            print("{:<10} | {:<15} | €{:<15} | {:<10}".format(quarto.numero, quarto.tipo, quarto.preco, 'Reservado' if quarto.reservado else 'Disponível'))
## função para a opção 3 - listar reservas efetudas
    def listar_reservas(self):
        print("\n{:<10} | {:<15} | {:<30} | {:<15} | {:<15}".format("Nº Quarto", "Tipo", "Cliente", "Check-in", "Check-out"))
        print("_" * 100)
        for quarto in self.quartos:
            if not quarto.reservado:
                print(" Sem reservas registadas...")
            else:
                if quarto.reservado:
                    print("{:<10} | {:<15} | {:<30} | {:<15} | {:<15}".format(quarto.numero, quarto.tipo, quarto.nome_cliente, quarto.check_in.strftime("%Y-%m-%d"), quarto.check_out.strftime("%Y-%m-%d")))
#função para reservar quarto
    def reservar_quarto(self, numero_quarto, cliente_nome, cliente_contato, check_in_str, check_out_str):
        quarto = self.encontrar_quarto(numero_quarto)  # Verificar se o quarto existe
        if quarto:
         # O quarto existe, agora tenta realizar a reserva
            resultado = quarto.reservar(cliente_nome, cliente_contato, check_in_str, check_out_str)
            self.check_ins += 1  # Incrementar o número de check-ins
            # insere no ficheiro a termo " ocupado" apos ser feito o check-in
            self.registrar_movimento("Ocupado", quarto.numero)
            return resultado
        else:
        # Caso o quarto não exista
            return f"Erro: Quarto nº:{numero_quarto}, que esta a tentar reservar não foi encontrado."
        
#libertar quarto e visualizar o recibo na consola
    def libertar_quarto(self, numero_quarto):
        quarto = self.encontrar_quarto(numero_quarto)
        if quarto:
            if quarto.reservado:  # Verifica se o quarto está reservado
                valor_total = quarto.calcular_total()  # Calcula o total
                self.total_fundo += valor_total  # Adiciona o valor ao fundo de caixa
                quarto.nif_cliente = input("Por favor, insira o NIF do cliente: ")  # Solicita o NIF
                quarto.reservado = False  # Libera o quarto
                quarto.nome_cliente = None
                quarto.contato_cliente = None
                quarto.check_out_realizado = True
                self.check_outs += 1  # Incrementa o número de check-outs
                self.registrar_movimento("Disponivel", quarto.numero)  # Registra o movimento
                # Chama a função gerar_recibo para exibir o recibo na consola
                quarto.gerar_recibo(valor_total)
                return f"Quarto {quarto.numero} esta disponivel a partir deste momento. Total a pagar: €{valor_total:.2f}"
            else:
                return f"Quarto {quarto.numero} não está reservado."
        return "Erro: Quarto não encontrado ou não existente, voltando ao menu principal."
    
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
#calcula a percentagem de ocupação 
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
# função para cancelamento da reserva
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
#funçõa para criar o menu
    def menu(self):
        while True:
            print("_" * 100)
            print(f"\n{' Bem vindo ao Sistema de Registo de Reservas '.center(90)}")
            print("_" * 100)
            print(f"\nDados Recolhidos ate ao momento :")
            print("_" * 100)
            print(f"\n| Nº Quartos Existentes: {len(self.quartos)} | Check-ins: {self.numero_check_ins()} | Check-outs: {self.numero_check_outs()} | Total de Ocupação: {self.ocupacao():.2f}%               |")
            print("_"*100)
            print(f"\nTotal em caixa: {self.total_fundo:.2f}€")
            print("_" * 100)
            print(f"\n{' |               M E N U                |'.center(30)}")
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
                    
                    while True:
                        try:
                           preco = float(input("Preço por noite: " ))
                           if preco <= 0:
                              print("Erro: O preço deve ser maior que 0. Tente novamente.")
                           else:
                              break  # Preço válido
                        except ValueError:
                           print("Erro: Entrada inválida para o preço. Por favor, insira um número válido.")
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
                    print("_" *100)
                    self.listar_quartos()
                                       
                elif opcao == '3':
                    print("Listagem de reservas registadas:")
                    self.listar_reservas()
                    
                elif opcao == "4":
                    numero_quarto = int(input("Número do Quarto para Check-in: "))
                    quarto = gestao.encontrar_quarto(numero_quarto)
                    if not quarto:
                        print(f"Erro: Quarto {numero_quarto} não encontrado, voltando ao menu principal !")
                        continue
                    cliente_nome = input("Nome do cliente: ")
                    cliente_contato = input("Contato do cliente: ")
                    check_in_str = input("Data de Check-in (AAAA-MM-DD): ")
                    check_out_str = input("Data de Check-out (AAAA-MM-DD): ")
                    print(gestao.reservar_quarto(numero_quarto, cliente_nome, cliente_contato, check_in_str, check_out_str))
                    
                elif opcao == '5':
                    numero = int(input("Número do quarto para check-out: "))
                    print(self.libertar_quarto(numero))
                    
                elif opcao == '6':
                    numero = int(input("Número do quarto para cancelar reserva: "))
                    print(self.cancelar_reserva(numero))
                    
                elif opcao == '7':
                    numero = int(input("Número do quarto para alterar reserva: "))
                    print(self.alterar_reserva(numero))
                    
                elif opcao == '8':
                    print("Fechando sistema...")
                    break
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Erro: Entrada inválida. Tente novamente.")
if __name__ == "__main__":
    gestao = GestaoQuartos()
    gestao.menu()

