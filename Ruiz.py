# -*- coding: utf-8 -*-
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import webbrowser

import pyttsx3
import speech_recognition as sr

WAKE_PHRASE = "ey ruiz"
SILENCE_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8


class RuizAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self._set_voice()

    def _set_voice(self):
        for voice in self.engine.getProperty("voices"):
            name = voice.name.lower()
            if "female" in name or "zira" in name or "samantha" in name:
                self.engine.setProperty("voice", voice.id)
                return

    def say(self, text: str):
        print("Ruiz:", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout: int = SILENCE_TIMEOUT, phrase_time_limit: int = PHRASE_TIME_LIMIT) -> str:
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = self.recognizer.recognize_google(audio, language="es-ES")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.say("No puedo conectarme al servicio de reconocimiento. Revisa tu conexi�n a internet.")
            return ""

    def wait_for_wake_word(self) -> bool:
        self.say("Di \"ey ruiz\" cuando quieras que act�e.")
        while True:
            text = self.listen(timeout=10, phrase_time_limit=5)
            if not text:
                continue
            print("Escuchado:", text)
            if WAKE_PHRASE in text or "ruiz" in text:
                self.say("S�, estoy aqu�.")
                return True

    def process_command(self, text: str):
        print("Comando recibido:", text)

        if any(word in text for word in ["adi�s", "salir", "hasta luego"]):
            self.say("Hasta luego. Cuando quieras, dime ey ruiz.")
            sys.exit(0)

        if any(word in text for word in ["hora", "qu� hora", "qu� hora es"]):
            now = time.strftime("%H:%M")
            self.say(f"Son las {now}")
            return

        if any(word in text for word in ["busca", "buscar"]):
            search_term = text.replace("busca", "").replace("buscar", "").strip()
            if not search_term:
                self.say("�Qu� quieres que busque?")
                return
            self.say(f"Buscando {search_term} en internet.")
            webbrowser.open(f"https://www.google.com/search?q={search_term.replace(' ', '+')}")
            return

        if any(word in text for word in ["abre", "abrir"]):
            self._open_target(text)
            return

        if any(word in text for word in ["llama", "llamar"]):
            self._phone_call(text)
            return

        if any(word in text for word in ["mensaje", "sms", "env�a mensaje", "enviar mensaje"]):
            self._send_message(text)
            return

        if any(word in text for word in ["whatsapp", "whats" ]):
            self._open_whatsapp_android()
            return

        self.say(
            "No entend� el comando. Puedo abrir sitios, buscar en internet o controlar un Android conectado con adb."
        )

    def _is_adb_available(self) -> bool:
        return shutil.which("adb") is not None

    def _is_phone_connected(self) -> bool:
        if not self._is_adb_available():
            return False
        proc = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if proc.returncode != 0:
            return False
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        for line in lines[1:]:
            if line.endswith("\tdevice"):
                return True
        return False

    def _run_adb(self, args):
        return subprocess.run(["adb"] + args, capture_output=True, text=True)

    def _phone_call(self, text: str):
        if not self._is_phone_connected():
            self.say(
                "No hay tel�fono Android conectado o adb no est� disponible. Conecta el tel�fono y habilita USB debugging."
            )
            return
        digits = re.sub(r"\D", "", text)
        if not digits:
            self.say("Dime el n�mero al que quieres llamar.")
            return
        self.say(f"Llamando al {digits} en el tel�fono conectado.")
        self._run_adb(["shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{digits}"])

    def _send_message(self, text: str):
        if not self._is_phone_connected():
            self.say(
                "No hay tel�fono Android conectado o adb no est� disponible. Conecta el tel�fono y habilita USB debugging."
            )
            return
        digits = re.sub(r"\D", "", text)
        if not digits:
            self.say("Dime el n�mero para el mensaje.")
            return
        self.say("Abriendo la aplicaci�n de mensajes en el tel�fono.")
        self._run_adb(
            [
                "shell",
                "am",
                "start",
                "-a",
                "android.intent.action.SENDTO",
                "-d",
                f"sms:{digits}",
            ]
        )

    def _open_whatsapp_android(self):
        if not self._is_phone_connected():
            self.say(
                "No hay tel�fono Android conectado o adb no est� disponible. Conecta el tel�fono y habilita USB debugging."
            )
            return
        self.say("Abriendo WhatsApp en el tel�fono conectado.")
        self._run_adb(
            ["shell", "monkey", "-p", "com.whatsapp", "-c", "android.intent.category.LAUNCHER", "1"]
        )

    def _open_target(self, text: str):
        if "youtube" in text:
            self.say("Abriendo YouTube.")
            webbrowser.open("https://www.youtube.com")
            return
        if "google" in text:
            self.say("Abriendo Google.")
            webbrowser.open("https://www.google.com")
            return
        if "telegram" in text:
            self.say("Abriendo Telegram Web.")
            webbrowser.open("https://web.telegram.org")
            return
        if "spotify" in text:
            self.say("Abriendo Spotify.")
            webbrowser.open("https://open.spotify.com")
            return
        if "abrir" in text or "abre" in text:
            self.say("Abrir� un navegador para eso.")
            webbrowser.open("https://www.google.com")
            return
        self.say("No s� c�mo abrir eso. Puedo abrir YouTube, Google, Telegram o Spotify.")

    def run(self):
        self.say("Hola, soy Ruiz. Estoy lista para escucharte.")
        while True:
            try:
                if self.wait_for_wake_word():
                    command = self.listen(timeout=6, phrase_time_limit=8)
                    if command:
                        self.process_command(command)
                    else:
                        self.say("No escuch� bien el comando. Intenta de nuevo.")
            except KeyboardInterrupt:
                self.say("Adi�s.")
                break


if __name__ == "__main__":
    assistant = RuizAssistant()
    assistant.run()
