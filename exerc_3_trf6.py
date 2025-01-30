#exerc_3

def salvar_ficheiro(nome_ficheiro, alunos, nota_minima=10):
    try:
        with open(nome_ficheiro, 'w') as file:
            for aluno in alunos:
                nome, nota = aluno
                # Determinar se o aluno está aprovado ou reprovado
                status = 'Aprovado' if nota >= nota_minima else 'Reprovado'
                # Salvar os dados no formato: nome, nota, status
                file.write("Lista de alunos e respetivas notas\n")
                file.write("_" * 30 + "\n")  # Linha de separação
                file.write(f"{nome}, {nota}, {status}\n")
                file.write("_" * 30 + "\n")  # Linha de separação 
        print(f"Dados salvos com sucesso no ficheiro {nome_ficheiro}!")
    except Exception as e:
        print(f"Erro ao salvar o ficheiro: {e}")

def ler_ficheiro(nome_ficheiro):
    alunos = []
    try:
        with open(nome_ficheiro, 'r') as file:
            for linha in file:
                # Dividir o nome, a nota e o status usando a vírgula
                nome, nota, status = linha.strip().split(',')
                alunos.append((nome.strip(), float(nota.strip()), status.strip()))
    except FileNotFoundError:
        print(f"Erro: O ficheiro {nome_ficheiro} não foi encontrado.")
    return alunos

def calcular_media(notas):
    return sum(notas) / len(notas) if notas else 0

def aluno_com_melhor_nota(alunos):
    melhor_nota = max(alunos, key=lambda aluno: aluno[1])[1]
    alunos_com_melhor_nota = [aluno[0] for aluno in alunos if aluno[1] == melhor_nota]
    return alunos_com_melhor_nota, melhor_nota

def alunos_aprovados(alunos):
    aprovados = [aluno[0] for aluno in alunos if aluno[2] == 'Aprovado']
    return aprovados

def main():
    alunos = []

    # Coletar dados dos alunos até o usuário escolher parar
    while True:
        nome = input("Digite o nome do aluno (ou 'sair' para finalizar): ")
        if nome.lower() == 'sair':
            break
        nota = float(input(f"Digite a nota de {nome}: "))
        alunos.append((nome, nota))
    
    # Salvar os dados no ficheiro
    nome_ficheiro = "notas.txt"
    salvar_ficheiro(nome_ficheiro, alunos)

    # Ler o ficheiro para processar os dados
    alunos_lidos = ler_ficheiro(nome_ficheiro)
    
    if alunos_lidos:
        # Listar todas as notas
        notas = [aluno[1] for aluno in alunos_lidos]
        
        # Calcular a média
        media = calcular_media(notas)
        print(f"\nA média das notas da turma é: {media:.2f}")
        
        # Identificar o(s) aluno(s) com a melhor nota
        melhor_nota_alunos, melhor_nota = aluno_com_melhor_nota(alunos_lidos)
        print(f"O(s) aluno(s) com a melhor nota ({melhor_nota}) é(são): {', '.join(melhor_nota_alunos)}")
        
        # Identificar os alunos aprovados
        aprovados = alunos_aprovados(alunos_lidos)
        print(f"Alunos aprovados: {', '.join(aprovados)}")
    else:
        print("Não há dados para processar.")

if __name__ == "__main__":
    main()
