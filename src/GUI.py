from logic import *

def close_window():
    root.destroy()

def perform_operations(root):
    # Perform operations that affect the UI
    record_and_upload("audio", message_label, root)
    bucket_name = 'audio-script-sm'
    destination = 'to_script.json'
    blob = wait_for_new_file(bucket_name, root)
    download_file(bucket_name, blob.name, destination, root)
    delete_file(bucket_name, blob.name, root)
    scripts()
    message_label.config(text="Hecho :)")

root = tk.Tk()
root.title("Voice Controlled GUI")

# Window size
root.geometry("800x600")

# Styles
title_font = tkfont.Font(family="Consolas", size=36, weight="bold")
button_font = tkfont.Font(family="Consolas", size=24, weight="bold")
label_font = tkfont.Font(family="Consolas", size=12)

# Title
title_label = tk.Label(root, text="Controlador de Voz", font=title_font)
title_label.pack(pady=20)

# Close button
close_button = tk.Button(root, text="Exit", command=close_window, font=button_font, bg="red", fg="white")
close_button.pack(side=tk.BOTTOM, padx=20, pady=20, anchor=tk.SE)

# Messages
message_label = tk.Label(root, text="", font=label_font)
message_label.pack()

perform_operations(root)

root.mainloop()