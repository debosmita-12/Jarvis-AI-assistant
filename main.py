# L.Y.R.A -> Light-Year Responsive Assistant
# A voice-activated virtual assistant with GPT-4o integration.

import speech_recognition as sr
import webbrowser
import pyttsx3
import openai
import os
from dotenv import load_dotenv
import musicLibrary 

load_dotenv()
openai.api_key = os.getenv("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")

# Text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print(f"Lyra: {text}")
    engine.say(text)
    engine.runAndWait()

# Command handler
def processCommand(c):
    print("Processing command:", c)
    speak("You said: " + c)
    command = c.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif command.startswith("play"):
        parts = command.split(" ", 1)
        if len(parts) > 1:
            song = parts[1].strip()
            if song in musicLibrary.music:
                link = musicLibrary.music[song]
                speak(f"Playing {song}")
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find the song '{song}' in your music library.")
        else:
            speak("Please say the name of the song you want to play.")
    else:
        # GPT-4o fallback
        speak("Let me think...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Lyra, a helpful AI assistant like Alexa or Siri."},
                    {"role": "user", "content": c}
                ]
            )
            gpt_reply = response['choices'][0]['message']['content']
            print("GPT says:", gpt_reply)
            speak(gpt_reply)
        except Exception as e:
            print("GPT error:", e)
            speak("Sorry, I couldn't fetch a reply from my brain.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Lyra, your personal AI assistant.")
    while True:
        r = sr.Recognizer()
        print("\n🎤 Waiting for wake word...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            print("Heard:", word)

            if word.lower() == "lyra":
                speak("Yes?")
                with sr.Microphone() as source:
                    print("🎧 Lyra active... Listening for command...")
                    audio = r.listen(source, timeout=5)
                    command = r.recognize_google(audio)
                    print("Command:", command)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("⏱Timeout: No speech detected.")
        except sr.UnknownValueError:
            print(" Could not understand audio.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
