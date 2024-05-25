import pyaudio
import wave
import os
import time
import mouse
import pyautogui
import json
#import wmi
import pygetwindow as gw
import difflib
#import tkinter as tk
#from tkinter import font as tkfont

from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

def record_and_upload(name):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    #label.config(text="Pulsa el botón central del ratón para empezar a grabar...")
    print("Pulsa el botón central del ratón para empezar a grabar...")

    frames = []

    while not mouse.is_pressed(button='middle'):
        #root.update_idletasks()  # Update GUI events
        #root.update()  # Process GUI events
        pass

    #label.config(text="Grabando, soltar el botón central del ratón para finalizar grabación.")
    print("Grabando, soltar el botón central del ratón para finalizar grabación.")
    while mouse.is_pressed(button='middle'):
        data = stream.read(1024)
        frames.append(data)
        #root.update_idletasks()  # Update GUI events
        #root.update()  # Process GUI events

    #label.config(text="Grabación finalizada. Processando instrucciones...")
    print("Grabación finalizada. Processando instrucciones...")
    #root.update_idletasks()  # Update GUI events
    #root.update()  # Process GUI events

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
    #root.update_idletasks()  # Update GUI events
    #root.update()  # Process GUI events


def wait_for_new_file(bucket_name, timeout=300):
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
        #root.update_idletasks()  # Update GUI events
        #root.update()  # Process GUI events

def download_file(bucket_name, file_name, destination):
    """Download a file from the specified bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(destination)

def delete_file(bucket_name, file_name):
    """Delete a file from the specified bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.delete()
"""
SCRIPTS
"""
def manage_windows(window_title, method):
    windows = gw.getAllTitles()
    windows = [title for title in windows if title]
    
    closest_match = difflib.get_close_matches(window_title, windows, n=1, cutoff=0.3)
    if closest_match==[]:
        return False
    closest_match = closest_match[0]
    
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window = window[0]
        if method == 'b':
            if window.isMinimized:
                window.restore()
            window.activate()
            return True
        elif method == 'c':
            window.close()
            return True
    else:
        print("Window not found.")
        return False
    
def scripts(distance=75):
    with open("to_script.json", 'r') as file:
        data = json.load(file)
    for action in data:
        i=0
        while (i<len(action)):
            if action[i] == 'copiar':
                pyautogui.hotkey('ctrl', 'c')
            elif action[i] == 'pegar':
                pyautogui.hotkey('ctrl', 'v')
            elif action[i] == 'cortar':
                pyautogui.hotkey('ctrl', 'x')
            elif action[i] == 'deshacer':
                pyautogui.hotkey('ctrl', 'z')
            elif action[i] == 'rehacer':
                pyautogui.hotkey('ctrl', 'y')
            elif action[i] == 'apagar':
                #label_scripts.config(text="¿Estás seguro de que quieres apagar el equipo? Responde con afirmativo o negativo")
                print("¿Estás seguro de que quieres apagar el equipo? Responde con afirmativo o negativo")
                record_and_upload("audio")
                blob = wait_for_new_file('audio-script-sm')
                download_file('audio-script-sm', blob.name, "to_script.json")
                delete_file('audio-script-sm', blob.name)
                #root.update_idletasks()
                #root.update()
                with open("to_script.json", 'r') as file:
                    data2 = json.load(file)
                for confirmation in data2:
                    if confirmation == ["afirmativo"]:
                        os.system('shutdown /s /t 1')
                    elif confirmation == ["negativo"]:
                        break
            elif action[i] == 'reiniciar':
                #label_scripts.config(text="¿Estás seguro de que quieres reiniciar el equipo? Responde con afirmativo o negativo")
                print("¿Estás seguro de que quieres reiniciar el equipo? Responde con afirmativo o negativo")
                record_and_upload("audio")
                blob = wait_for_new_file('audio-script-sm')
                download_file('audio-script-sm', blob.name, "to_script.json")
                delete_file('audio-script-sm', blob.name)
                #root.update_idletasks()
                #root.update()
                with open("to_script.json", 'r') as file:
                    data2 = json.load(file)
                for confirmation in data2:
                    if confirmation == ["afirmativo"]:
                        os.system('shutdown /r /t 1')
                    elif confirmation == ["negativo"]:
                        break
            elif action[i] == 'cambiar':
                i+=1
                manage_windows(action[i],'b')
            elif action[i] == 'cerrar':
                i+=1
                manage_windows(action[i],'c')
            elif action[i] == 'abrir':
                #to implement
                print("Not done") 
            elif action[i] == 'escribir':
                pyautogui.write(action[i+1])
                pyautogui.press('space')
                i+=1
            elif action[i] == 'mover':
                i+=2
                if action[i] == 'arriba':
                    if(len(action)>3):
                        i+=1
                        distance=int(action[i])
                        pyautogui.moveRel(xOffset=0, yOffset=-distance, duration=0.15)
                        distance=75
                    else:
                        pyautogui.moveRel(xOffset=0, yOffset=-distance, duration=0.15)
                elif action[i] == 'abajo':
                    if(len(action)>3):
                        i+=1
                        distance=int(action[i])
                        pyautogui.moveRel(xOffset=0, yOffset=distance, duration=0.15)
                        distance=75
                    else:
                        pyautogui.moveRel(xOffset=0, yOffset=distance, duration=0.15)
                elif action[i] == 'derecha':
                    if(len(action)>3):
                        i+=1
                        distance=int(action[i])
                        pyautogui.moveRel(xOffset=distance, yOffset=0, duration=0.15)
                        distance=75
                    else:
                        pyautogui.moveRel(xOffset=distance, yOffset=0, duration=0.15)
                elif action[i] == 'izquierda':
                    if(len(action)>3):
                        i+=1
                        distance=int(action[i])
                        pyautogui.moveRel(xOffset=-distance, yOffset=0, duration=0.15)
                        distance=75
                    else:
                        pyautogui.moveRel(xOffset=-distance, yOffset=0, duration=0.15)
            elif action[i] == 'doble':
                i+=1
                pyautogui.doubleClick()
            elif action[i] == 'clic':
                i+=1
                if action[i] == 'derecho':
                    pyautogui.rightClick()
                if action[i] == 'izquierdo':
                    pyautogui.click()
                if action[i] == 'central':
                    pyautogui.middleClick()
            else:
                print('Error not a scripts') 
            i=i+1
            time.sleep(1)

def use():
    record_and_upload("audio")
    bucket_name = 'audio-script-sm'
    destination = 'to_script.json'
    blob = wait_for_new_file(bucket_name)
    download_file(bucket_name, blob.name, destination)
    delete_file(bucket_name, blob.name)
    print("Scripts!")
    scripts()



use()

