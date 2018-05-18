import random

class Comptador:    
    def __init__(self,inici=0,maxim=9999999):
        self.valor=inici
        self.tope=maxim
    def inicialitzar(self):
        self.valor=0
    def incrementar(self):
        if self.valor<self.tope:
            self.valor=self.valor+1
    def decrementar(self):
        self.valor=self.valor-1
    def consulta(self):
        return self.valor
    def eszero(self):
        return self.valor>0
    def imprimir(self):
        print(self.valor)
    def dividir_per_2(self):
        self.valor=self.valor//2

class Pkmn:
    Dic={}
    def __init__(self,punts=0):
        self.punts=punts

    def guarda_pkmn(nom,punts):
        Pkmn.Dic[nom]=Pkmn(punts)
        
    def sumar_punts(nom,ronda):
        if ronda=='Vuitens':
            Pkmn.Dic[nom].punts+=2
        elif ronda=='Quarts':
            Pkmn.Dic[nom].punts+=4
        elif ronda=='Semifinal':
            Pkmn.Dic[nom].punts+=8
        elif ronda=='Final':
            Pkmn.Dic[nom].punts+=10
        elif ronda=='win':
            Pkmn.Dic[nom].punts+=15
            
    def actualitzar_punts():
        f=open('pkbr.txt','w')
        l=''
        for e in Pkmn.Dic:
            l=str(e)+' '+str(Pkmn.Dic[e].punts)+'\n'
            f.write(l)
        f.close()   
                

def crea_seed():
    seed=[]
    seed1=[]
    seed2=[]
    seed3=[]
    seed4=[]
    seed5=[]
    for i in range(0,32):
        a=str(random.randint(0,31))
        while a in seed1:
            a=str(random.randint(0,31))
        seed1.append(a)
    for i in range(0,16):
        a=str(random.randint(0,15))
        while a in seed2:
            a=str(random.randint(0,15))
        seed2.append(a)
    for i in range(0,8):
        a=str(random.randint(0,7))
        while a in seed3:
            a=str(random.randint(0,7))
        seed3.append(a)
    for i in range(0,4):
        a=str(random.randint(0,3))
        while a in seed4:
            a=str(random.randint(0,3))
        seed4.append(a)
    seed=seed1+seed2+seed3+seed4
    seed=' '.join(seed)
    return seed

def crea_ronda(l,seed,c):
    l2=[]
    x=c.consulta()
    i=0
    while i<len(l):
        a=int(seed[x])
        if l[a]!=0:
            l2.append(l[a])
        i+=1
        x+=1
    return l2

def batalles(ll,txt,c):
    x=1
    llwin=[]
    i=0
    win=''
    while i<len(ll) and win!='p':
        if txt=='Final':
            print(txt+':',ll[i],'vs',ll[i+1])
        else:
            print(txt,str(x)+':',ll[i],'vs',ll[i+1])
        x+=1
        win=input('Guanyador? ')
        if win=='1':
            llwin.append(ll[i])
            Pkmn.sumar_punts(ll[i+1],txt)
        elif win=='2':
            llwin.append(ll[i+1])
            Pkmn.sumar_punts(ll[i],txt)
        i+=2
        c.incrementar()
        c.incrementar()
    if win=='p':
        return '*'
    else:
        return llwin
def classi():
    d={}
    f=open('pkbr.txt','r')
    for e in f:
        r=e.split(' ')
        d[r[0]]=int(r[1])
    r=list(d.items())
    r.sort(key=lambda x: x[1])
    r.reverse()
    for i in range(0,len(r)):
        print(str(i+1)+'.',r[i][0]+':',str(r[i][1])+'pts')
    f.close()

opcio=int(input('1.Crear nou\n2.Continuar\n'))
c=Comptador()
if opcio==1:
    seed=crea_seed()
    seed=seed.split(' ')
else:
    f=open('seed.txt','r')
    seed=f.readline()
    seed=seed.split(' ')
    f.close()
ll=[]
f=open('pkbr.txt','r')
for e in f:
    e=e.split(' ')
    ll.append(e[0])
    Pkmn.guarda_pkmn(e[0],int(e[1]))
f.close()  
print('SETZENS DE FINAL:')
setz=crea_ronda(ll,seed,c)
sdef=batalles(setz,'Setzens',c)
if sdef=='*':
    f=open('seed.txt','w')
    f.write(' '.join(seed))
    f.close()
else:
    print('VUITENS DE FINAL:')
    vuit=crea_ronda(sdef,seed,c)
    vdef=batalles(vuit,'Vuitens',c)
    if vdef=='*':
        f=open('seed.txt','w')
        f.write(' '.join(seed))
        f.close()
    else:
        print('QUARTS DE FINAL:')
        quar=crea_ronda(vdef,seed,c)
        qdef=batalles(quar,'Quarts',c)
        if qdef=='*':
            f=open('seed.txt','w')
            f.write(' '.join(seed))
            f.close()
        else:
            print('SEMIFINALS:')
            semi=crea_ronda(qdef,seed,c)
            sedef=batalles(semi,'Semifinal',c)
            if sedef=='*':
                f=open('seed.txt','w')
                f.write(' '.join(seed))
                f.close()
            else:
                print('FINAL:')
                champ=batalles(sedef,'Final',c)
                print('El guanyador és:',champ[0])
                Pkmn.sumar_punts(champ[0],'win')

try:                         
    if vdef!='*' and qdef!='*' and sedef!='*' and champ!='*':
        Pkmn.actualitzar_punts()
except NameError:
    Pkmn.actualitzar_punts()
classi()

