import os
import webbrowser
import subprocess
from gtts import gTTS
import pygame
import speech_recognition as sr
import pyttsx3
import psutil
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")
import json
import datetime
import pyautogui
import tkinter as tk
from tkinter import filedialog
import threading
import time
import ctypes
import pygetwindow as gw
import re
from difflib import SequenceMatcher

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
        "           ♥♥♥           ",
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
    tts = gTTS(text=text, lang="tr")  # 'tr' dil kodu Türkçe'yi temsil eder
    tts.save("output.mp3")  # Ses dosyasını kaydet

    # pygame ile ses dosyasını çal
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    # Ses dosyasının tamamlanmasını bekleyin
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(
            10
        )  # Ses dosyasının çalmasını beklerken döngüyü düzenler

    # Ses çalma tamamlandığında ses dosyasını temizle
    pygame.mixer.quit()
    os.remove("output.mp3")


def load_asistant_name():
    with open("names.json", "r") as file:
        data = json.load(file)
        assistant_name = data["assistant_name"]
    return assistant_name


def unknown_command():
    print("Bilinmeyen komut!")


def is_site_opened(url):
    try:
        port = url.split(":")[2]
        for conn in psutil.net_connections():
            if conn.status == "LISTEN" and port in str(conn.laddr):
                return True
        return False
    except IndexError:
        return False


def get_assistant_name():
    try:
        with open("names.json", "r") as file:
            data = json.load(file)
            assistant_name = data.get("assistant_name")
            if assistant_name:
                return assistant_name
    except FileNotFoundError:
        assistant_name = input("Adımı ne koymak istersiniz? ")


def get_user_name():
    try:
        with open("names.json", "r") as file:
            data = json.load(file)
            user_name = data.get("user_name")
            if user_name:
                return user_name
    except FileNotFoundError:
        pass

    user_name = input("Adınız nedir?")
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


def save_applications(applications):
    with open("applications.json", "w") as file:
        json.dump(applications, file)


# def listen():
#     recognizer = sr.Recognizer()

#     while True:
#         with sr.Microphone() as source:
#             recognizer.adjust_for_ambient_noise(source)
#             print("Sesinizi dinliyorum...")
#             audio = recognizer.listen(source, phrase_time_limit=6)

#         try:
#             text = recognizer.recognize_google(audio, language="tr-TR")
#             print("Ses algılandı: " + text)
#             return text
#         except sr.UnknownValueError:
#             print("Ses anlaşılamadı.")
#         except sr.RequestError as e:
#             print("Ses tanıma servisi çalışmıyor; {0}".format(e))

#         time.sleep(1)  # 1 saniye bekle ve tekrar dinle


def listen(silence_duration=0.2, total_duration=10):
    recognizer = sr.Recognizer()
    text = ""

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_adjustment_ratio = (
            1.5  # Increase if ambient noise is high
        )
        recognizer.dynamic_energy_adjustment_damping = 0.15

        print("Dinliyorum...")
        audio = recognizer.listen(
            source, timeout=total_duration, phrase_time_limit=total_duration
        )

    try:
        text = recognizer.recognize_google(audio, language="tr-TR")
        print("Konuşma algılandı: " + text)
        return text
    except sr.UnknownValueError:
        print("Konuşma tanınmadı.")
    except sr.RequestError as e:
        print("Konuşma tanıma hizmeti kullanılamıyor; {0}".format(e))

    # Kullanıcının cümlesi tamamlanmamış veya tamamen sessiz ise sessizlik süresini ayarlayarak tekrar dinleme yap
    if len(text) == 0 or not any(char.isalpha() for char in text):
        if silence_duration < 5:
            print("Cümle uzun. Sessizlik süresi ayarlanıyor...")
            time.sleep(silence_duration)  # Sessizlik süresi kadar beklet
            return listen(
                silence_duration=silence_duration + 1, total_duration=total_duration
            )

    # Kullanıcının cümlesi kısa ise hemen dön, sessizlik süresini ayarlamadan
    if len(text.split()) <= 3:
        return text

    # Cümlenin uzunluğuna göre sessizlik süresini ayarla
    adjusted_silence_duration = silence_duration + len(text.split()) // 3
    if adjusted_silence_duration > 5:
        adjusted_silence_duration = 5

    print("Cümle uzun. Sessizlik süresi ayarlanıyor...")
    time.sleep(adjusted_silence_duration)  # Sessizlik süresi kadar beklet
    return listen(
        silence_duration=adjusted_silence_duration, total_duration=total_duration
    )


def extract_playlist_number(response):
    # Extract playlist number from the response using regular expression
    match = re.search(r"\b(\d+)\b", response)
    if match:
        return match.group(1)
    else:
        return None


def play_user_playlist(playlist_number=None):
    global is_spotify_opened
    load_names()
    user_name = get_user_name()

    if is_spotify_opened:
        if not playlist_number:
            speak(
                user_name
                + ", Hangi şarkı listesini çalmamı istersiniz? You can say the number."
            )
            response = listen()

            # Extract playlist number from the response
            playlist_number = extract_playlist_number(response)

    else:
        url = "https://open.spotify.com/"
        if not is_site_opened(url):
            webbrowser.open(url)
            is_spotify_opened = True
            if not playlist_number:
                speak(
                    user_name
                    + ", Hangi şarkı listesini çalmamı istersiniz? You can say the number."
                )
                response = listen()

                # Extract playlist number from the response
                playlist_number = extract_playlist_number(response)

                if playlist_number:
                    play_user_playlist(playlist_number)
                    return

    if playlist_number:
        user_playlists = sp.current_user_playlists(limit=50)
        if user_playlists["items"]:
            playlist_index = int(playlist_number) - 1
            if playlist_index < len(user_playlists["items"]):
                playlist_uri = user_playlists["items"][playlist_index]["uri"]
                devices = sp.devices()
                target_device_id = None
                for device in devices["devices"]:
                    if device["type"] == "Computer":
                        target_device_id = device["id"]
                        sp.transfer_playback(
                            device_id=target_device_id, force_play=True
                        )
                        break
                if target_device_id:
                    sp.start_playback(
                        device_id=target_device_id, context_uri=playlist_uri
                    )
                    current_playlist_name = user_playlists["items"][playlist_index][
                        "name"
                    ]
                    speak("şu anda çalıyor: " + current_playlist_name)
                else:
                    speak("Oynatmak için uygun cihaz bulunamadı.")
            else:
                speak("Belirtilen oynatma listesi numarası geçerli değil.")
        else:
            speak("Kendi çalma listelerinizi bulamadım.")


# Spotify yetkilendirme ayarları
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
is_spotify_opened = False  # global değişken olarak tanımlanması
is_playing = False


def play_playlist(playlist_name=None):
    global is_spotify_opened
    load_names()
    user_name = get_user_name()

    if is_spotify_opened:
        speak("Kendi çalma listenizden çalmamı ister misiniz?")
        own = listen().lower()
        if own == "evet" or own == "yes":
            play_user_playlist()
            return
        elif own == "hayır" or own == "no":
            if not playlist_name:
                speak(user_name + ", Hangi şarkı listesini çalmamı istersiniz?")
                playlist_name = listen()
    else:
        url = "https://open.spotify.com/"
        if not is_site_opened(url):
            webbrowser.open(url)
            is_spotify_opened = True
            if not playlist_name:
                speak(user_name + ", Hangi şarkı listesini çalmamı istersiniz?")
                playlist_name = listen()
                if playlist_name:
                    play_playlist(playlist_name)
                    return

    if playlist_name:
        results = sp.search(q=playlist_name, limit=1, type="playlist")
        if results["playlists"]["items"]:
            playlist_uri = results["playlists"]["items"][0]["uri"]
            devices = sp.devices()
            target_device_id = None
            for device in devices["devices"]:
                if device["type"] == "Computer":
                    target_device_id = device["id"]
                    break
            if target_device_id:
                sp.start_playback(device_id=target_device_id, context_uri=playlist_uri)
                current_playlist_name = results["playlists"]["items"][0]["name"]
                speak("Şu an da çalıyor: " + current_playlist_name)
            else:
                speak("Oynatmak için uygun cihaz bulunamadı.")
        else:
            speak("Üzgünüm o oynatma listesini bulamadım.")


def set_device_for_spotify():
    speak(
        "Spotify fonksiyonunun düzgün çalışması için bilgisayarınızda Spotify programını açmayı unutmayın!"
    )
    global is_spotify_opened
    is_spotify_opened = True
    devices = sp.devices()
    target_device_id = None
    for device in devices["devices"]:
        if device["type"] == "Computer":
            target_device_id = device["id"]
            break
    if target_device_id:
        sp.transfer_playback(device_id=target_device_id, force_play=False)
    else:
        is_spotify_opened = False



def resume_song():
    sp.start_playback()
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"Şarkı devam ediyor. şu an da: {track_name}")
    else:
        speak("Şarkı devam ediyor.")


def pause_song():
    sp.pause_playback()
    speak("Şarkı durduruldu.")


def play_next_song():
    sp.next_track()
    time.sleep(1)  # Şarkı değişikliğinin tamamlanması için bir süre bekleyin
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"Sonraki şarkıyı çalıyorum: {track_name}")
    else:
        speak("Sonraki şarkı.")


def play_previous_song():
    sp.previous_track()
    time.sleep(1)  # Şarkı değişikliğinin tamamlanması için bir süre bekleyin
    current_track = sp.current_user_playing_track()
    if current_track:
        track_name = current_track["item"]["name"]
        speak(f"Önceki şarkıyı çalıyorum: {track_name}")
    else:
        speak("Önceki şarkı")


def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")


def volume_down():
    for _ in range(5):
        pyautogui.hotkey("volumedown")


def search_web():
    speak("Neyi aramak istersiniz?")
    query = listen()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("İşte şunu buldum" + query)


def open_website(website=None):
    if not website:
        speak("Hangi web sitesini ziyaret etmek istersiniz?")
        website = listen()
    website = website.replace(" ", "")
    url = f"https://{website}.com"
    webbrowser.open(url)
    speak("Şu web sitesini açıyorum" + website)


def what_today():
    # Gün ismini Türkçe olarak almak için bir sözlük kullanabiliriz
    turkish_days = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }

    # İngilizce gün adını al
    day = datetime.datetime.now().strftime("%A")

    # Türkçe gün ismini almak için sözlüğü kullan
    turkish_day = turkish_days.get(day, day)

    speak(f"Bugün {turkish_day}.")


def load_alarms():
    try:
        with open("alarms.json", "r") as file:
            alarms = json.load(file)
            return alarms
    except FileNotFoundError:
        return []


def save_alarms(alarms):
    with open("alarms.json", "w") as file:
        json.dump(alarms, file)


def set_alarm():
    alarms = load_alarms()

    speak("Alarmı saat kaça kurmak istersiniz?")
    time_input = listen()
    speak(f"Alarm set for {time_input}.")
    time_input = time_input.replace(".", ":").replace(",", ":").replace(" ", "")
    if len(time_input) == 4:
        time_input = time_input[:2] + ":" + time_input[2:]
    try:
        alarm_time = datetime.datetime.strptime(time_input, "%H:%M").time()
        current_time = datetime.datetime.now().time()
        if alarm_time < current_time:
            speak("Belirtilen süre zaten geçti. Lütfen gelecekteki bir zamanı girin.")
            return

        alarm = {"time": str(alarm_time), "status": "active"}
        alarms.append(alarm)
        save_alarms(alarms)

        while True:
            current_time = datetime.datetime.now().time()
            if current_time >= alarm_time:
                speak("Alarm zamanı!")
                execute_command("alarm")  # Execute alarm-specific commands
                break

            # Check for new commands during the alarm
            command = listen().lower()
            if "stop" in command.lower() or "cancel" in command.lower():
                speak("Alarm iptal edildi.")
                alarms.remove(alarm)
                save_alarms(alarms)
                break

            execute_command(command)

    except ValueError:
        speak("Geçersiz zaman biçimi. Lütfen tekrar deneyin.")
        return


def get_weather(city=None):
    if not city:
        speak("Hangi şehrin hava durumunu bilmek istersiniz?")
        city = listen()
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en&aqi=no"
    response = requests.get(url)
    weather_data = response.json()
    if "current" in weather_data:
        weather_description = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        speak(
            f"{city} için hava durumu: {weather_description}, sıcaklık: {temperature} derece"
        )
    else:
        speak("Maalesef o şehrin hava durumu bilgisini alamadım.")


def open_spotify():
    speak("Spotify'ı açıyorum.")
    subprocess.Popen("C:\\Users\\omere\\AppData\\Roaming\\Spotify\\Spotify.exe")


def what_time_is_it():
    speak("şu an saat " + datetime.datetime.now().strftime("%H:%M"))


def open_application(application_name):
    applications = load_applications()
    application_name = (
        application_name.replace("'u", "").replace("'ı", "").strip()
    )  # Tek tırnak içindeki 'u' ve 'ı' karakterlerini çıkaralım
    if application_name in applications:
        application_path = applications[application_name]

    # Uygulama adını büyük harfe çevirelim
    application_name = application_name.lower()

    for app in applications:
        if app.lower() in application_name:
            application_path = applications[app]
            speak(f"{app} açılıyor.")
            subprocess.Popen(application_path)
            return

    # Eşleşme bulunamadıysa buraya kadar gelecek
    speak(f"Üzgünüm, ilgili uygulamayı bulamadım.")
    speak(f"Lütfen {application_name} uygulamasının konumunu belirtin.")
    application_path = filedialog.askopenfilename(
        title=f"{application_name} adlı Uygulamasını bir dahaki sefere hatırlamam için seçin"
    )

    if os.path.exists(application_path):
        speak(f"{application_name} açılıyor.")
        subprocess.Popen(application_path)
        applications[application_name] = application_path
        save_applications(applications)
    else:
        speak(f"Sorry, I couldn't find the {application_name} application.")
        speak(f"Lütfen {application_name} uygulamasının konumunu belirtin.")
        application_path = filedialog.askopenfilename(
            title=f"{application_name} adlı Uygulamasını bir dahaki sefere hatırlamam için seçin"
        )
        speak("Üzgünüm uygulamayı bulamadım.")

        if os.path.exists(application_path):
            speak(f"{application_name} açılıyor.")
            subprocess.Popen(application_path)
            applications[application_name] = application_path
            save_applications(applications)
        else:
            speak("Üzgünüm uygulamayı bulamadım.")


def search_application(application_name):
    try:
        with open("applications.json", "r") as file:
            applications = json.load(file)
            return applications.get(application_name)
    except FileNotFoundError:
        return None


def load_applications():
    try:
        with open("applications.json", "r") as file:
            applications = json.load(file)
            return applications
    except FileNotFoundError:
        return {}


# Other functions omitted for brevity


def close_application():
    speak("Hangi uygulamayı kapatmak istiyorsunuz?")
    application_name = listen()

    try:
        subprocess.run(["taskkill", "/F", "/IM", application_name + ".exe"], check=True)
        speak(f"{application_name} başarıyla kapatıldı.")
    except subprocess.CalledProcessError:
        speak(f"Üzgünüm, çalışan {application_name} uygulamasını bulamadım.")


def play_song(song_name=None):
    if not song_name:
        speak("Hangi şarkıyı çalmak istiyorsunuz?")
        song_name = listen()

    if song_name:
        speak(f"{song_name} şarkısını hangi platformdan çalmak istersiniz, YouTube'dan mı yoksa Spotify'dan mı?")
        platform = listen().lower()

        if platform == "spotify":
            play_spotify_track(song_name)
        elif platform == "youtube":
            play_youtube(song_name)
        else:
            speak("Üzgünüm, platformu anlamadım. Lütfen tekrar deneyin.")

def play_youtube(track_name=None):
    if not track_name:
        speak("Hangi şarkıyı çalmamı istersiniz?")
        track_name = listen()

    if track_name:
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("YOUTUBE_API_KEY")

        if api_key:
            search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={track_name.replace(' ', '+')}&key={api_key}"
            response = requests.get(search_url)
            json_data = response.json()

            if "items" in json_data and len(json_data["items"]) > 0:
                video_id = json_data["items"][0]["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                webbrowser.open(video_url)
                speak("YouTube'dan şarkı çalınıyor: " + track_name)
            else:
                speak("Üzgünüm, YouTube'da eşleşen video bulamadım.")
        else:
            speak(
                "YouTube API anahtarı bulunamadı. Lütfen .env dosyasında API anahtarınızı ayarladığınızdan emin olun."
            )


def play_spotify_track(track_name=None):
    global is_spotify_opened
    load_names()
    user_name = get_user_name()

    if is_spotify_opened:
        if not track_name:
            speak(user_name + ", Hangi şarkıyı çalmamı istersiniz?")
            track_name = listen()
    else:
        url = "https://open.spotify.com/"
        if not is_site_opened(url):
            webbrowser.open(url)
            is_spotify_opened = True
            if not track_name:
                speak(user_name + ", Hangi şarkıyı çalmamı istersiniz?")
                track_name = listen()
                if track_name:
                    play_spotify_track(track_name)
                    return

    if track_name:
        results = sp.search(q=track_name, limit=1, type="track")
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            devices = sp.devices()
            target_device_id = None
            for device in devices["devices"]:
                if device["type"] == "Computer":
                    target_device_id = device["id"]
                    sp.transfer_playback(device_id=target_device_id, force_play=True)
                    break
            if target_device_id:
                sp.start_playback(device_id=target_device_id, uris=[track_uri])
                current_track_name = results["tracks"]["items"][0]["name"]
                speak("Şu anda çalınıyor: " + current_track_name)
            else:
                speak("Oynatılacak kullanılabilir cihaz yok.")
        else:
            speak("Üzgünüm o şarkıyı bulamadım.")







def get_weather(city=None):
    if not city:
        speak("Hangi şehrin hava durumunu bilmek istersiniz?")
        city = listen()

    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=en&aqi=no"
    response = requests.get(url)
    weather_data = response.json()

    if "current" in weather_data:
        weather_description = weather_data["current"]["condition"]["text"]
        temperature = weather_data["current"]["temp_c"]
        speak(
            f"{city} için hava durumu: {weather_description}, sıcaklık: {temperature} derece"
        )
    else:
        speak("Maalesef o şehrin hava durumu bilgisini alamadım.")


def take_screenshot():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(file_path)
    speak("Ekran görüntüsü kaydedildi.")


def add_application():
    root = tk.Tk()
    speak("Elbette, hangi uygulamayı eklemek istiyorsunuz?")
    application_name = listen()
    speak("Lütfen uygulamanın konumunu seçin.")
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
        speak(f"{application_name} başarıyla eklendi.")


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
    speak("Yapılacaklar listenize ne eklemek istersiniz?")
    todo_item = listen()
    if todo_item:
        todo_items = []
        if os.path.isfile("todo.json"):
            with open("todo.json", "r") as file:
                todo_items = json.load(file)
        todo_items.append(todo_item)
        with open("todo.json", "w") as file:
            json.dump(todo_items, file)
        speak(f"{todo_item} yapılacaklar listenize eklendi.")


def show_todo():
    todo_items = []
    if os.path.isfile("todo.json"):
        with open("todo.json", "r") as file:
            todo_items = json.load(file)
    if todo_items:
        speak("Yapılacaklar listenizdeki öğeler şunlardır:")
        for index, item in enumerate(todo_items):
            speak(f"{index + 1}. {item}")
    else:
        speak("Yapılacaklar listeniz boş.")


def HeyAssistant():
    user_name = get_user_name()
    assistant_name = get_assistant_name()
    speak(f"Merhaba, ben {assistant_name}. Sana nasıl yardımcı olabilirim {user_name}?")


COMMANDS = {
    "şarkı çal": play_song,
    "play song": play_song,
    "sonraki şarkı": play_next_song,
    "next song": play_next_song,
    "önceki şarkı": play_previous_song,
    "previous song": play_previous_song,
    "şarkıyı durdur": pause_song,
    "pause song": pause_song,
    "hava durumu": get_weather,
    "weather": get_weather,
    "hey": HeyAssistant,
    "web siteyi aç": open_website,
    "open website": open_website,
    "alarm kur": set_alarm,
    "set alarm": set_alarm,
    "ekran görüntüsü al": take_screenshot,
    "take screenshot": take_screenshot,
    "uygulame ekle": add_application,
    "add application": add_application,
    "bilgisayarı yeniden başlat": restart,
    "restart computer": restart,
    "oturumu kapat": log_out,
    "log out": log_out,
    "saat kaç": what_time_is_it,
    "what time is it": what_time_is_it,
    "sesi arttır": volume_up,
    "increase volume": volume_up,
    "sesi azalt": volume_down,
    "decrease volume": volume_down,
    "hangi gündeyiz": what_today,
    "what day is it": what_today,
    "yapılacaklar listesine ekle": todo,
    "add to-do list": todo,
    "yapılacaklar listesini göster": show_todo,
    "show to-do list": show_todo,
    "sekmeyi kapat": close_tab,
    "close tab": close_tab,
    "instagram'ı aç": open_instagram,
    "open Instagram": open_instagram,
    "şarkıyı devam ettir": resume_song,
    "resume song": resume_song,
    "web'de ara": search_web,
    "search the web": search_web,
    "uygulama kapat": close_application,
    "close application": close_application,
    "oynatma listesi çal": play_playlist,
    "play  playlist": play_playlist,
    "bilgisayarı kapat": shutdown,
    "niko": HeyAssistant,
    "shut down computer": shutdown,
}


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def run_assistant():
    initialize_engine()
    applications = load_applications()
    user_name = get_user_name()

    # Gün ismini Türkçe olarak almak için bir sözlük kullanabiliriz
    turkish_days = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }

    current_time = datetime.datetime.now().strftime("%H:%M")
    day = datetime.datetime.now().strftime("%A")

    # Türkçe gün ismini almak için sözlüğü kullan
    turkish_day = turkish_days.get(day, day)

    speak(
        f"Merhaba {user_name}! Bugün {turkish_day}. Saat {current_time}, Size Nasıl Yardımcı Olabilirim?"
    )

    assistant_name, user_name = load_names()
    if not assistant_name or not user_name:
        assistant_name = get_assistant_name()
        user_name = get_user_name()
        save_names(assistant_name, user_name)

    # Start the main loop
    while True:
        # Listen for the user's response
        response = listen().lower()

        # Check if the response is in the list of commands
        if response in COMMANDS:
            COMMANDS[response]()
        else:
            # Find the most similar command
            matched_command = None
            highest_similarity = 0.7

            for key in COMMANDS:
                if similar(response, key) > highest_similarity:
                    matched_command = key
                    highest_similarity = similar(response, key)
                    break

            # If a similar command was found, ask the user if they meant that command
            if matched_command:
                # Speak the confirmation prompt
                speak(f"{matched_command} mı demek istediniz? (Evet Hayır):")
                print(f"{matched_command} mı demek istediniz? (Evet Hayır):")
                # Listen for the user's response
                second_response = listen().lower()

                # If the user said yes, execute the command
                if second_response == "evet" or second_response == "yes":
                    COMMANDS[matched_command]()
                else:
                    unknown_command()
            else:
                unknown_command()


if __name__ == "__main__":
    show_logo()  # Logo gösterimini yapın
    time.sleep(3)  # Logonun gösterim süresini bekleyin
    set_device_for_spotify()
    time.sleep(3)  # Logonun gösterim süresini bekleyin
    run_assistant()
