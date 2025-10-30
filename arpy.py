# Arpy v. 0.5

# configurazione del sistema. Deve essere uguale tra Arduino e Python

# velocità di comunicazione
BAUD = 9600

# chi è il device master ?
# Il device master chiama l'altro device che può solo rispondere
MASTER = 1
# 1=Python
# 0=Arduino

# porta cui è collegato l'Arduino
# copiare da quello usato in Arduino IDE
PORT = 'COM5'

isThereSomeone = False
#########################################


import serial
import threading
import time



# Apriamo la porta seriale
ser = serial.Serial(PORT, BAUD, timeout=1)

# Funzione da chiamare per inviare un comando ad Arduino
def cmdOut(c, n):
    msg = f"{c}{n}\n"
    ser.write(msg.encode('utf-8'))
    # se master è python,  aspettiamo un attimo per dar modo all'arduino di rispondere se vuole
    if (MASTER==1):
        time.sleep(0.05)

# Funzione che viene chiamata quando Arduino manda un comando
def cmdIn(c, n):
    # print(f"Ricevuto da Arduino: {c}{n}")
    # cambiare qui per fare cose diverse in base al comando ricevuto


    if (c=='V'):
        if(n>500):
            isThereSomeone = True
            print("ginocchio")
        else:
            print("nulla")
        # print(f"Valore potenziometro: {n}")
        # Esempio se master è Arduino (MASTER = 0)
        #if(n>900):
        #    cmdOut('Z',1)
        #else:
        #    cmdOut('Z',0)
    return isThereSomeone

# non cambiare: legge dalla porta seriale in background
def serial_reader():
    buffer = ""
    while True:
        if ser.in_waiting:
            char = ser.read().decode('utf-8')

            if char == '\n':
                if len(buffer) >= 2:
                    c = buffer[0]
                    try:
                        n = int(buffer[1:])
                        cmdIn(c, n)
                    except ValueError:
                        print(f"Errore nel parsing del numero in '{buffer}'")
                buffer = ""
            else:
                buffer += char


# inizio programma

# Avviamo la lettura dalla seriale
threading.Thread(target=serial_reader, daemon=True).start()



while True:
    # Esempio: comandi di prova (da fare solo se MASTER=1)
    # L1 e L0: accendono e spengono  il led sul pin13
    cmdOut('L', 1)
    print("on")
    time.sleep(0.1)
    cmdOut('L', 0)
    print("off")
    time.sleep(0.1)

    # P0: chiede all'arduino il valore del potenziometro (se esiste :-) )
    cmdOut('P', 0)
    # Arduino risponderà con Vnnn dove nnn è il valore letto dal potenziometro

