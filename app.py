import os

def hexadecimal_binario(linha):
    conversao = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }

    binario = ""

    for caractere in linha:
        binario += conversao.get(caractere.upper(), "")

    return binario         

def reorganizar_instrucoes(solucao):
    solucao_nova = []

    for i in range(len(solucao)):
        aritmetico = solucao[i][-7:] == "0010011"
        load_word = solucao[i][-7:] == "0000011"

        if aritmetico or load_word:
            for j in range(i, 0, -1):
                ja_ou_jalr = solucao[j - 1][-7:] == "1101111" or solucao[i - 1][-7:] == "1100111"
                aritmetico_acima = solucao[j - 1][-7:] == "0010011"
                load_word_acima = solucao[j - 1][-7:] == "0000011"
                
                if ja_ou_jalr or aritmetico_acima or load_word_acima:
                    break
                else:
                    temp = solucao[j]
                    solucao[j] = solucao[j - 1]
                    solucao[j - 1] = temp

    for i in range(len(solucao)):
        if solucao[i] != "00000000000000000000000000010011 - NOP":
            solucao_nova.append(solucao[i])

    return solucao_nova

def adicionar_nops_forwarding(vetor):
    solucao = []

    for i in range(len(vetor)):

        if i + 1 > len(vetor) - 1:
            segundaLinha = ""
        else:
            segundaLinha = vetor[i + 1]

        primeiraLinha = vetor[i] if all(c in '01' for c in vetor[i].strip()) else hexadecimal_binario(vetor[i])
        segundaLinha = segundaLinha if all(c in '01' for c in vetor[i].strip()) else hexadecimal_binario(segundaLinha)

        instrucao = primeiraLinha[-7:]
        rd = primeiraLinha[-12:-7]

        segunda_instrucao = segundaLinha[-7:]
        segunda_rs1 = segundaLinha[-20:-15]
        segunda_rs2 = segundaLinha[-25:-20]

        solucao.append(primeiraLinha)

        if instrucao == "0010011" or instrucao == "0000011":
            if segunda_instrucao != "1101111" or segunda_instrucao != "1100111":
                if rd == segunda_rs1 or rd == segunda_rs2:
                    if instrucao == "0000011":
                        solucao.append('00000000000000000000000000010011 - NOP')

    return solucao

def adicionar_nops(vetor):
    solucao = []

    for i in range(len(vetor)):

        if i + 1 > len(vetor) - 1:
            segundaLinha = ""
        else:
            segundaLinha = vetor[i + 1]

        if i + 2 > len(vetor) - 1:
            terceiraLinha = ""
        else:
            terceiraLinha = vetor[i + 2]

        primeiraLinha = vetor[i] if all(c in '01' for c in vetor[i].strip()) else hexadecimal_binario(vetor[i])
        segundaLinha = segundaLinha if all(c in '01' for c in vetor[i].strip()) else hexadecimal_binario(segundaLinha)
        terceiraLinha = terceiraLinha if all(c in '01' for c in vetor[i].strip()) else hexadecimal_binario(terceiraLinha)

        instrucao = primeiraLinha[-7:]
        rd = primeiraLinha[-12:-7]

        segunda_instrucao = segundaLinha[-7:]
        segunda_rs1 = segundaLinha[-20:-15]
        segunda_rs2 = segundaLinha[-25:-20]

        terceira_rs1 = terceiraLinha[-20:-15]
        terceira_rs2 = terceiraLinha[-25:-20]

        solucao.append(primeiraLinha)

        if instrucao == "0010011" or instrucao == "0000011":
            if segunda_instrucao == "1101111" or segunda_instrucao == "1100111":
                solucao.append('00000000000000000000000000010011 - NOP')
            else:
                if rd == segunda_rs1 or rd == segunda_rs2:
                    solucao.append('00000000000000000000000000010011 - NOP')
                    solucao.append('00000000000000000000000000010011 - NOP')

                elif rd == terceira_rs1 or rd == terceira_rs2:
                    solucao.append('00000000000000000000000000010011 - NOP')

    return solucao

def desempenho(solucao, vetor, clock, i):
    numero_ciclos =  5 + (len(solucao) - 1)

    print("SOLUÇÃO", i)
    print("- Qtd. ciclos: ", numero_ciclos, "ciclos")
    print("- Sobrecusto ciclos:", numero_ciclos - (5 + (len(vetor) - 1)), "ciclos")
    print("- Tempo de execução:", numero_ciclos * clock," nanossegundos")
    print("- Sobrecusto execução:", (numero_ciclos * clock) - ((5 + (len(vetor) - 1)) * clock), "nanossegundos")
    print("- CPI médio:", "{:.2f}".format(numero_ciclos / len(solucao)))
    print("\n")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCONFLITO DE DADOS NO PIPELINE\n")
    print("Feito por:")
    print("- Nicolas dos Santos Renaux")
    print("- Pedro Henrique Camargo Ruthes\n")

    clock = float(input("Informe o tempo de relógio (CLOCK) em nanossegundos: "))
    caminho_arquivo = 'arquivos/binario'
    vetor = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            vetor.append(linha.strip())

        solucao_1 = adicionar_nops(vetor)
        solucao_2 = adicionar_nops_forwarding(vetor)
    
    solucao_3 = adicionar_nops(reorganizar_instrucoes(solucao_1))
    solucao_4 = adicionar_nops_forwarding(reorganizar_instrucoes(solucao_2))

    with open('solucoes/solucao_1', 'w') as arquivo:
        for i in range(len(solucao_1)):
            arquivo.write(solucao_1[i] + "\n")
    
    with open('solucoes/solucao_2', 'w') as arquivo:
        for i in range(len(solucao_2)):
            arquivo.write(solucao_2[i] + "\n")

    with open('solucoes/solucao_3', 'w') as arquivo:
        for instrucao in solucao_3:
            arquivo.write(instrucao + "\n")

    with open('solucoes/solucao_4', 'w') as arquivo:
        for instrucao in solucao_4:
            arquivo.write(instrucao + "\n")

    print("\nSOLUÇÕES NO PIPELINE\n")

    desempenho(solucao_1, vetor, clock, 1)
    desempenho(solucao_2, vetor, clock, 2)
    desempenho(solucao_3, vetor, clock, 3)
    desempenho(solucao_4, vetor, clock, 4)

if __name__ == "__main__":
    main()