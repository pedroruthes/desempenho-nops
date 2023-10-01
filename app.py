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

def tipo_instrucao(linha, segundaLinha, terceiraLinha):
    instrucao = linha[-7:]
    rd = linha[-12:-7]

    segunda_instrucao = segundaLinha[-7:]
    segunda_rs1 = segundaLinha[-20:-15]
    segunda_rs2 = segundaLinha[-25:-20]

    terceira_rs1 = terceiraLinha[-20:-15]
    terceira_rs2 = terceiraLinha[-25:-20]

    print(linha + "  " + segundaLinha + "  " + terceiraLinha)

    # if instrucao == "0110011":
    #     print('R')
    # elif instrucao == "1100011":
    #     print('B')
    # elif instrucao == "0100011":
    #     print('S')
    # elif instrucao == "0010011":
    #     print('ARITMETICO - I')
    # elif instrucao == "0000011":
    #     print('LOAD - I')
    # elif instrucao == "1110011":
    #     print('ECALL - I')
    # elif instrucao == "1101111":
    #     print('JALR - I')

    if instrucao == "0010011" or instrucao == "0000011":
        if segunda_instrucao == "1101111" or segunda_instrucao == "1100111":
            print('NOP')
        else:
            if rd == segunda_rs1 or rd == segunda_rs2:
                print('NOP')
                print('NOP')
            elif rd == terceira_rs1 or rd == terceira_rs2:
                print('NOP')

def main():
    caminho_arquivo = 'arquivos/binario' # Caminho do arquivo a ser lido
    vetor = []

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            vetor.append(linha.strip())

        for i in range(len(vetor)):

            if i + 1 > len(vetor) - 1:
                segundaLinha = "Não possui esta linha           "
            else:
                segundaLinha = vetor[i + 1]

            if i + 2 > len(vetor) - 1:
                terceiraLinha = "Não possui esta linha"
            else:
                terceiraLinha = vetor[i + 2]


            if all(c in '01' for c in linha.strip()): # Verifica se a linha lida contêm somente os valores 0 e 1
                tipo_instrucao(vetor[i], segundaLinha, terceiraLinha)
            else:
                tipo_instrucao(hexadecimal_binario(vetor[i]), segundaLinha, terceiraLinha)

if __name__ == "__main__":
    main()