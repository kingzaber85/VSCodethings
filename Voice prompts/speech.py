# https://github.com/acgrissom/courses/blob/master/2020-hci/hw1_voiceui.md
# https://github.com/acgrissom/courses/blob/master/2020-hci/code/recognize_speech.py
# sudo apt install portaudio19-dev libespeak-dev
# pip3 install pyaudio pyttsx3 speechrecognition
# alternatively: pip3 install pipwin && pipwin install pyaudio

import speech_recognition as sr
import pyttsx3
import sys
import time

tts = pyttsx3.init()


def speak(tts, text):
    tts.say(text)
    tts.runAndWait()

def main():
    # get audio from the microphone                                                                       
    listener = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source) # used to detect silence to stop listening after a phrase is spoken
        while True:
            print("Listening.")
            speak(tts, "listening") # how do we prevent this from being spoken every time an exception is thrown?
            time.sleep(1) # used to prevent hearing any spoken text; what else could we do?
            user_input = None
            sys.stdout.write(">")
            #record audio
            listener.pause_threshold = 0.5 # how long, in seconds, to observe silence before processing what was heard
            audio = listener.listen(source, timeout=5) #, timeout = N throws an OSError after N seconds if nothing is heard.  can also call listen_in_background(source, callback) and specify a function callback that accepts the recognizer and the audio when data is heard via a thread
            try:
                #convert audio to text
                #user_input = listener.recognize_sphinx(audio) #requires PocketSphinx installation
                user_input = listener.recognize_google(audio, show_all = False) # set show_all to True to get a dictionary of all possible translations

                print(user_input)
                speak(tts, user_input)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
            except OSError:
                print("No speech detected")
                
            sys.stdout.write("\n")




if __name__ == "__main__":
    main()