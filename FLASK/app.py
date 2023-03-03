from flask import Flask, render_template, request, redirect, url_for
from imaplib import Int2AP

import socket
from threading import Thread
import time, sqlite3
import RPi.GPIO as GPIO
import random, string

# f|2 == 1 metro last time we used it #
meter = 2
curva90 = 0.48
tempoComando = 1
letters = string.ascii_letters + "1234567890"

class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26, time=1):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stopNoT()

    def forward(self): # va "indietro": la sinistra gira di meno
        self.PWMA.ChangeDutyCycle(50) # guardandolo quando va avanti: ruota sx
        self.PWMB.ChangeDutyCycle(58.7)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stopNoT(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self): # va "avanti"
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def left(self, speed=30): # 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self, speed=30): # 
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def contaTempo(tempoComando, start):
    timeMesured = 0
    while timeMesured < tempoComando:
        now = time.time()
        timeMesured = now - start
        
def creaURL():
    length=30
    stringa = ""
#    print(letters) # stringa di tutte le lettere maiuscole e minuscole + numeri
    for i in range(length):
        #print(random.choice(letters))
        stringa = stringa + random.choice(letters)
    return "/" + stringa

def creaPSW():
    length = 3
    stringa = ""
    #    print(letters) # stringa di tutte le lettere maiuscole e minuscole + numeri
    for i in range(length):
            #print(random.choice(letters))
            stringa = stringa + random.choice(letters)
    print(stringa)
    
def bruteforceFORSEok(): # lultimo che ho fatto in filBruteForce.py
    f = open("./bruteForce.txt", "w")
    for ifuori in range(len(letters)):
        for giro in range(len(letters)):
            for fuori in range(len(letters)):
                stringa = letters[len(letters)-fuori-1]
                stringa = stringa + letters[len(letters)-giro-1]
                stringa = stringa + letters[len(letters)-ifuori-1]
                #print(stringa)
                f.write(f"{stringa}\n")
    f.close()

def bruteForce(): # forse funziona fileBruteFprce sul file prova.txt
    f = open("./bruteForce.txt", "w")
    length = 3

    for ifuori in range(len(letters)):
        for giro in range(len(letters)):
            for fuori in range(len(letters)):
                stringa = letters[len(letters)-fuori-1]
                #print(stringa)
                for i in range(length-2):
                    #print(i)
                    stringa = stringa + letters[len(letters)-giro-1]
                    #print(stringa)
                    for l in range(length-2):
                        stringa = stringa + letters[len(letters)-ifuori-1]
                        #print(stringa)
                        f.write(f"{stringa}\n")
    #print(len(letters)**3)
        

app = Flask(__name__)

def validate(username, password):
    completion = False
    con = sqlite3.connect('./db.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        #print(row)
        dbUser = row[1]
        dbPass = row[2] # avendo messo anche l'id dobbiamo prendere la seconda e la terza colonna
        if dbUser == username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password 
    # la password hashata non sarà mai uguakle alla password inserita e 
    # per il momento noi la teniamo !hashata

#------------------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST']) # -> primo decoratore: associa un url con una funzione di python
def login():
    error = None
    if request.method == 'POST': # ovviamente glielo mando nel post così passa crittografata in rete
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

#-------------------------------------------------------------------------------

@app.route(creaURL(), methods=['GET', 'POST'])
def secret():
    Ab = AlphaBot()
    start = time.time() # riprende il time
    if request.method == 'POST': #  chiedo al server con la post: perché gli input li do sempre in post, con la get NO
        #print(request.form.get('sx')) # prendo il bottone sx
        if request.form.get('sx') == 'sinistra': # preno il comando dal sito e se è ... allora
            print("SINISTRA")  
            comando = "l"    
            Ab.left()
            contaTempo(tempoComando, start)    
        elif  request.form.get('dx') == 'destra':
            print("DESTRA")       
            comando = "r" 
            Ab.right()
            contaTempo(tempoComando, start) # gira a dx
        if request.form.get('su') == 'sopra':
            print("SU")
            comando = "f" 
            Ab.forward()
            contaTempo(tempoComando, start)
        elif  request.form.get('giu') == 'sotto':
            print("GIU'")
            comando = "b" 
            Ab.backward()
            contaTempo(tempoComando, start)
        else:
            print("Unknown")
        Ab.stop()     # proprio per questo io ho scritto solo index.html
    return render_template('index.html') # su flask io non devo scriverci nulla, lui ha già un "template" diposizioni delle cartelle e dei files al loro interno
                                             # qindi devo seguire questo template di cartelle
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


#                  C:\Users\paola\Documents\SCUOLA\FRANCY\V!!!\TPSIT\FLASK\AB\FLASK


#                  http://192.168.1.112:5000/
"""
    pagina segreta: @approute("/secret")
    def secret():
        return "this is the pulcinella's secret!" -> ecco la pagina a cui si accede dopo il login
    
    apreoute('/' (action), methods{get, post}) -> a seconda del metodo faccio delle cose diverse
    ...
        if post: prende username e psw (2 stringhe)
        devo fare dei controlli su queste robe: funzione valudate (def validate())
    ...return;
    
    aggiungiamo una tabella 2 nel db. nomeutente (univoco), psw, + chiave primarie sottoforma di autoincrement
    
                nel login.html
                {% if error %}
                bla bla bla
                {% endif  %}
    
    
    redirect(url_for("nome della funzione")) -> il nome "secret" == fa il redirect sulla pagina segreta!
    
    al posto della url /secret: ci possiamo mettere una stinga generata dall'algoritmo completamente a caso
    """
    
""" password di 3 caratteri alfanumerici (lettere dell'alfabeto inglese e numeri)"""
