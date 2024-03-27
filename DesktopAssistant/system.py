import math
import psutil
import time
from random import randint
import subprocess
import AppOpener
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import wmi
import os
import subprocess
import pyttsx3
import speech_recognition as sr


class SystemTasks:
    def __init__(self):
        self.keyboard = Controller()

    def write(self, text):
        self.keyboard.type(text)

    def select(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(Key.ctrl)

    def hitEnter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def delete(self):
        self.select()
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)

    def copy(self):
        self.select()
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(Key.ctrl)

    def paste(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.ctrl)

    def new_file(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('n')
        self.keyboard.release('n')
        self.keyboard.release(Key.ctrl)

    def save(self, name):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('s')
        self.keyboard.release('s')
        self.keyboard.release(Key.ctrl)
        time.sleep(0.2)
        self.write(name)
        self.hitEnter()


class TabOpt:
    def __init__(self):
        self.keyboard = Controller()

    def switchTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.ctrl)

    def closeTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('w')
        self.keyboard.release('w')
        self.keyboard.release(Key.ctrl)

    def newTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('t')
        self.keyboard.release('t')
        self.keyboard.release(Key.ctrl)


class WindowOpt:
    def __init__(self):
        self.keyboard = Controller()

    def closeWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.f4)
        self.keyboard.release(Key.f4)
        self.keyboard.release(Key.alt_l)

    def minimizeWindow(self):
        for i in range(2):
            self.keyboard.press(Key.cmd)
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.cmd)
            time.sleep(0.05)

    def maximizeWindow(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.cmd)

    def switchWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.alt_l)

    def Screen_Shot(self):
        im = ImageGrab.grab()
        speak("yes, Your screenshot is save in screenshots folder")
        im.save(f'Screenshots/s_{randint(1, 100)}.jpg')


def systemInfo():
    
    c = wmi.WMI()
    my_system_1 = c.Win32_LogicalDisk()[0]
    my_system_2 = c.Win32_ComputerSystem()[0]
    info = f"Total Disk Space: {round(int(my_system_1.Size)/(1024**3),2)} GB\n" \
           f"Free Disk Space: {round(int(my_system_1.Freespace)/(1024**3),2)} GB\n" \
           f"Manufacturer: {my_system_2.Manufacturer}\n" \
           f"Model: {my_system_2. Model}\n" \
           f"Owner: {my_system_2.PrimaryOwnerName}\n" \
           f"Number of Processors: {psutil.cpu_count()}\n" \
           f"System Type: {my_system_2.SystemType}"
    return info


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    stats = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory} is being used and " \
                f"battery level is at {battery_percent}%"
    return stats


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def open_app(query):
    username = os.getlogin() 

    app_paths = {
        'zoom': fr'C:\Users\{username}\AppData\Roaming\Zoom\bin\Zoom.exe',  
        'notepad': r'C:\Windows\System32\notepad.exe',
        'access': fr'C:\Program Files\Microsoft Office\Office16\MSACCESS.EXE',  
        'excel': fr'C:\Program Files\Microsoft Office\Office16\EXCEL.EXE',  
        'word': fr'C:\Program Files\Microsoft Office\Office16\WINWORD.EXE', 
        'powerpoint': fr'C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE',  
        'outlook': fr'C:\Program Files\Microsoft Office\Office16\OUTLOOK.EXE',  
        'onenote': fr'C:\Program Files\Microsoft Office\Office16\ONENOTE.EXE',  
        'publisher': fr'C:\Program Files\Microsoft Office\Office16\MSPUB.EXE', 
        'infopathdesigner': fr'C:\Program Files\Microsoft Office\Office16\INFOPATHDESIGNER.EXE',  
        'infopathfiller': fr'C:\Program Files\Microsoft Office\Office16\INFOPATH.EXE',  
        'project': fr'C:\Program Files\Microsoft Office\Office16\WINPROJ.EXE', 
        'visio': fr'C:\Program Files\Microsoft Office\Office16\VISIO.EXE',  
        'calculator': 'C:\\Windows\\System32\\calc.exe',  
        
      
    }

    # for app, path in app_paths.items():
    #     if app in query.lower():
    #         try:
    #             speak("Openning "+app)
    #             subprocess.Popen(path)
    #             return True
    #         except Exception as e:
    #             return f"Error opening {app}: {e}"
            

    # return False  
    for app, path in app_paths.items():
        if app in query.lower():
            try:
                result = record(app)
                print(result)
                if( "yes" in result) or ("continue" in result):
                    subprocess.Popen(path)
                    finishMesage(app + " Is open Proceed")
                    return True
                else:
                    finishMesage("Terminated")
                
            except Exception as e:
                return f"Error opening {app}: {e}"
            
    return False

def finishMesage(text):
    try:
        print(text)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return
    
def record(app):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        
        finishMesage("Are You Sure You want to open "+app+" ?")
        #time.sleep(2)
        audio = recognizer.listen(mic)
        time.sleep(3)
        try:
            text = recognizer.recognize_google(audio, language='us-in').lower()
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error during speech recognition: {e}")
   
    return None



def take_note(note):
    open_app("open notepad")
    time.sleep(0.2)
    sys_task = SystemTasks()
    sys_task.write(note)
    sys_task.save(f'note_{randint(1, 100)}')