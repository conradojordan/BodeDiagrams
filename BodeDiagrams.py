# Importa as bibliotecas necessárias
import matlab.engine
import os
from random import randint


# Avisa usuário que programa começou e está aguardando o Matlab
print("Inicializando Matlab. Por favor aguarde... ")


# Cria o diretório que vai salvar os bodes e o txt
# os.chdir(os.path.join(os.path.expanduser('~'), 'Desktop'))
if not os.path.exists('.\\Diagramas de Bode'):
    os.makedirs('.\\Diagramas de Bode')
os.chdir('.\\Diagramas de Bode')


# Abre o txt e o engine do Matlab e inicializa 's'
arquivoTexto = open('Funções de transferência.txt', 'a')
eng = matlab.engine.start_matlab()
eng.eval("s = tf('s');", nargout=0)


# "Interface" com o usuário
print("Matlab inicializado com sucesso!")
print("\n--------Gerador de diagramas de Bode v1.0--------")
print("Digite a quantidade de funções de transferência desejada:")
numeroDeFTs = int(input())
print("Digite a ordem máxima das funções de transferência:")
ordemDaFT = int(input())
limitePoloZero = 20
limiteKp = 20
print("Gerando as funções de transferência e seus respectivos diagramas. Por favor aguarde...")

# Função para gerar polo ou zero em (s + p) onde p máximo é definido por 'limite'
def criaPoloZeroZPK(separador,limite):
    localizacao = randint(0,limite)
    poloZero = ""
    if localizacao == 0:
        poloZero = separador + "s"
    else:
        poloZero =  separador + "(s + " + str(localizacao) + ")"
    return poloZero


# Função para gerar função de transferência na forma Kp*(s + z1)*...*(s + zi)/(s + p1)*...*(s + pi)
# Ordem é a ordem máxima de ambos o numerador e denominador
# LimiteKp é o Kp máximo da funçao de transferência
def criaFuncao(ordem):
    Kp = randint(1,limiteKp)
    numerador = str(Kp)
    denominador = str(1)
    ordemNumerador = randint(0,ordem)
    ordemDenominador = randint(0,ordem)
    
    if ordemNumerador != 0:
        parentesis = ordemNumerador != 1
        if Kp == 1:
            numerador = criaPoloZeroZPK("",limitePoloZero)
            ordemNumerador -= 1
        for n in range(ordemNumerador):
            numerador = numerador + criaPoloZeroZPK("*",limitePoloZero)
        if parentesis:
            numerador = "(" + numerador + ")"
    if numerador == "(s)":
        numerador = "s"
        
    if ordemDenominador != 0:
        denominador = criaPoloZeroZPK("",limitePoloZero)
        for d in range(ordemDenominador-1):
            denominador = denominador + criaPoloZeroZPK("*",limitePoloZero)
    if ordemDenominador > 1:
        denominador = "(" + denominador + ")"
    if denominador == "(s)":
        denominador = "s"

    if denominador == "1":
        ft = numerador
    else:
        ft = numerador + "/" + denominador
    return ft


# Gera a função de transferência aleatória, registra ela no documento txt e gera o bode no Matlab
# Depois de gerar o Bode, salva a figura como bode_X.png (onde X é o numero da FT)
for i in range(numeroDeFTs):
    funcaoDeTransferencia = criaFuncao(ordemDaFT)
    arquivoTexto.write(str(i+1) + " - " + funcaoDeTransferencia + "\n")
    print("G = " + funcaoDeTransferencia + ";")
    eng.eval("G = tf(" + funcaoDeTransferencia + ");", nargout=0)
    eng.eval("bode(G);", nargout=0)
    eng.eval("saveas(gcf,'bode_" + str(i+1) + ".png');", nargout=0)


# Finalização do programa, fechamento do Matlab e do documento de texto
print("\nDiagramas de Bode gerados com sucesso!! (Estão na pasta 'Diagramas de Bode')")
eng.quit()
eng = None
arquivoTexto.close()
print("<fim>")
