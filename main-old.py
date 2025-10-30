import threading
import serial
import time
import cv2
import pygame
import pyaudio
import wave
import numpy as np
from semaphores import wait_semaphore, set_semaphore, clear_semaphores, check_semaphore
import os
from esegui import esegui
from PIL import Image

NUMEROCAMERA = 1
# 0 sistema, 1 esterno

# se true, sente sempre il ginocchio
EMULASERIALE=True

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


def get_next_output_folder(base_name="output", width=3):
    i = 0
    while True:
        folder_name = f"{i:0{width}d}"  # genera nomi come "000", "001", ecc.
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            return folder_name
        i += 1

# Uso
OUTPUT_FOLDER = get_next_output_folder()
print(f"Salverò i file in: {OUTPUT_FOLDER}")


isThereSomeone = False

fotoFatta = False



#########################################

cap = cv2.VideoCapture(NUMEROCAMERA)

# Apriamo la porta seriale
if not EMULASERIALE:
    ser = serial.Serial(PORT, BAUD, timeout=1)

# Funzione da chiamare per inviare un comando ad Arduino
def cmdOut(c, n):
    if EMULASERIALE:
        return
    msg = f"{c}{n}\n"
    ser.write(msg.encode('utf-8'))
    # se master è python,  aspettiamo un attimo per dar modo all'arduino di rispondere se vuole
    if (MASTER==1):
        time.sleep(0.05)

# Funzione che viene chiamata quando Arduino manda un comando
def cmdIn(c, n):
    global isThereSomeone
    print(f"Ricevuto da Arduino: {c}{n}")
    # cambiare qui per fare cose diverse in base al comando ricevuto

    if (c=='V'):
        if(n==0):
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

def capturePhoto():
    if not cap.isOpened():
        print("Errore, non trovo la webcam")
    else:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(OUTPUT_FOLDER +"/utente.jpg", frame)
            print("Fatto")
        else:
            print("Errore leggendo il frame")

    cap.release()

def playAudio(file_path=None):
    # Initialize mixer
    pygame.mixer.init()

    # Load and play MP3
    pygame.mixer.music.load(file_path)

    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    print("Fatto")

def playAudioLoadImage(file_path=None):
    # Initialize mixer
    pygame.mixer.init()

    # Load and play MP3
    pygame.mixer.music.load(file_path)

    pygame.mixer.music.play()
    mostrata = False

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

        if (check_semaphore("leogenera")):
            if (not mostrata):
                mostrata=True
                print("trovata immagine CORNICE")
                # Inizializzazione di Pygame
                pygame.init()

                # Carica l'immagine
                try:
                    immagine = pygame.image.load("santino.jpg")
                except pygame.error as e:
                    print(f"Errore nel caricamento dell'immagine: {e}")
                    pygame.quit()


                # Ottieni dimensioni dello schermo
                info_schermo = pygame.display.Info()
                altezza_schermo = info_schermo.current_h

                # Ottieni dimensioni dell'immagine
                larghezza_orig, altezza_orig = immagine.get_size()

                # Calcola scala proporzionale per adattare l'altezza dell'immagine all'altezza dello schermo
                scala = altezza_schermo / altezza_orig
                nuova_larghezza = int(larghezza_orig * scala)
                nuova_altezza = altezza_schermo

                # Ridimensiona l'immagine
                immagine_scalata = pygame.transform.smoothscale(immagine, (nuova_larghezza, nuova_altezza))

                # Crea una finestra con le nuove dimensioni
                schermo = pygame.display.set_mode((1, 1))
                time.sleep(0.1)
                schermo = pygame.display.set_mode((nuova_larghezza, nuova_altezza))
                time.sleep(0.1)
                pygame.display.set_caption("Visualizzatore Santino")

                # Mostra l'immagine
                schermo.blit(immagine_scalata, (0, 0))
                pygame.display.flip()
                time.sleep(0.1)

    print("Fatto")

def record_audio(file_num):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    SILENCE_THRESHOLD = 200  # da tarare in base al microfono
    MAX_SILENCE_SECONDS = 4
    MAX_SILENCE_CHUNKS = int(RATE / CHUNK * MAX_SILENCE_SECONDS)

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Registro.... (si fermerà dopo {MAX_SILENCE_SECONDS} secondi di silenzio)")

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Evita overflow: converti a float32
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        rms = np.sqrt(np.mean(audio_data ** 2))

        # Debug opzionale
        # print(f"RMS: {rms}")

        if rms < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > MAX_SILENCE_CHUNKS:
            print("Silenzio rilevato per 4 secondi. Registrazione terminata.")
            break

    print("Fatto.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salva su file
    fname=OUTPUT_FOLDER+"/"+str(file_num)+".wav"
    wf = wave.open(fname, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Saved recording as {fname}")


def crea_santino():
    # Crea un'immagine vuota 1000x2000 px, bianca
    base = Image.new("RGB", (1132, 2000), "white")
    # Carica 'generata.jpg' e ridimensionala a 800x1600 px
    generata = Image.open(OUTPUT_FOLDER+"/generata.jpg").resize((963, 1442))
    # Incolla l'immagine ridimensionata alle coordinate (100, 100)
    base.paste(generata, (91, 91))
    # Carica 'cornice.png' (che può avere trasparenza)
    cornice = Image.open("frames/Cornice"+str(numsantino)+".png").convert("RGBA")
    # Converte la base in RGBA per supportare l'alpha channel temporaneamente
    base = base.convert("RGBA")
    # Sovrapponi la cornice alla base mantenendo la trasparenza
    base.alpha_composite(cornice, dest=(0, 0))
    # Converti di nuovo in RGB per salvare in formato JPEG (che non supporta trasparenza)
    base = base.convert("RGB")
    # Salva l'immagine risultante
    base.save(OUTPUT_FOLDER+"/santino.jpg", "JPEG")




# inizio programma
clear_semaphores()


if not EMULASERIALE:
    # Avviamo la lettura dalla seriale
    threading.Thread(target=serial_reader, daemon=True).start()
else:
    # sempre qualcuno
    isThereSomeone=True


while fotoFatta==False:
    cmdOut('P',0)
    print(isThereSomeone)
    TEST=""
    TEST="-test" # "" per non test
    if (isThereSomeone):
        playAudio("audio-domande/intro"+TEST+".wav")
        capturePhoto()
        fotoFatta = True
        playAudio("audio-domande/domanda1"+TEST+".wav")
        record_audio("1")
        esegui("whisper.py", OUTPUT_FOLDER, "1")
        playAudio("audio-domande/domanda2"+TEST+".wav")
        record_audio("2")
        esegui("whisper.py", OUTPUT_FOLDER, "2")
        # 3 e 4
        playAudio("audio-domande/domanda3"+TEST+".wav")
        record_audio("3")
        esegui("whisper.py", OUTPUT_FOLDER, "3")
        playAudio("audio-domande/domanda4"+TEST+".wav")
        record_audio("4")
        esegui("whisper.py", OUTPUT_FOLDER, "4")
        # audio riempimento 1

        wait_semaphore("whisper1")
        wait_semaphore("whisper2")
        wait_semaphore("whisper3")
        wait_semaphore("whisper4")


        esegui("chat.py", arg1=OUTPUT_FOLDER)
        # aspetta ritorno chat
        wait_semaphore("chat")

        # leggi ritorno chat
        result_fname = OUTPUT_FOLDER + "/" + "numsantino" + ".txt"
        with open(result_fname) as f:
            numsantino = f.read()

        print("esegue leogenera")
        esegui("leogenera.py", arg1=OUTPUT_FOLDER)

        # audio responso
        playAudioLoadImage("audio-risposte/risultato"+numsantino+".wav")

        # aspetta ritorno leogenera
        wait_semaphore("leogenera")

        #incornicia
        crea_santino()
        # OUTPUT_FOLDER +"/utente.jpg"

        #mostra
        # Loop per mantenere aperta la finestra finché non viene chiusa
        in_esecuzione = True
        while in_esecuzione:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    in_esecuzione = False

        pygame.quit()
