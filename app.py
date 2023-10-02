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

def tipo_instrucao(linha, segundaLinha, terceiraLinha):
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

        for i in range(len(vetor)):

            if i + 1 > len(vetor) - 1:
                segundaLinha = ""
            else:
                segundaLinha = vetor[i + 1]

            if i + 2 > len(vetor) - 1:
                terceiraLinha = ""
            else:
                terceiraLinha = vetor[i + 2]


            if all(c in '01' for c in linha.strip()): # Verifica se a linha lida contêm somente os valores 0 e 1
                tipo_instrucao(vetor[i], segundaLinha, terceiraLinha)
            else:
                tipo_instrucao(hexadecimal_binario(vetor[i]), hexadecimal_binario(segundaLinha), hexadecimal_binario(terceiraLinha))

    with open('solucoes/solucao_1', 'w') as arquivo:
        for i in range(len(solucao_1)):
            arquivo.write(solucao_1[i] + "\n")
    
    with open('solucoes/solucao_2', 'w') as arquivo:
        for i in range(len(solucao_2)):
            arquivo.write(solucao_2[i] + "\n")
    
    solucao_3 = solucao_1.copy()
    
    for i in range(len(solucao_1) - 1):
        achou_jal = solucao_1[i - 1][-7:] == "1101111"  or solucao_1[i - 1][-7:] == "1100111"
        utiliza_rd = solucao_1[i][-20:-15] == solucao_1[i - 3][-12:-7] or solucao_1[i][-25:-20] == solucao_1[i - 3][-12:-7] and solucao_1[i - 3][-7:] == "0010011" or solucao_1[i - 3][-7:] == "0000011"
        utiliza_rs = solucao_1[i - 1][-20:-15] == solucao_1[i][-12:-7] or solucao_1[i - 1][-25:-20] == solucao_1[i][-12:-7]

        atual = solucao_1[i]
        modificar = True
        count = 0

        if solucao_1[i + 1] == "00000000000000000000000000010011 - NOP" and solucao_1[i + 2] ==  "00000000000000000000000000010011 - NOP":

            for j in range(i, 0, -1):
                if solucao_1[j - 1] == "00000000000000000000000000010011 - NOP" or achou_jal or utiliza_rd or utiliza_rs:
                    if solucao_1[j - 1] == "00000000000000000000000000010011 - NOP":
                        modificar = False
                        solucao_3[j - 1] = atual
                        del solucao_3[i]
                        break
                    break

                count += 1
                            
            if count >= 2 and modificar:
                solucao_3.insert(i - count, atual)

                del solucao_3[i + 1]
                del solucao_3[i + 2]
            elif count == 1 and modificar:
                solucao_3.insert(i - count, atual)
                del solucao_3[i + 1]

        elif solucao_1[i + 1] == "00000000000000000000000000010011 - NOP" and solucao_1[i] != "00000000000000000000000000010011 - NOP":

            for j in range(i, 0, -1):
                if solucao_1[j - 1] == "00000000000000000000000000010011 - NOP" or achou_jal or utiliza_rd or utiliza_rs:
                    if solucao_1[j - 1] == "00000000000000000000000000010011 - NOP":
                        modificar = False
                        solucao_3[j - 1] = atual
                        del solucao_3[i]
                        break

                    break
                count += 1

            if count >= 1 and modificar:
                solucao_3.insert(i - count, atual)
                del solucao_3[i + 1]
    
    with open('solucoes/solucao_3', 'w') as arquivo:
        for i in range(len(solucao_3)):
            arquivo.write(solucao_3[i] + "\n")

if __name__ == "__main__":
    main()

# 1 PASSO: PEGAR A INSTRUÇÃO ATUAL E VERIFICAR SE ELE TEM UM OU DOIS NOP APÓS ELA (CERTO)
# 2 PASSO: SE TIVER NOP, DEVE JOGAR A INSTRUÇÃO ATUAL PARA CIMA ATÉ ACHAR UM JALR/JAL OU NOP
# 3 PASSO: VERIFICAR QUANTAS CASAS PARA CIMA ELE SUBIU E EXCLUIR A QUANTIDADE DE NOPS (POR EXEMPLO: SUBIU UMA CASA, TIRA UM NOP)
# 4 PASSO: CASO ELE SUBA ATÉ ACHAR UM NOP, DEVE TIRAR TAMBÉM O NOP ACIMA DELE

# OBS: PARA FAZER ESSAS SUBIDAS, DEVE VERIFICAR SE O RD DA INSTRUÇÃO ATUAL NÃO É UTILIZADA PELO RD, RS1 OU RS2 DA INSTRUÇÃO ACIMA