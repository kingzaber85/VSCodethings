import pyttsx3

for i in range(3):
    engine = pyttsx3.init()
    engine.say(f"Test number {i+1}")
    engine.runAndWait()
    engine.stop()
