import os
import webbrowser
import subprocess
import speech_recognition as sr
import pyttsx3
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import json
import datetime
import pyautogui
import tkinter as tk
from tkinter import filedialog
import threading
import time
from PIL import Image, ImageTk
# .env dosyasından çevre değişkenlerini yükle
load_dotenv()
engine = pyttsx3.init()

def listen():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Sesinizi dinliyorum...")
            audio = recognizer.listen(source, phrase_time_limit=3)

        try:
            text = recognizer.recognize_google(audio, language="tr-TR")
            print("Ses algılandı: " + text)
            return text
        except sr.UnknownValueError:
            print("Ses anlaşılamadı.")
        except sr.RequestError as e:
            print("Ses tanıma servisi çalışmıyor; {0}".format(e))

        time.sleep(1)  # 1 saniye bekle ve tekrar dinle

if __name__ == "__main__":
    metin = listen()

def initialize_engine():
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def get_assistant_name():
    assistant_name = input("What should be my name? ")
    return assistant_name

def get_user_name():
    user_name = input("What's your name? ")
    return user_name

def save_names(assistant_name, user_name):
    data = {
        "assistant_name": assistant_name,
        "user_name": user_name
    }
    with open("names.json", "w") as file:
        json.dump(data, file)

def load_names():
    try:
        with open("names.json", "r") as file:
            data = json.load(file)
            return data.get("assistant_name"), data.get("user_name")
    except FileNotFoundError:
        return None, None

def load_applications():
    try:
        with open('applications.json', 'r') as file:
            applications = json.load(file)
            return applications
    except FileNotFoundError:
        return {}
   

# Spotify yetkilendirme ayarları
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def play_spotify_track(track_name):
    results = sp.search(q=track_name, limit=1, type="track")
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        devices = sp.devices()
        target_device_id = devices["devices"][0]["id"]
        sp.start_playback(uris=[track_uri], device_id=target_device_id)
        current_track_name = results["tracks"]["items"][0]["name"]
        speak("Now playing: " + current_track_name)
    else:
        speak("Sorry, I couldn't find that song.")

def resume_song():
    sp.start_playback()
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"The song continues. Currently playing: {track_name}")
    else:
        speak("The song continues.")

def pause_song():
    sp.pause_playback()
    speak("The song has been stopped.")

def play_next_song():
    sp.next_track()
    time.sleep(1)  # Şarkı değişikliğinin tamamlanması için bir süre bekleyin
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"Next song. Currently playing: {track_name}")
    else:
        speak("Next song.")

def play_previous_song():
    sp.previous_track()
    time.sleep(1)  # Şarkı değişikliğinin tamamlanması için bir süre bekleyin
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"Previous song. currently playing: {track_name}")
    else:
        speak("Previous song.")


def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here is what I found for " + query)

def open_website(website):
    url = f"https://{website}.com"
    webbrowser.open(url)
    speak("Opening " + website)


def set_alarm():
    speak("Sure, at what time would you like to set the alarm? Please provide the time in HH:MM format.")
    time_input = listen()
    try:
        alarm_time = datetime.datetime.strptime(time_input, "%H:%M").time()
        current_time = datetime.datetime.now().time()
        if alarm_time < current_time:
            speak("The specified time has already passed. Please enter a future time.")
            return
        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= alarm_time:
                speak("Wake up! It's time for the alarm.")
                break
    except ValueError:
        speak("Invalid time format. Please try again.")
        return


def get_weather(city):
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en&aqi=no"
    response = requests.get(url)
    weather_data = response.json()
    if "current" in weather_data:
        weather_description = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        return f"Weather for {city}: {weather_description}, temperature: {temperature} degrees"
    else:
        return None

def open_spotify():
    speak("Opening Spotify.")
    subprocess.Popen("C:\\Users\\omere\\AppData\\Roaming\\Spotify\\Spotify.exe")


def open_application(application_name):
    applications = load_applications()
    if application_name in applications:
        application_path = applications[application_name]
        speak(f"Opening {application_name}.")
        subprocess.Popen(application_path)
    else:
        if "open"  in application_name:
            application_name = application_name.replace("open", "").strip()
        speak(f"Sorry, I couldn't find the {application_name} application. Please provide the location of the application.")
        application_path = filedialog.askopenfilename(title="Select Application")
        if os.path.exists(application_path):
            speak(f"Opening {application_name}.")
            subprocess.Popen(application_path)
        else:
            speak(f"Sorry, I couldn't find the application at the specified location.")


def take_screenshot():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(file_path)
    speak("Screenshot saved.")

def add_application():
    root = tk.Tk()
    speak("Sure, which application would you like to add?")
    application_name = listen()
    speak("Please select the location of the application.")
    root.withdraw()
    application_path = filedialog.askopenfilename(title="Select Application")
    if application_path:
        applications = {}
        if os.path.isfile("applications.json"):
            with open("applications.json", "r") as file:
                applications = json.load(file)
        applications[application_name] = application_path
        with open("applications.json", "w") as file:
            json.dump(applications, file)
        speak(f"{application_name} has been added successfully.")

def get_application_command(application_name):
    applications = {}
    if os.path.isfile("applications.json"):
        with open("applications.json", "r") as file:
            applications = json.load(file)
    return applications.get(application_name)
def open_instagram():
    speak("Opening Instagram.")
    webbrowser.open("https://www.instagram.com")

def close_tab():
    pyautogui.hotkey("ctrl", "w")

def restart():
    speak("Restarting.")
    subprocess.call(["shutdown", "/r"])

def shutdown():
    speak("Shutting down.")
    subprocess.call(["shutdown", "/s"])

def log_out():
    speak("Logging out.")
    subprocess.call(["shutdown", "/l"])
def sleep():
    speak("Going to sleep.")
    subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0") 

def todo():
    speak("What would you like to add to your to-do list?")
    todo_item = listen()
    if todo_item:
        todo_items = []
        if os.path.isfile("todo.json"):
            with open("todo.json", "r") as file:
                todo_items = json.load(file)
        todo_items.append(todo_item)
        with open("todo.json", "w") as file:
            json.dump(todo_items, file)
        speak(f"{todo_item} has been added to your to-do list.")
def show_todo():
    todo_items = []
    if os.path.isfile("todo.json"):
        with open("todo.json", "r") as file:
            todo_items = json.load(file)
    if todo_items:
        speak("Here are the items on your to-do list:")
        for index, item in enumerate(todo_items):
            speak(f"{index + 1}. {item}")
    else:
        speak("Your to-do list is empty.")


def load_asistant_name():
     with open('names.json', 'r') as file:
        data = json.load(file)
        assistant_name = data['assistant_name']
     return assistant_name

 
def run_assistant():
    initialize_engine()
    applications = load_applications()
    speak("Hi, I'm your virtual assistant.")
    assistant_name, user_name = load_names()
    if not assistant_name or not user_name:
        assistant_name = get_assistant_name()
        user_name = get_user_name()
        save_names(assistant_name, user_name)
    while True:
        command = listen()
        if command:
            if command.lower() == assistant_name.lower():  # Eğer komut asistanın adı ise devam et
                 continue
            if "weather" in command or "hava durumu" in command:
                speak(f"{user_name}, which city's weather would you like to know?")
                city = listen()
                if city:
                    weather_info = get_weather(city)
                    if weather_info:
                        speak(weather_info)
                    else:
                        speak("Weather information could not be retrieved.")
                else:
                    speak("City information not understood. Please try again.")
            elif any(keyword in command for keyword in ["play a song", "sing a song", "play song", "şarkı çal", "müzik oynat"]):
                if "spotify" in command:
                    open_spotify()
                else:
                    url = "https://open.spotify.com/"
                    webbrowser.open(url)
                speak(f"{user_name}, which song would you like me to play?")
                track_name = listen()
                if track_name:
                    play_spotify_track(track_name)
                else:
                    speak("Song information not understood. Please try again.")
            elif any(keyword in command for keyword in ["resume", "resume music", "şarkıyı devam ettir", "devam ettir", "müziği devam ettir"]):
                resume_song()
            elif any(keyword in command for keyword in ["pause", "pause music", "şarkıyı durdur", "duraklat", "müziği durdur"]):
                pause_song()
            elif any(keyword in command for keyword in ["play the next song", "next song", "sonraki şarkıyı çal", "sonraki şarkı"]):
                play_next_song()
            elif any(keyword in command for keyword in ["play the prev song", "prev song", "önceki şarkıyı çal", "önceki şarkı"]):
                play_previous_song()
            elif any(greeting in command for greeting in ["hello", "hi", "hey", "selam"]):
                speak(f"Hello, {user_name}! How can I assist you?")
            elif any(keyword in command for keyword in ["close Fivem", "fivem'i kapat", "gta kapat", "close gta", "close gta v", "gta v kapat"]):
                speak("Closing Fivem.")
                subprocess.Popen("taskkill /f /im FiveM.exe")
            elif any(keyword in command for keyword in ["closing epic games", "epic games'i kapat"]):
                speak("Closing Epic Games.")
                subprocess.Popen("taskkill /f /im EpicGamesLauncher.exe")
            elif any(keyword in command for keyword in ["close lol", "lol'ü kapat", "close league of legends"]):
                speak("Closing League of Legends.")
                subprocess.Popen("taskkill /f /im LeagueClient.exe")
            elif any(keyword in command for keyword in ["close discord", "discord'u kapat"]):
                 speak("Closing Discord.")
                 subprocess.Popen("taskkill /f /im Discord.exe")
            elif any(keyword in command for keyword in ["close steam", "steam'i kapat"]):
                  speak("Closing Steam.")
                  subprocess.Popen("taskkill /f /im Steam.exe")
            elif any(keyword in command for keyword in ["close spotify", "spotify'ı kapat"]):
                 speak("Closing Spotify.")
                 subprocess.Popen("taskkill /f /im Spotify.exe")
            elif any(keyword in command for keyword in ["open", "open application", "uygulama aç", "uygulma çalıştr", "uygulama başlat", "run application"]):
                  application_name = command.replace("open", "").replace("aç", "").replace("application", "").replace("uygulama", "").replace("çalıştır", "").replace("başlat", "").replace("run", "").strip()
                  open_application(application_name)
            elif "add application" in command or "uygulama ekle" in command:
                add_application()
            elif "which command" in command.lower():
                speak("Sure, which application's command would you like to know?")
                application_name = listen()
                command = get_application_command(application_name)
                if command:
                    speak(f"To open {application_name}, you can say: {command}")
                else:
                    speak("Sorry, I couldn't find the command for that application.")
            elif any(keyword in command for keyword in ["open instagram", "instagram'ı aç"]):
                speak("Opening Instagram.")
                open_instagram()
            elif any(keyword in command for keyword in ["close tab", "sekmeyi kapat", "sekme kapat"]):
                speak("Closing the tab.")
                close_tab()
            elif any(keyword in command for keyword in ["set an alarm", "alarm kur", "alarm ayarla"]):
                set_alarm()
            elif any(keyword in command for keyword in ["close instagram", "instagramı kapat"]):
                speak("Closing Instagram.")
                close_tab()
            elif any(keyword in command for keyword in ["open notepad", "not defterini aç"]):
                speak("Opening Notepad.")
                subprocess.Popen("notepad.exe")
            elif any(keyword in command for keyword in ["close notepad", "not defterini kapat"]):
                speak("Closing Notepad.")
                subprocess.Popen("taskkill /f /im notepad.exe")
            elif any(keyword in command for keyword in ["search", "find", "ara"]):
                search_web()
            elif any(keyword in command for keyword in ["go to", "go", "git"]):
                website = command.replace("go to", "").replace("go", "").replace("git", "").strip()
                open_website(website)
            elif any(keyword in command for keyword in ["take a screenshot", "ekran görüntüsü al", "screenshot al"]):
                take_screenshot()
            elif any(keyword in command for keyword in ["what is your name", "adın ne", "ismin ne"]):
                speak("My name is Assistant.")
            elif any(keyword in command for keyword in ["thank you", "thanks", "teşekkür ederim", "sağ ol"]):
                speak("You're welcome!")
            elif any(keyword in command for keyword in ["what is the time", "saat kaç", "saat kaç şimdi", "saat kaç şuan", "saat kaç oldu", "saat kaç oldu şimdi", "saat kaç oldu şuan"]):
                speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}.")
            elif any(keyword in command for keyword in ["bugün günlerden ne", "hangi gündeyiz"]):
                speak(f"Today is {datetime.datetime.now().strftime('%A')}.")
            elif any(keyword in command for keyword in ["bilgisayarı kapat", "shut down computer", "pc kapat"]):
                speak("Shutting down the computer.")
                shutdown()
            elif any(keyword in command for keyword in ["bilgisayarı yeniden başlat", "restart computer", "pc'i yeniden başlat"]):
                 speak("Restarting the computer.")
                 restart()        
            elif any(keyword in command for keyword in ["oturumu kapat", "oturumdan çık", "log out", "log out of computer"]):
                 speak("Logging out of the computer.")
                 log_out()
            elif any(keyword in command for keyword in ["bilgisayarı uykuya gönder", "uykuya gönder", "sleep computer", "sleep", "bilgisayarı uyut", "uyut", "bilgisayarı uyku moduna al", "uyku moduna al"]):
                 speak("Putting the computer to sleep.")
                 sleep()
            elif any(keyword in command for keyword in ["todo list oluştur", "todo list yap", "todo list yap", "todo list oluştur", "todo", "yapılacaklar listesi oluştur"]):
                 speak("Creating Todo List.")
                 todo()
            elif any(keyword in command for keyword in ["show to do", "yapılacaklar listesini göster", "todo list göster", "todo listi göster", "todo listi aç", "todo list", "todo list aç", "todo listi görüntüle", "todo list görüntüle", "todo listi gör", "todo list gör"]):
                 speak("Opening Todo List.")
                 show_todo()

            elif any(keyword in command for keyword in ["uykuya gidebilirsin", "uykuya geçebilirsin", "uykuya geç", "stand by" ]):
                 standby_assistant()
            
            elif any(keyword in command for keyword in ["exit", "quit", "kapat", "çıkış", "goodbye", "bye", "güle güle", "görüşürüz", "bye bye"]):
             speak("Goodbye!")
             break
        else:  # Hiç komut alınmazsa
            break

run_assistant()
