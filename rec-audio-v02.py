import pyaudio
import wave
import time
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "registra.wav"
SILENCE_THRESHOLD = 500  # da tarare in base al microfono
MAX_SILENCE_SECONDS = 2
MAX_SILENCE_CHUNKS = int(RATE / CHUNK * MAX_SILENCE_SECONDS)


def record_audio():
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
        rms = np.sqrt(np.mean(audio_data**2))

        # Debug opzionale
        # print(f"RMS: {rms}")

        if rms < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > MAX_SILENCE_CHUNKS:
            print("Silenzio rilevato per 2 secondi. Registrazione terminata.")
            break

    print("Fatto.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Salva su file
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Saved recording as {OUTPUT_FILENAME}")
