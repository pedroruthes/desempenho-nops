import os
solucao_1 = []
solucao_2 = []

def hexadecimal_binario(linha):
    conversao = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }

    binario = ""

    for caractere in linha:
        binario += conversao.get(caractere.upper(), "") # Pega o caractere correspondente ao objeto "conversao" e adicione na string binario o seu valor correspondente

    return binario     

def tipo_instrucao(linha, segundaLinha, terceiraLinha, solucao):
    instrucao = linha[-7:]
    rd = linha[-12:-7]

    segunda_instrucao = segundaLinha[-7:]
    segunda_rs1 = segundaLinha[-20:-15]
    segunda_rs2 = segundaLinha[-25:-20]

    terceira_rs1 = terceiraLinha[-20:-15]
    terceira_rs2 = terceiraLinha[-25:-20]

    solucao_1.append(linha)
    solucao_2.append(linha)

    if instrucao == "0010011" or instrucao == "0000011": # instrucao == I ARITMÉTICO ou instrucao == LOAD WORD
        if segunda_instrucao == "1101111" or segunda_instrucao == "1100111": # segunda_instrucao == JAL ou segunda_instrucao == JALR
            solucao_1.append('00000000000000000000000000010011 - NOP')
        else:
            if rd == segunda_rs1 or rd == segunda_rs2: # registrador_destino == rs1_proxima_linha ou registrador_destino == rs2_proxima_linha
                solucao_1.append('00000000000000000000000000010011 - NOP')
                solucao_1.append('00000000000000000000000000010011 - NOP')

                if instrucao == "0000011":
                    solucao_2.append('00000000000000000000000000010011 - NOP')

            elif rd == terceira_rs1 or rd == terceira_rs2: # registrador_destino == rs1_terceira_linha ou registrador_destino == rs2_terceira_linha
                solucao_1.append('00000000000000000000000000010011 - NOP')
    

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

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCONFLITO DE DADOS NO PIPELINE\n")
    print("Feito por:")
    print("- Nicolas dos Santos Renaux")
    print("- Pedro Henrique Camargo Ruthes\n")

    clock = input("Informe o tempo de relógio (CLOCK) em nanossegundos: ") # Tempo de CLOCK do programa
    caminho_arquivo = 'arquivos/binario' # Caminho do arquivo a ser lido
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

if __name__ == "__main__":
    main()