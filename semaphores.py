import os
import time
from pathlib import Path

SEMAPHORE_DIR = Path("semaphores")
SEMAPHORE_DIR.mkdir(exist_ok=True)

def set_semaphore(nome: str):
    """Crea un file di semaforo con nome specificato."""
    sem_path = SEMAPHORE_DIR / f"{nome}.txt"
    sem_path.touch(exist_ok=True)

def wait_semaphore(nome: str, check_interval: float = 0.5):
    """Attende finché il file di semaforo specificato non esiste."""
    sem_path = SEMAPHORE_DIR / f"{nome}.txt"
    while not sem_path.exists():
        time.sleep(check_interval)
    print("trovato semaforo "+nome)

def check_semaphore(nome: str):
    """ritorna True se il file di semaforo specificato non esiste."""
    sem_path = SEMAPHORE_DIR / f"{nome}.txt"
    return sem_path.exists()


def clear_semaphores():
    """Elimina tutti i file .txt nella cartella dei semafori."""
    for file in SEMAPHORE_DIR.glob("*.txt"):
        print(file.name)
        file.unlink()
