import matlab.engine
import os
from random import randint

print("Initializing Matlab and preparing files. Please wait...")

# Creates directory to save bode diagrams and .txt file
if not os.path.exists('.\\Bode_diagrams'):
    os.makedirs('.\\Bode_diagrams')
os.chdir('.\\Bode_diagrams')

# Opens .txt file, the Matlab engine
txtFile = open('Transfer_Functions.txt', 'a')
eng = matlab.engine.start_matlab()
eng.eval("s = tf('s');", nargout=0)


print("Matlab initialized successfully!")
print("\n--------Bode diagrams generator v1.1--------")
TFCount = int(input("Enter the desired number of transfer functions: "))
TFOrder = int(input("Enter maximum order for the transfer function: "))
PoleZeroLimit = 20
KpLimit = 20
print("Generating the transfer functions and their diagrams. Please wait...")

# Function that a pole or zero in (s + p) where maximum p is defined by variable 'limit'
def createPoleZeroZPK(separator,limit):
    location = randint(0,limit)
    poleZero = ""
    if location == 0:
        poleZero = separator + "s"
    else:
        poleZero =  separator + "(s + " + str(location) + ")"
    return poleZero


# Function that generates transfer function in the format Kp*(s + z1)*...*(s + zi)/(s + p1)*...*(s + pi)
# Order is the maximum order of both numerator and denominator
# KpLimit is the maximum Kp of the transfer function

def generateTF(order):
    Kp = randint(1,KpLimit)
    numerator = str(Kp)
    denominator = str(1)
    numeratorOrder = randint(0,order)
    denominatorOrder = randint(0,order)

    if numeratorOrder != 0:
        parentheses = numeratorOrder != 1
        if Kp == 1:
            numerator = createPoleZeroZPK("",PoleZeroLimit)
            numeratorOrder -= 1
        for n in range(numeratorOrder):
            numerator = numerator + createPoleZeroZPK("*",PoleZeroLimit)
        if parentheses:
            numerator = "(" + numerator + ")"
    if numerator == "(s)":
        numerator = "s"

    if denominatorOrder != 0:
        denominator = createPoleZeroZPK("",PoleZeroLimit)
        for d in range(denominatorOrder-1):
            denominator = denominator + createPoleZeroZPK("*",PoleZeroLimit)
    if denominatorOrder > 1:
        denominator = "(" + denominator + ")"
    if denominator == "(s)":
        denominator = "s"

    if denominator == "1":
        transferFunction = numerator
    else:
        transferFunction = numerator + "/" + denominator
    return transferFunction


# Generates random transfer function, registers it in the .txt file and generate bode diagram with Matlab engine
# After generating the Bode diagram, saves it as bode_X.png (where X is the transfer function number)
for i in range(TFCount):
    transferFunction = generateTF(TFOrder)
    txtFile.write(str(i+1) + " - " + transferFunction + "\n")
    print("G = " + transferFunction + ";")
    eng.eval("G = tf(" + transferFunction + ");", nargout=0)
    eng.eval("bode(G);", nargout=0)
    eng.eval("saveas(gcf,'bode_" + str(i+1) + ".png');", nargout=0)

# End of program, closes Matlab and .txt file
print("\nBode diagrams generated with success! (They are in directory 'Bode_diagrams')")
eng.quit()
eng = None
txtFile.close()
print("<End of program. Press any keyboard to exit.>")
input()
