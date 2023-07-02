import os
import webbrowser
import subprocess
import speech_recognition as sr
import pyttsx3
import psutil
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
from PIL import Image, ImageTk, ImageDraw, ImageFont
import ctypes
current_date = datetime.datetime.now().date()
current_day = current_date.strftime("%A")  # Haftanın gününü almak için
current_month = current_date.strftime("%B")  # Ayın adını almak için
current_year = current_date.year  # Yıl bilgisini almak için
# .env dosyasından çevre değişkenlerini yükle
load_dotenv()
engine = pyttsx3.init()
# Başlık metnini ayarlamak için SetConsoleTitle fonksiyonunu kullanma
def set_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# İkonu değiştirmek için SetConsoleIcon fonksiyonunu kullanma
def set_cmd_icon(icon_path):
    ctypes.windll.kernel32.SetConsoleIcon(icon_path)

# Başlık ve ikonu ayarlama
set_cmd_title("Niko Voice Asistant")
set_cmd_icon("logo.ico")
def show_logo():
    # Niko yazısı ve kalp ikonu oluşturuluyor
    logo = [
        "NNNNNNNN        NNNNNNNNIIIIIIIIIIIKKKKKKKK    KKKKKKK      OOOOOOOOO000",
        "N:::::::N       N::::::NI::::::::IK:::::::K    K:::::K    OO:::::::::OO0",
        "N::::::::N      N::::::NI::::::::IK:::::::K    K:::::K  OO:::::::::::::OO",
        "N:::::::::N     N::::::NII::::::IIKK::::::K    K:::::K O:::::::OOO:::::0O",
        "N::::::::::N    N::::::N  I::::I    K:::::K K:::::K  O::::::O   O:::::::00",
        "N:::::::::::N   N::::::N  I::::I    K::::::K:::::K   O:::::O     O:::::OOO",
        "N:::::::N::::N  N::::::N  I::::I    K:::::::::::K    O:::::O     O:::::OO",
        "N::::::N N::::N N::::::N  I::::I    K:::::::::::K    O:::::O     O:::::OO",
        "N::::::N  N::::N:::::::N  I::::I    K::::::K:::::K   O:::::O     O:::::O0",
        "N::::::N   N:::::::::::N  I::::I    K:::::K K:::::K  O::::::O   O:::::::O0",
        "N::::::N    N::::::::::N  I::::I    KK::::::K  K:::::KO:::::::OOO:::::::O0",
        "N::::::N     N:::::::::N  I::::I      K:::::::K   K:::::KO:::::::::::::OO",
        "N::::::N      N::::::::NII::::::II    K:::::::K    K:::::KO:::::::::OOOO",
        "N::::::N       N:::::::NI::::::::I    K:::::::K    K:::::K OO::::::::0OO",
        "NNNNNNNN        NNNNNNNNIIIIIIIIII    KKKKKKKKK    KKKKKKK   OOOOOOOOO",
    ]


    heart = [
        "     ♥♥♥♥     ♥♥♥♥     ",
        "   ♥♥     ♥♥ ♥♥     ♥♥   ",
        " ♥♥         ♥♥         ♥♥ ",
        " ♥♥                   ♥♥ ",
        "   ♥♥               ♥♥   ",
        "     ♥♥           ♥♥     ",
        "       ♥♥       ♥♥       ",
        "         ♥♥   ♥♥         ",
        "           ♥♥♥           "
    ]

        # "Niko Voice Asistan Açılıyor" yazısını ekrana yazdırma
    print("\nNiko Voice Asistan Açılıyor...\n")

    # Niko yazısı ve kalp ikonunu ekrana yazdırma
    for line in logo:
        print(line)
    
    print("\n")  # Boş bir satır bırakma
    
    for line in heart:
        print(line)

def initialize_engine():
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def load_asistant_name():
     with open('names.json', 'r') as file:
        data = json.load(file)
        assistant_name = data['assistant_name']
     return assistant_name
    
def unknown_command():
    print("Bilinmeyen komut!")

def is_site_opened(url):
    try:
        port = url.split(':')[2]
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN' and port in str(conn.laddr):
                return True
        return False
    except IndexError:
        return False

def get_assistant_name():
    assistant_name = input("What should be my name? ")
    return assistant_name


def get_user_name():
    try:
        with open("names.json", "r") as file:
            data = json.load(file)
            user_name = data.get("user_name")
            if user_name:
                return user_name
    except FileNotFoundError:
        pass
    
    user_name = input("What is your name?")
    save_names(user_name=user_name)
    return user_name

def save_names(assistant_name=None, user_name=None):
    data = {}
    if assistant_name:
        data["assistant_name"] = assistant_name
    if user_name:
        data["user_name"] = user_name
    
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

def save_applications(applications):
    with open('applications.json', 'w') as file:
        json.dump(applications, file)    
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



# Spotify yetkilendirme ayarları
scope = "user-read-playback-state,user-modify-playback-state,playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
is_spotify_opened = False  # global değişken olarak tanımlanması
is_playing = False
def play_playlist(playlist_index=None):
   
    playlists = sp.current_user_playlists()["items"]
    num_playlists = len(playlists)
    global is_spotify_opened
    global is_playing
    load_names()
    user_name = get_user_name()
    if is_playing is True:
        pause_song()
        is_playing = False
    if is_spotify_opened:
        if playlist_index is None:
            speak(f"{user_name}, which playlist would you like me to play?")
            playlist_index = listen()
            if playlist_index:
                playlist_index = int(playlist_index) - 1  # Convert to integer here
                if playlist_index < 0 or playlist_index >= num_playlists:
                    speak("Invalid playlist index. Please try again.")
                else:
                    # Pause the current playback if any
                    sp.pause_playback()

                    playlist_id = playlists[playlist_index]["id"]
                    sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
                    is_playing = True
    else:
        url = "https://open.spotify.com/"
        if not is_site_opened(url):
            webbrowser.open(url)
            is_spotify_opened = True
            if playlist_index is None:
                speak(f"{user_name}, which playlist would you like me to play?")
                playlist_index = listen()
                if playlist_index:
                    playlist_index = int(playlist_index) - 1  # Convert to integer here
                    if playlist_index < 0 or playlist_index >= num_playlists:
                        speak("Invalid playlist index. Please try again.")
                    else:
                        # Pause the current playback if any
                        sp.pause_playback()

                        playlist_id = playlists[playlist_index]["id"]
                        sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
                        is_playing = True



def play_spotify_track(track_name=None):
    global is_spotify_opened
    load_names()
    user_name = get_user_name()

    if is_spotify_opened:
        if not track_name:
            speak( user_name + "," "Which song would you like me to play?")
            track_name = listen()
    else:
        url = "https://open.spotify.com/"
        if not is_site_opened(url):
            webbrowser.open(url)
            is_spotify_opened = True
            if not track_name:
                speak( user_name + ","  "Which song would you like me to play?")
                track_name = listen()
                if track_name:
                    play_spotify_track(track_name)  # Şarkıyı çalma komutunu tekrar çağır
                    return  # Geri kalan kodu çalıştırmayı durdur

    if track_name:
        results = sp.search(q=track_name, limit=1, type="track")
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            devices = sp.devices()
            target_device_id = None
            for device in devices["devices"]:
                if device["type"] == "Computer":
                    target_device_id = device["id"]
                    break
            if target_device_id:
                sp.start_playback(uris=[track_uri], device_id=target_device_id)
                current_track_name = results["tracks"]["items"][0]["name"]
                speak("Şu anda çalınıyor: " + current_track_name)
            else:
                speak("Çalınacak bir cihaz bulunamadı.")
        else:
            speak("Üzgünüm, o şarkıyı bulamadım.")


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
 
def volume_up():
    for _ in range(5):
        pyautogui.press('volumeup')

def volume_down():
 for _ in range(5):
    pyautogui.hotkey('volumedown')
def search_web():
    speak("What would you like to search for?")
    query = listen()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here is what I found for " + query)


def open_website(website=None):
    if not website:
        speak("Which website would you like to visit?")
        website = listen()
    website = website.replace(" ", "")
    url = f"https://{website}.com"
    webbrowser.open(url)
    speak("Opening " + website)

def what_time():
    speak(speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}."))

def what_today():
    speak(f"Today is {datetime.datetime.now().strftime('%A')}.")



def set_alarm():
    speak("What time would you like to set the alarm?")
    time_input = listen()
    speak(f"Alarm set for {time_input}.")
    time_input = time_input.replace(".", ":").replace(",", ":").replace(" ", "")
    if len(time_input) == 4:
        time_input = time_input[:2] + ":" + time_input[2:]
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
                execute_command("alarm")  # Execute alarm-specific commands
                break

            # Check for new commands during the alarm
            command = listen().lower()
            if "stop" in command.lower() or "cancel" in command.lower():
                speak("Alarm canceled.")
                break

            execute_command(command)

    except ValueError:
        speak("Invalid time format. Please try again.")
        return








def get_weather(city=None):
    if not city:
        speak("Which city's weather would you like to know?")
        city = listen()
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en&aqi=no"
    response = requests.get(url)
    weather_data = response.json()
    if "current" in weather_data:
        weather_description = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        speak(f"Weather for {city}: {weather_description}, temperature: {temperature} degrees")
    else:
        speak("Sorry, I couldn't retrieve the weather information for that city.")


def open_spotify():
    speak("Opening Spotify.")
    subprocess.Popen("C:\\Users\\omere\\AppData\\Roaming\\Spotify\\Spotify.exe")


def open_application():
    speak("Which application would you like to open?")
    application_name = listen()
    applications = load_applications()

    if application_name in applications:
        application_path = applications[application_name]
        speak(f"Opening {application_name}.")
        subprocess.Popen(application_path)
    else:
        speak(f"Sorry, I couldn't find the {application_name} application. Please provide the location of the application.")
        application_path = filedialog.askopenfilename(title="Select Application")

        if os.path.exists(application_path):
            speak(f"Opening {application_name}.")
            subprocess.Popen(application_path)
            applications[application_name] = application_path
            save_applications(applications)
        else:
            speak("Sorry, I couldn't find the application at the specified location.")

def close_application():
    speak("Which application would you like to close?")
    application_name = listen()

    for proc in psutil.process_iter(['name']):
        try:
            process_name = proc.name().lower()
            if application_name.lower() in process_name or application_name.lower() + '.exe' in process_name:
                speak(f"Closing {application_name}.")
                proc.terminate()
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    speak(f"Sorry, I couldn't find the {application_name} application running.")


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
    speak("Closing tab")
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



 
def execute_command(command):
    global is_spotify_opened  # is_spotify_opened değişkenini global olarak kullanmak için eklenen satır
    commands = {
        "şarkı çal": play_spotify_track,
        "sonraki şarkı": play_next_song,
        "önceki şarkı": play_previous_song,
        "şarkıyı durdur": pause_song,
        "hava durumu": get_weather,
        "web siteyi aç": open_website,
        "alarm kur": set_alarm,
        "ekran görüntüsü al": take_screenshot,
        "uygulame ekle": add_application,
        "bilgisayarı yeniden başlat" : restart,
        "oturumu kapat" : log_out,
        "saat kaç" : what_time,
        "sesi arttır" : volume_up,
         "sesi azalt" : volume_down,
        "hangi gündeyiz" : what_today,
        "yapılacaklar listesine ekle" : todo,
        "yapılacaklar listesini göster" : show_todo,
         "sekmeyi kapat": close_tab,
         "instagram'ı aç": open_instagram,
        "şarkıyı devam ettir": resume_song,
        "web'de ara": search_web,
        "uygulama aç": open_application,
        "uygulama kapat": close_application,
        "oynatma listemi çal": play_playlist,
        "bilgisayarı kapat" : shutdown,
        # diğer komutlar burada eklenebilir
    }


    if command in commands:
        commands[command]()
    else:
        unknown_command()

 
def run_assistant():
    initialize_engine()
    applications = load_applications()
    user_name = get_user_name()
    current_time = datetime.datetime.now().strftime('%H:%M')
    day = datetime.datetime.now().strftime('%A')
    speak(f"Hi, {user_name}! Today {day}. Time is {current_time}, How Can I Help You?")

    assistant_name, user_name = load_names()
    if not assistant_name or not user_name:
        assistant_name = get_assistant_name()
        user_name = get_user_name()
        save_names(assistant_name, user_name)
    while True:
        command = listen().lower()
        print("Alınan komut:", command)  # Sorunları ayıklama amacıyla alınan komutu yazdırma
        execute_command(command)



if __name__ == "__main__":
    show_logo()  # Logo gösterimini yapın
    time.sleep(3)  # Logonun gösterim süresini bekleyin
    run_assistant()

run_assistant()
