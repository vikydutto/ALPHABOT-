# crezione del file per la brute force
import random, string 

f = open("./prova.txt", "w")
letters = string.ascii_letters + "1234567890"
# length = 3

# print(len(letters)**3) # combinazioni
    #    print(letters) # stringa di tutte le lettere maiuscole e minuscole + numeri
for ifuori in range(len(letters)):
    for giro in range(len(letters)):
        for fuori in range(len(letters)):
            stringa = letters[len(letters)-fuori-1]
            stringa = stringa + letters[len(letters)-giro-1]
            stringa = stringa + letters[len(letters)-ifuori-1]
            #print(stringa)
            f.write(f"{stringa}\n")
f.close()
f  = open("./prova.txt", "r")
righe = f.readlines()
"""
print(f"riga {righe[1]}")
print(f"{len(righe)} dovrebbe essere giusto, ovvero il numero di combinazioni, ma le combinazioni sono giuste?"
      + "\n INCREDIBILMENTE LO SONO, SIGNORIIII!!!")
"""

for i, riga in enumerate(righe):
    #print(riga + "-")
    righe[i] = riga[:-1]
    #print(righe[i] + "-")
#print("riga di prova: " + righe[1] + "-")

scontrol, r, continua = "aaa", 0, True # lo faccio partire da 1 perché so benissimo che la pri,a scontrol _è_ la prima stringa dell'elenco
# quindi faccio poi attenmzione a mettere <= nel while

while continua & (r < len(letters)**3):
    if scontrol != righe[r]:
        # print("entro nel for -> riga:" + righe[r] + ", r: " + str(r) + ", scontrol: " + scontrol + "\n")
        scontrol= righe[r]
        r += 1
        # print(righe[r] + "-  e poi " + str(r))
        # lo aumento per poi fare il cambio della stringa da confrontare
        # print(f"no errore: {c}, siamo a {scontrol} e {stringa[c]} STIAMO ANDANDO FORTEEEE")
    else: 
        continua = False
        print(f"\n >> errore a {scontrol} con {righe[r]}")
    if r % 200 == 0: print("sono a quesa riga" + str(r))

if continua: print("Pacca sulla spalla che hai il brute force!")
else: print("fi solo un po' schifo eh, ma solo perché oggi sono clemente!")
# C:\Users\paola\Documents\SCUOLA\FRANCY\V!!!\TPSIT\FLASK\AB\FLASK
