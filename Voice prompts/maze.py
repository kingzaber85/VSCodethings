import speech_recognition as sr
import pyttsx3

# ---------- setup ----------
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    print("SPEAK:", text)

    engine = pyttsx3.init()   
    engine.say(text)
    engine.runAndWait()
    engine.stop()          


def listen():
    with sr.Microphone() as source:
        speak("listening.")
    

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            speak("I did not hear anything. Wait a second and try again")
            return None

    try:
        command = recognizer.recognize_google(audio).lower()
        print("HEARD:", command)
        return command
    except sr.UnknownValueError:
        speak("I did not understand. Please wait a second then speak clearly and slowly.")
        return None
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return None



# ---------- maze ----------
rooms = {
    "entrance": {"north": "hallway"},
    "hallway": {"south": "entrance", "east": "treasure", "west": "monster"},
    "treasure": {"west": "hallway"},
    "monster": {"east": "hallway"},
}

current_room = "entrance"
monster_alive = True
treasure_taken = False


def describe_room():
    if current_room == "entrance":
        speak("You are at the entrance. You can go north.")

    elif current_room == "hallway":
        speak("You are in a hallway. Treasure is east. Monster is west.")

    elif current_room == "treasure":
        if not treasure_taken:
            speak("You found the treasure. Say take treasure.")
        else:
            speak("The room is empty. Go west.")

    elif current_room == "monster":
        if monster_alive:
            speak("A monster is here. Say fight.")
        else:
            speak("The monster is defeated. Go east.")


# ---------- main loop ----------
def game_loop():
    global current_room, monster_alive, treasure_taken

    speak("Welcome to the voice maze. Say help for commands.")

    while True:
        describe_room()

        command = listen()
        if command is None:
            continue

        if "quit" in command or "exit" in command:
            speak("Goodbye.")
            break

        if "help" in command:
            speak("Say go north south east or west. Say fight. Say take treasure. Say quit to exit.")
            continue


        if command.startswith("go "):
            direction = command.split(" ")[1]

            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                speak("You cannot go that way.")
            continue

 
        if "fight" in command and current_room == "monster" and monster_alive:
            speak("You defeated the monster.")
            monster_alive = False
            continue


        if "take" in command and current_room == "treasure" and not treasure_taken:
            if monster_alive:
                speak("Defeat the monster first. Leave this room by going west.")
            else:
                speak("You take the treasure. You win!")
                break
            continue

        speak("I did not understand that command.")


# ---------- start ----------
if __name__ == "__main__":
    game_loop()
