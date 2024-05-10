import subprocess
import pyaudio
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'
cliente_storage = storage.Client()

def descarrega_executa(nom, bucket):
    bucket = cliente_storage.bucket(bucket)

    # Definir el nombre del archivo que se va a descargar
    archivo_nombre = nom

    # Descargar el archivo
    blob = bucket.blob(archivo_nombre)
    blob.download_to_filename(archivo_nombre)
    subprocess.run(['python', nom])

#descarrega_executa('helloworld.py', 'audio-script-sm')
