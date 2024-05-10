import pyaudio
import wave
import os

from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

def gravacio(temps, nom):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    print("Gravant audio...")

    frames = []

    for i in range(0, int(44100 / 1024 * temps)):
        data = stream.read(1024)
        frames.append(data)

    print("Gravacio acabada.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio as a WAV file
    wf = wave.open(nom+'.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    storage_client = storage.Client()
    bucket = storage_client.bucket('input-audio-uab')
    blob = bucket.blob(nom+'.wav')
    blob.upload_from_filename(nom + '.wav')
    os.remove(nom+'.wav')

    print('Audio pujat al Bucket input-audio-uab')

#gravacio(3, 'test3') # Arguments: Temps en segons, nom del fitxer. Sortida wav