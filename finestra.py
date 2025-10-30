import webbrowser
import os
from urllib.request import pathname2url

def apri_immagine_nel_browser(percorso_immagine):
    if not os.path.isfile(percorso_immagine):
        print("File non trovato:", percorso_immagine)
        return

    # Ottieni il percorso assoluto e converti in URL
    percorso_assoluto = os.path.abspath(percorso_immagine)
    url = 'file://' + pathname2url(percorso_assoluto)

    # Apre l'immagine nel browser
    webbrowser.open(url)

# Esempio di utilizzo
apri_immagine_nel_browser("santino.jpg")
