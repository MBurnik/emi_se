# https://drive.google.com/file/d/1315Oi2hdC0ozh-WcBsprIQYyCfqN4KeM/view?usp=drive_link
# Michał Burnicki 264411

import math
import matplotlib.pyplot as plt


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Funkcje

def calculateN(l, d, n, S):
    c = math.sqrt((pow(d+l, 2) - pow((l/2)+(d/2), 2)))
    e = c - l
    border = d
    z = ((d+(l/2))*math.sqrt(3))/2

    mPerEvenRow = math.floor((x-(2*border)+d)/(l+d))
    mPerOddRow = math.floor((x-(2*border)+(d/2)+(l/2)-(2*d))/(l+d))

    mPerCollumn = math.floor((y-(2*z)+e)/(l+e))

    if (mPerCollumn%2):
        N = (mPerEvenRow * (math.ceil(mPerCollumn/2))) + (mPerOddRow * (math.floor(mPerCollumn/2)))
    else:
        N = (mPerEvenRow * (mPerCollumn/2)) + (mPerOddRow * (mPerCollumn/2))

    return N, mPerEvenRow, mPerOddRow, mPerCollumn

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dane wejściowe

f = 4110                            # częstotliwość w MHz
x = 0.5                             # wymiar x płyty w metrach
y = 0.5                             # wymiar y płyty w metrach
SMin = 15                           # minimalna skuteczność tłumienia w dB
precision = 0.00001                 # precyzja z jaką bedą przeliczane dane w metrach


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Część przeliczająca

lamda = 300/f                       # długość fali w metrach
lMin = 0.00001                      # minimalny wymiar liniowy otworu w metrach
dMin = lamda/10                     # minimalna wartość odstępu pomiędzy otworami w metrach

nMax = math.floor((lamda-(2*dMin))/(2*(lMin+dMin)))  # maksymalna ilość otworów w rzędzie

print("nMax =", nMax)

lList = []
dList = []
nList = []
SList = []
PList = []
NList = []
mPerEvenRowList = []
mPerOddRowList = []
mPerCollumnList = []


# Dla n = 1
n = 1
d = lamda/4
l = lamda/(2*pow(10, SMin/20))
S = SMin
N, mPerEvenRow, mPerOddRow, mPerCollumn = calculateN(l, d, n, S)
lList.append(l)
dList.append(d)
nList.append(n)
SList.append(S)
NList.append(N)
P = math.pi*pow(l/2, 2)*N
PList.append(P)
mPerEvenRowList.append(mPerEvenRow)
mPerOddRowList.append(mPerOddRow)
mPerCollumnList.append(mPerCollumn)


# Dla n > 1
n = 2
while (n <= nMax):
    d = dMin

    while (d <= (lamda/((n+1)*2))):
        l = (lamda-(2*d*(n+1)))/(2*n)
        S = 20*(math.log((lamda/(2*l*math.sqrt(n))), 10))

        if (S >= SMin):
            N, mPerEvenRow, mPerOddRow, mPerCollumn = calculateN(l, d, n, S)
            lList.append(l)
            dList.append(d)
            nList.append(n)
            SList.append(S)
            NList.append(N)
            P = math.pi*pow(l/2, 2)*N
            PList.append(P)
            mPerEvenRowList.append(mPerEvenRow)
            mPerOddRowList.append(mPerOddRow)
            mPerCollumnList.append(mPerCollumn)

        d += precision
    
    n += 1


# Wyszukanie optymlanych wartości
PMax = max(PList)
index = PList.index(PMax)

lOpt = lList[index]
dOpt = dList[index]
nOpt = nList[index]
SFinal = SList[index]
N = NList[index]
mPerEvenRow = mPerEvenRowList[index]
mPerOddRow = mPerOddRowList[index]
mPerCollumn = mPerCollumnList[index]

print("Optimal values:")
print("l =", lOpt)
print("d =", dOpt)
print("n =", nOpt)
print("S =", SFinal)
print("N =", N)
print("P =", PMax)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Część wyświetlająca

plt.axes()

square = plt.Rectangle((0, 0), x, y, fc='None', ec='black')

ax = plt.gca()
ax.add_patch(square)

k = 0
offset = False
e = math.sqrt(pow(dOpt+lOpt, 2) - pow((lOpt/2)+(dOpt/2), 2)) - lOpt
print("e =", e)
z = ((dOpt+(lOpt/2))*math.sqrt(3))/2 - (lOpt/2)
print("z =", z)

border = dOpt

if (mPerEvenRow == mPerOddRow):
    xCord = ((x - ((mPerEvenRow*lOpt) + ((mPerEvenRow-1)*dOpt) + (dOpt/2) - (lOpt/2) + (2*border)))/2) + (lOpt/2) + border
else:
    xCord = ((x - ((mPerEvenRow*lOpt) + ((mPerEvenRow-1)*dOpt) + (2*border)))/2) + (lOpt/2) + border

yCord = ((y - (((mPerCollumn*lOpt)) + ((mPerCollumn-1)*e) + (2*z)))/2) + (lOpt/2) + z

print("Distance to first hole xcord =", xCord - lOpt)
print("Distance to first hole ycord =", yCord - lOpt)

while k < mPerCollumn:
    i = 0
    if (offset == False):
        offset = True
        while i < mPerEvenRow:
            ax.add_patch(plt.Circle((xCord + ((dOpt+lOpt)*i), yCord + ((lOpt+e)*k)), lOpt/2, fc='None', ec='blue'))
            i += 1
    else:
        offset = False
        while i < mPerOddRow:
            ax.add_patch(plt.Circle((xCord + (lOpt/2)+(dOpt/2) + ((dOpt+lOpt)*i), yCord + ((lOpt+e)*k)), lOpt/2, fc='None', ec='blue'))
            i += 1
    k += 1

plt.axis('scaled')
plt.axis('off')

#plt.xlim(-0.01, 0.15)    #0.415, 0.51
#plt.ylim(-0.01, 0.15)    #-0.01, 0.085

plt.show()