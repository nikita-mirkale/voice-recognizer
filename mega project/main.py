import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
from musicLibrary import music  # Importing the music library from the separate file

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = "54ac4833004a460c93a2b0c6a3b67c7b"  # Replace with your NewsAPI key

# Function to speak text
def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('temp.mp3')

# Function to fetch news
def get_news():
    try:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")

        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get("articles", [])

            if articles:
                # Read out the headlines
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, there are no news articles available at the moment.")
        else:
            speak("Sorry, I couldn't fetch the news at this time.")
    except Exception as e:
        speak(f"An error occurred while fetching the news: {e}")

# Function to process commands
def processCommand(c):
    if c.lower().startswith("play"):
        song_name = c.lower().replace("play", "").strip()

        # Try to find a partial match in the music library
        found_song = None
        for song, link in music.items():
            if song_name in song:
                found_song = link
                break

        if found_song:
            webbrowser.open(found_song)
            print(f"Playing {song_name}...")
        else:
            print(f"Sorry, I couldn't find {song_name} in your music library.")

    elif "news" in c.lower():
        get_news()  # Call the function to get news



    elif "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")

    elif "stop" in c.lower() or "exit" in c.lower():
        speak("Goodbye!")
        exit()  # Exit the program

# Function to continuously listen for commands
def continuous_listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening for commands...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
                command = recognizer.recognize_google(audio).lower()
                print(f"Command received: {command}")
                processCommand(command)
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Please repeat.")
            except sr.RequestError as e:
                speak(f"Sorry, there was an issue with the Google service: {e}")

# Main function
if __name__ == "__main__":
    speak("Initializing Siri...")

    while True:
        print("Waiting for wake word 'Siri'...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            recognizer.energy_threshold = 150
            print("Listening for wake word...")

            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                word = recognizer.recognize_google(audio).lower()

                if "hi siri" in word:
                    speak("Yes Baby")
                    continuous_listen()  # Start continuous listening for commands after wake word
            except sr.WaitTimeoutError:
                print("No speech detected. Trying again.")
            except sr.UnknownValueError:
                print("Could not understand the wake word.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
