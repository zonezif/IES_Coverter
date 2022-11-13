import numpy as np
import matplotlib.pyplot as plt
import os

filt = 0.1
angulo = 1


def coord(data, angle):

    ex = angle
    defase = ex+int(len(data)/2)
    if (defase > len(data)-1):
        defase = defase-len(data)

    if (ex > len(data)-1):
        ex = ex-len(data)

    vet = data[defase]

    vet = vet[0:len(vet)-1]

    vet2 = data[ex]

    vet2 = vet2[0:len(vet2)-1]

    val = []
    l = len(vet2)

    for i in vet:
        val.append(float(i))

    for i in range(len(vet2)):
        val.append(float(vet2[l-1-i]))
    return val


def cord(data, angle):

    ex = angle
    defase = ex+int(len(data)/2)
    if (defase > len(data)-1):
        defase = defase-len(data)

    if (ex > len(data)-1):
        ex = ex-len(data)

    vet = data[defase]

    vet = vet[0:len(vet)-1]

    vet2 = data[ex]

    vet2 = vet2[0:len(vet2)-1]

    val = []
    l = len(vet2)

    for i in vet:
        val.append(float(i))

    for i in range(len(vet2)):
        val.append(float(vet2[l-1-i]))
    return vet


def angles():
    x1 = list(range(90, 180, 10))
    x2 = sorted(x1, key=int, reverse=True)
    x3 = list(range(10, 90, 10))
    x4 = sorted(x3, key=int, reverse=True)
    x = x1+[180]+x2+x4+[0]+x3

    return x


def abrir(name, nick):

    with open(name, "r") as f:
        reader = f.read()

    x = reader
    x = x.splitlines()

    data = ""
    cabeçalho = []

    for i in range(len(x)):
        if (x[i] == 'TILT=NONE'):
            for j in x[i+1:]:
                data += j
                cabeçalho = x[:i+3]
            break
    dic = {}

    for i in cabeçalho:
        if (len(i.split()) > 1):
            dic[i.split()[0]] = i.split(']')[1:]

    if (nick == 0):
        data = data[:]
        return data

    if (nick == 1):
        data = data[4:len(data)-1]
        return data

    if (nick == 2):
        return (dic)

    if (nick == 3):
        return (cabeçalho)


def distr(vet2, vet1):
    val = []
    l = len(vet2)
    for i in vet1[:len(vet1)-1]:
        val.append(float(i))

    for i in range(len(vet2)-1):
        val.append(float(vet2[l-1-i]))

    return val


def rad(vet):
    rads = []
    x = range(len(vet))
    for i in x:
        rads.append(float(i)*np.pi/180-np.pi/2)
    return rads


def med(data):
    sum = 0
    for i in data:
        sum += float(i)
    return sum/len(data)


def difere(dd1, dd2):
    P = 0
    for ang in range(int(len(dd1)/2)):
        d1 = coord(dd1, ang)
        d2 = coord(dd2, ang)

        result = []

        for i in range(len(coord(dd1, ang))):
            if (d1[i] > (med(d1)*filt) and d2[i] > med(d2)*filt):
                result.append(abs((((d1[i]+0.01)/(d2[i]+0.01))-1)*100))
            else:
                result.append(0)
        sum = 0

        for i in result:
            sum += i
        P += sum/len(result)

    P = P/12
    return P


class IES(object):

    def __init__(self, arq):
        self.x = abrir(arq, 0).split(" ")
        self.off = 0

        AngV = [0]
        self.off = int(self.Nang())+11

        for i in self.x[12:self.off]:
            AngV.append(float(i))

        self.angv = AngV

        AngH = []
        for i in self.x[self.off:int(self.Nah())+self.off]:
            AngH.append(float(i))
        self.angh = AngH

        Cd = []

        self.off += int(self.Nah())

        for j in range(int(self.Nah())):
            cd = []
            for i in self.x[self.off:int(self.Nang())+self.off]:
                cd.append(float(i))
            self.off += int(self.Nang())
            Cd.append(cd)
        self.Xd = Cd

        self.dic = abrir(arq, 2)

        self.top = abrir(arq, 3)

    def Lm(self):
        return float(self.x[1])  # Fluxo

    def Fat(self):
        return float(self.x[2])  # Fator de multiplicação

    def Nang(self):
        return self.x[3]  # Numeros de angulos da teia

    def Nah(self):
        return self.x[4]  # numero de angulos horizontais

    def Unid(self):
        return self.x[6]  # Unidade 1 para pes 2 para metros

    def AngV(self):
        return self.angv

    def AngH(self):
        return self.angh

    def Cd(self):
        return self.Xd

    def Dic(self):
        return self.dic

    def Top(self):
        return self.top


def convert(arq):

    print('convertendo...> ' + arq + ' >>>'+'IES_' + arq)

    ies1 = IES(arq)

    result = []
    ignor = []

    dd1 = ies1.Cd()
    top = ies1.Top()
    av = ies1.AngV()
    ah = ies1.AngH()
    # print(dd1[0][int(ies1.Nang())-1])

    arquivo = open('./out/'+'IES_'+arq, 'w', encoding='utf-8')
    m = 0
    arquivo.write('IESNA:LM-63-2002\n')

    for i in top[1:]:
        arquivo.write(i+'\n')

    for i, j in zip(av, range(len(av))):
        arquivo.write(str(i)+' ')
        arquivo.write((" "*(8-len(str(i)))))
        if ((j+1) % 10 == 0):
            arquivo.write('\n')

    arquivo.write('\n')

    for i, j in zip(ah, range(len(ah))):
        arquivo.write(str(i)+' ')
        arquivo.write((" "*(8-len(str(i)))))
        if ((j+1) % 10 == 0):
            arquivo.write('\n')

    arquivo.write('\n')

    for l in range(len(dd1)):

        for i, j in zip(dd1[l], range(int(ies1.Nang()))):
            arquivo.write(str(i)+' ')
            arquivo.write((" "*(8-len(str(i)))))
            if ((j+1) % 10 == 0):
                arquivo.write('\n')

        arquivo.write('\n')
    arquivo.close()


key = 's'

while (key == 's'):
    dire = input("\nArraste a pasta aqui!!").replace('\"', '')
    os.system('cls')
    dire = dire.replace('\'', '')
    dire = dire.replace('&', '')
    if (dire[0] == " "):
        dire = dire[1:]
    print(dire)
    os.chdir(dire)

    page = os.getcwd()
    lista = os.listdir(page)
    IESs = []
    cwd = page

    for i in lista:
        arq = i.split('.')
        if (len(arq) > 1):
            if arq[1] == 'ies':
                if (arq[0].count('IES_') != 1):
                    IESs.append(i)

    if (os.path.exists('out') != 1):
        os.makedirs(page+'//out')
        page += page+'//out'

    # convert('m2.ies')
    u = 0
    for i in IESs:
        convert(i)
        u += 1

    print('\n', u, 'Arquivos convertidos')
