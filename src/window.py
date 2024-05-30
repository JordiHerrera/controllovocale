import eel
import main as mn

eel.init('web')
eel._exposed_functions = {}


def u():
    # eel.expose(scripts, record_and_upload, wait_for_new_file, download_file, delete_file)
    mn.record_and_upload("audio")
    bucket_name = 'audio-script-sm'
    destination = 'to_script.json'
    blob = mn.wait_for_new_file(bucket_name)
    mn.download_file(bucket_name, blob.name, destination)
    mn.delete_file(bucket_name, blob.name)
    # mn.print_message("Scripts!")
    mn.scripts()
    u()

if __name__ =='__main__':
    eel.expose(u)
    eel.start('index.html', size=(1000, 900))
