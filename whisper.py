import sys
from openai import OpenAI
from chiave import KEY
from semaphores import wait_semaphore, set_semaphore, clear_semaphores


# Controlla che sia stato passato un argomento per il nome del file
if len(sys.argv) < 3:
    print("Uso: python script.py nome_file_output.txt")
    sys.exit(1)

print(sys.argv)

OUTPUT_FOLDER= sys.argv[1]

file_num = sys.argv[2]

client = OpenAI(api_key=KEY)

audio_fname =  OUTPUT_FOLDER + "/" + str(file_num) + ".wav"

# Apri il file audio
audio_file = open(audio_fname, "rb")

# Trascrizione
transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe",
    file=audio_file,
    language="it",
    prompt="if there is no sound return an empty string"
)

transcription_fname =  OUTPUT_FOLDER + "/" + str(file_num) + ".txt"

# Salva la trascrizione in un file .txt
with open(transcription_fname, "w", encoding="utf-8") as f:
    f.write(transcription.text)

print("Salvato in" + transcription_fname)

set_semaphore("whisper" + str(file_num))
