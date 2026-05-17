# -*- coding: utf-8 -*-
import re
from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform as kivy_platform

ANDROID = kivy_platform == "android"

if ANDROID:
    from android import activity
    from jnius import autoclass, PythonJavaClass, java_method

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Intent = autoclass("android.content.Intent")
    Uri = autoclass("android.net.Uri")
    Locale = autoclass("java.util.Locale")
    TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
    RecognizerIntent = autoclass("android.speech.RecognizerIntent")
    Activity = autoclass("android.app.Activity")

KV = """
<MainWidget>:
    orientation: 'vertical'
    padding: 16
    spacing: 12

    Label:
        text: 'Ruiz - Asistente Android'
        size_hint_y: None
        height: self.texture_size[1] + 20
        font_size: '24sp'

    Label:
        text: root.status
        size_hint_y: None
        height: self.texture_size[1] + 20
        text_size: self.width, None
        halign: 'center'

    ScrollView:
        size_hint_y: 0.7
        do_scroll_x: False

        Label:
            text: root.log
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.width, None
            halign: 'left'
            valign: 'top'

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        spacing: 10

        Button:
            text: 'Escuchar'
            on_release: root.on_listen()

        Button:
            text: 'Salir'
            on_release: app.stop()
"""


class RuizAssistant:
    def __init__(self, ui):
        self.ui = ui
        self.tts_ready = False
        self.request_code = 1001
        self.context = PythonActivity.mActivity
        self._init_tts()
        activity.bind(on_activity_result=self._on_activity_result)

    def _init_tts(self):
        self.tts = TextToSpeech(self.context, self.TTSInitListener(self))

    class TTSInitListener(PythonJavaClass):
        __javainterfaces__ = ['android/speech/tts/TextToSpeech$OnInitListener']

        def __init__(self, assistant):
            super().__init__()
            self.assistant = assistant

        @java_method('(I)V')
        def onInit(self, status):
            if status == TextToSpeech.SUCCESS:
                self.assistant.tts_ready = True
                self.assistant.tts.setLanguage(Locale('es', 'ES'))
                self.assistant.speak('Estoy lista para escucharte.')
            else:
                self.assistant.ui.log_message('No se pudo iniciar el motor de voz.')

    def speak(self, text):
        self.ui.update_status(text)
        if self.tts_ready:
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, 'ruiz_tts')
        self.ui.log_message('Ruiz: ' + text)

    def listen(self):
        self.speak('Di ey ruiz y tu comando.')
        intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, 'es-ES')
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, 'Habla ahora')
        self.context.startActivityForResult(intent, self.request_code)

    def _on_activity_result(self, request_code, result_code, intent):
        if request_code != self.request_code:
            return False

        if result_code == Activity.RESULT_OK and intent is not None:
            results = intent.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if results and results.size() > 0:
                text = results.get(0).lower()
                self.ui.log_message('Escuchado: ' + text)
                self.process_command(text)
            else:
                self.speak('No escuché nada. Intenta de nuevo.')
        else:
            self.speak('No pude entender tu voz. Vuelve a intentarlo.')
        return True

    def process_command(self, text):
        if 'ey ruiz' not in text and 'ruiz' not in text:
            self.speak('Por favor, di ey ruiz antes del comando.')
            return

        if any(word in text for word in ['adiós', 'adios', 'salir', 'hasta luego']):
            self.speak('Hasta luego. Estoy aquí cuando me necesites.')
            return

        if any(word in text for word in ['hora', 'qué hora', 'que hora', 'qué hora es']):
            from time import strftime

            now = strftime('%H:%M')
            self.speak(f'Son las {now}')
            return

        if any(word in text for word in ['busca', 'buscar']):
            search_term = text.replace('busca', '').replace('buscar', '').strip()
            if not search_term:
                self.speak('¿Qué quieres que busque?')
                return
            self.search_web(search_term)
            return

        if any(word in text for word in ['llama', 'llamar']):
            self.call_number(text)
            return

        if any(word in text for word in ['mensaje', 'sms', 'envía mensaje', 'enviar mensaje']):
            self.send_sms(text)
            return

        if 'whatsapp' in text:
            self.open_whatsapp()
            return

        if any(word in text for word in ['abre', 'abrir']):
            self.open_target(text)
            return

        self.speak('No entendí el comando. Puedo abrir YouTube, buscar en internet, llamar a un número, enviar mensajes o abrir WhatsApp.')

    def search_web(self, search_term):
        query = search_term.replace(' ', '+')
        url = f'https://www.google.com/search?q={query}'
        self.speak(f'Buscando {search_term}')
        self.open_uri(url)

    def call_number(self, text):
        digits = re.sub(r'\D', '', text)
        if not digits:
            self.speak('Dime el número al que quieres llamar.')
            return
        self.speak(f'Abriendo el marcador para llamar a {digits}')
        uri = Uri.parse(f'tel:{digits}')
        intent = Intent(Intent.ACTION_DIAL, uri)
        self.context.startActivity(intent)

    def send_sms(self, text):
        digits = re.sub(r'\D', '', text)
        if not digits:
            self.speak('Dime el número para el mensaje.')
            return
        self.speak(f'Abriendo mensajes para {digits}')
        uri = Uri.parse(f'sms:{digits}')
        intent = Intent(Intent.ACTION_SENDTO, uri)
        self.context.startActivity(intent)

    def open_whatsapp(self):
        self.speak('Abriendo WhatsApp')
        package_manager = self.context.getPackageManager()
        intent = package_manager.getLaunchIntentForPackage('com.whatsapp')
        if intent is not None:
            self.context.startActivity(intent)
        else:
            self.speak('No encontré WhatsApp instalado en el teléfono.')

    def open_target(self, text):
        if 'youtube' in text:
            self.open_uri('https://www.youtube.com')
            return
        if 'google' in text:
            self.open_uri('https://www.google.com')
            return
        if 'spotify' in text:
            self.open_uri('https://open.spotify.com')
            return
        self.speak('No sé cómo abrir eso. Prueba diciendo abre YouTube o abre WhatsApp.')

    def open_uri(self, url):
        intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        self.context.startActivity(intent)


class MainWidget(BoxLayout):
    status = StringProperty('Presiona Escuchar para comenzar.')
    log = StringProperty('Bienvenido a Ruiz. Di ey ruiz y tu comando.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if ANDROID:
            self.assistant = RuizAssistant(self)
        else:
            self.assistant = None

    def on_listen(self):
        if ANDROID and self.assistant:
            self.assistant.listen()
        else:
            self.log_message('Esta versión está diseñada para Android con Kivy.')

    @mainthread
    def update_status(self, text):
        self.status = text

    @mainthread
    def log_message(self, text):
        self.log += '\n' + text


class RuizAndroidApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    RuizAndroidApp().run()
