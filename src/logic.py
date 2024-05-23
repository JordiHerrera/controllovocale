import pyaudio
import wave
import os
import time
import mouse
import pyautogui
import json
import tkinter as tk
from tkinter import font as tkfont

from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

def record_and_upload(name, label, root):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    label.config(text="Pulsa el botón central del ratón para empezar a grabar...")

    frames = []

    while not mouse.is_pressed(button='middle'):
        root.update_idletasks()  # Update GUI events
        root.update()  # Process GUI events

    label.config(text="Grabando, soltar el botón central del ratón para finalizar grabación.")

    while mouse.is_pressed(button='middle'):
        data = stream.read(1024)
        frames.append(data)
        root.update_idletasks()  # Update GUI events
        root.update()  # Process GUI events

    label.config(text="Grabación finalizada. Processando instrucciones...")
    root.update_idletasks()  # Update GUI events
    root.update()  # Process GUI events

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio
    wf = wave.open(name + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Upload to Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket('input-audio-uab')
    blob = bucket.blob(name + '.wav')
    blob.upload_from_filename(name + '.wav')

    # Remove local file after upload
    os.remove(name + '.wav')
    root.update_idletasks()  # Update GUI events
    root.update()  # Process GUI events


def wait_for_new_file(bucket_name, root, timeout=300):
    """Wait for a new file to be uploaded to the specified bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    start_time = time.time()
    while True:
        blobs = list(bucket.list_blobs())
        if blobs:
            return blobs[0]
        if time.time() - start_time >= timeout:
            raise TimeoutError("Timeout waiting for new file")
        root.update_idletasks()  # Update GUI events
        root.update()  # Process GUI events

def download_file(bucket_name, file_name, destination, root):
    """Download a file from the specified bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(destination)

def delete_file(bucket_name, file_name, root):
    """Delete a file from the specified bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()

def scripts(distance=75):
    with open("to_script.json", 'r') as file:
        data = json.load(file)
    for action in data:
        if not isinstance(action, list):
            if action == 'copiar':
                pyautogui.hotkey('ctrl', 'c')
            elif action == 'cerrar':
                pyautogui.hotkey('alt', 'f4')
            elif action == 'pegar':
                pyautogui.hotkey('ctrl', 'v')
            elif action == 'cortar':
                pyautogui.hotkey('ctrl', 'x')
            elif action == 'deshacer':
                pyautogui.hotkey('ctrl', 'z')
            elif action == 'rehacer':
                pyautogui.hotkey('ctrl', 'y')
            elif action == 'clic':
                pyautogui.click()
            elif action == 'doble':
                pyautogui.doubleClick()
            else:
                print('Queseso')
        else:
            for i in range(1, len(action)):
                if action[0] == 'mover':
                    if action[1] == 'raton' or 'cursor':
                        if action[i] == 'arriba':
                            pyautogui.moveRel(xOffset=0, yOffset=-distance, duration=0.15)
                        elif action[i] == 'abajo':
                            pyautogui.moveRel(xOffset=0, yOffset=distance, duration=0.15)
                        elif action[i] == 'derecha':
                            pyautogui.moveRel(xOffset=distance, yOffset=0, duration=0.15)
                        elif action[i] == 'izquierda':
                            pyautogui.moveRel(xOffset=-distance, yOffset=0, duration=0.15)
                if action[0] == 'clic':
                    if action[i] == 'derecha':
                        pyautogui.rightClick()
                    if action[i] == 'izquierda':
                        pyautogui.click()
                    if action[i] == 'central':
                        pyautogui.middleClick()
                if action[0] == 'escribir':
                    pyautogui.write(action[i])
                    pyautogui.press('space')
        time.sleep(1)