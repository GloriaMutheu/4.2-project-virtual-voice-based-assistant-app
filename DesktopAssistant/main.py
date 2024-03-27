
import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import random

from system import *
from API import *
from browse import *
import warnings
warnings.filterwarnings("ignore")
win_ops = WindowOpt()
sys_ops = SystemTasks()
tab_ops = TabOpt()


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)


from keras_preprocessing.sequence import pad_sequences
from keras.models import load_model
from pickle import load
import numpy as np


# load trained from DATA directory model
model = load_model('Data\\chat_model')

# load tokenizer object
with open('Data\\tokenizer.pickle', 'rb') as handle:
    tokenizer = load(handle)

# load label encoder object
with open('Data\\label_encoder.pickle', 'rb') as enc:
    lbl_encoder = load(enc)

def chat(text):
    max_len = 20
    while True:
        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]),
                                                                          truncating='post', maxlen=max_len), verbose=False)
        intent = lbl_encoder.inverse_transform([np.argmax(result)])[0]
        return intent


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! ")

    elif hour>=12 and hour<17:
        speak("Good Afternoon! ")

    elif hour>=17 and hour<19 :
        speak("Good Evening! ")

    else:
        speak("Good Night! ")

    speak("I am your  Vertual  Assistant master. Please tell me how may I help you")

def takeCommand():
   
    rr = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        rr.pause_threshold = 1
        audio = rr.listen(source)

    try:
        print("Recognizing...")
        query = rr.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
       
        print("Say that again please...")
        #speak("Connection error")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jackmutiso37@gmail.com', 'tzuhdwrgmuqtgydw')
    server.sendmail('jackmutiso37@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
        intent = chat(query)
        # Logic for executing tasks based on query
        if 'Master' in query:
            speak('Yes, tell me...')
          

        elif "hello" in query or "hello master" in query:
            hello1 = "Hello ! How May i Help you.."
            print(hello1)
            speak(hello1)

        elif "who are you" in query or "about you" in query or "your details" in query:
            who_are_you = "I am master an A I based computer program but i can help you lot like a your assistant ! try me to give simple command !"
            print(who_are_you)
            speak(who_are_you)

        elif 'who make you' in query or 'who made you' in query or 'who created you' in query or 'who develop you' in query:
            speak(" For your information GloriaDev Created me !    I can show you his Linked In profile if you want to see.    Yes or no .....")
            ans_from_user_who_made_you = takeCommand()
            if 'yes' in ans_from_user_who_made_you or 'ok' in ans_from_user_who_made_you or 'yeah' in ans_from_user_who_made_you:
                webbrowser.open("https://github.com/jarrdim")
                speak('opening his profile...... please wait')

            elif 'no' in ans_from_user_who_made_you or 'no thanks' in ans_from_user_who_made_you or 'not' in ans_from_user_who_made_you:
                speak("All right ! OK...")
            else :
                speak("I can't understand. Please say that again !")
        elif  "address" in query or "ip" in query or "my ip address" in query:
            ip = get_ip()
            print(ip)
            speak(ip)
          
        elif "todays news" in query or "news" in query:
            news = get_news()
            print(news)
            speak(news)
       
        elif "joke" in query or "funny" in query:
            joke = get_joke()
            print(joke)
            speak(joke)
            done = True
        
        elif intent == "open_app":
            completed = open_app(query)
            if completed:
                done = True

        elif "info" in query or "specs" in query or "information" in query or "system information" in query:
            try:
                info = systemInfo()
                print(info)
                speak(info)
                done = True
            except Exception  as e:
                speak(e)

        elif intent == "wikipedia" and ("tell" in query or "about" in query):
            description = tell_me_about(query)
            if description:
                print(description)
                speak(description)
            else:
                googleSearch(query)
            done = True
        elif intent == "screenshot" and "screenshot" in query:
            win_ops.Screen_Shot()
            done = True
        elif intent == "internet_speedtest" and "internet" in query or "internet speed" in query or "network speed" in query:
            speak("Getting your internet speed, this may take some time")
            speed = get_speedtest()
            if speed:
                print(speed)
                speak(speed)
                done = True
        elif ("youtube" in query and "search" in query) or "play" in query or ("how to" in query and "youtube" in query):
            youtube(query)
        elif ("google" in query and "search" in query) or ("google" in query and "how to" in query) or "google" in query:
            googleSearch(query)
        elif intent == "note" and "note" in query:
            speak("what would you like to take down?")
            note = takeCommand()
            take_note(note)
            done = True
        elif intent == "select_text" and "select" in query:
            sys_ops.select()
            done = True
        elif intent == "copy_text" and "copy" in query:
            sys_ops.copy()
            done = True
        elif intent == "paste_text" and "paste" in query:
            sys_ops.paste()
            done = True
        elif intent == "delete_text" and "delete" in query:
            sys_ops.delete()
            done = True
        elif intent == "new_file" and "new" in query:
            sys_ops.new_file()
            done = True
        elif intent == "switch_tab" and "switch" in query and "tab" in query:
            tab_ops.switchTab()
            done = True
        elif intent == "close_tab" and "close" in query and "tab" in query:
            tab_ops.closeTab()
            done = True
        elif intent == "new_tab" and "new" in query and "tab" in query:
            tab_ops.newTab()
            done = True
        elif intent == "close_window" and "close" in query:
            win_ops.closeWindow()
            done = True
        elif intent == "switch_window" and "switch" in query:
            win_ops.switchWindow()
            done = True
        elif intent == "minimize_window" and "minimize" in query:
            win_ops.minimizeWindow()
            done = True
        elif intent == "maximize_window" and "maximize" in query:
            win_ops.maximizeWindow()
            done = True
        
        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            speak("opening youtube")

        elif 'open github' in query:
            webbrowser.open("https://www.github.com")
            speak("opening github")

        elif 'open facebook' in query:
            webbrowser.open("https://www.facebook.com")
            speak("opening facebook")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")
            speak("opening instagram")   

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("opening google")

        elif 'open stackoverflow' in query or "open stack overflow" in query:
            webbrowser.open("stackoverflow.com")
            speak("opening stackoverflow")

        elif 'open yahoo' in query:
            webbrowser.open("https://www.yahoo.com")
            speak("opening yahoo")
            
        elif 'open gmail' in query:
            webbrowser.open("https://mail.google.com")
            speak("opening google mail") 
            
   
             
        elif 'open amazon' in query or 'shop online' in query:
            webbrowser.open("https://www.amazon.com")
            speak("opening amazon")

        elif 'open kabarak' in query:
            webbrowser.open("https://kabarak.ac.ke")
            speak("opening kabarak")

        elif 'music' in query:
            speak("ok i am playing music")
            music_dir = 'D:\Music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'video from pc' in query or "video" in query:
            speak("ok i am playing videos")
            video_dir = 'D:\Video music'
            Videos = os.listdir(video_dir)
            print(Videos)
            os.startfile(os.path.join(video_dir,Videos[0]))

        elif 'good bye' in query:
            speak("good bye")
            exit()

        elif "shutdown" in query:
            speak("shutting down")
            os.system('shutdown -s')

        elif "your name" in query or "sweat name" in query:
            naa_mme = "Thanks for Asking my self ! Master Behide"
            print(naa_mme)
            speak(naa_mme)

        elif "you feeling" in query:
            print("feeling Very happy to help you")
            speak("feeling Very happy to help you")

        elif query == 'none':
            continue

        elif 'exit' in query or 'stop' in query or 'quit' in query :
            exx_exit = 'See you soon. Bye'
            speak(exx_exit)
            exit() 

        elif 'the time' in query or "current time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"the time is {strTime}")

        elif 'open code' in query:
            codePath = "D:\\vs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            speak("opening visual studio code")

        elif 'email to master' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "mutheugloria5@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry.... I am not able to send this email")

        elif 'how are you' in query:
            setMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!']
            ans_qus = random.choice(setMsgs)
            speak(ans_qus)
            speak(" How are you'")
            ans_from_user_how_are_you = takeCommand()
            if 'fine' in ans_from_user_how_are_you or 'happy' in ans_from_user_how_are_you or 'okey' in ans_from_user_how_are_you:
                speak('Great')  
            elif 'not' in ans_from_user_how_are_you or 'sad' in ans_from_user_how_are_you or 'upset' in ans_from_user_how_are_you:
                speak('Tell me how can i make you happy')
            else :
                speak("I can't understand. Please say that again !")

        else:
            tempp = query.replace(' ','+')
            prasun_url="https://www.google.com/search?q="    
            res_prasun = 'sorry! i cant understand but i search from internet to give your answer !'
            print(res_prasun)
            speak(res_prasun)
            webbrowser.open(prasun_url+tempp)